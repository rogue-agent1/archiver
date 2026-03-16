#!/usr/bin/env python3
"""archiver - Create and extract archives (tar, zip, gz)."""
import argparse, tarfile, zipfile, os, sys, time

def fmt_size(b):
    for u in ['B','KB','MB','GB']:
        if b < 1024: return f"{b:.1f}{u}"
        b /= 1024
    return f"{b:.1f}TB"

def create_tar(output, files, compression='gz'):
    mode = f'w:{compression}' if compression else 'w'
    with tarfile.open(output, mode) as tar:
        for f in files:
            tar.add(f, arcname=os.path.basename(f) if os.path.isfile(f) else f)
            print(f"  + {f}")
    print(f"\nCreated {output} ({fmt_size(os.path.getsize(output))})")

def create_zip(output, files):
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            if os.path.isdir(f):
                for root, dirs, fnames in os.walk(f):
                    for fn in fnames:
                        fp = os.path.join(root, fn)
                        zf.write(fp)
                        print(f"  + {fp}")
            else:
                zf.write(f)
                print(f"  + {f}")
    print(f"\nCreated {output} ({fmt_size(os.path.getsize(output))})")

def extract(archive, dest='.'):
    if tarfile.is_tarfile(archive):
        with tarfile.open(archive) as tar:
            members = tar.getmembers()
            tar.extractall(dest)
            print(f"Extracted {len(members)} files to {dest}")
    elif zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(dest)
            print(f"Extracted {len(zf.namelist())} files to {dest}")
    else:
        print(f"Unknown format: {archive}", file=sys.stderr); sys.exit(1)

def list_archive(archive):
    if tarfile.is_tarfile(archive):
        with tarfile.open(archive) as tar:
            for m in tar.getmembers():
                print(f"  {fmt_size(m.size):>8}  {time.strftime('%Y-%m-%d %H:%M', time.localtime(m.mtime))}  {m.name}")
    elif zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as zf:
            for info in zf.infolist():
                dt = time.strftime('%Y-%m-%d %H:%M', info.date_time + (0,0,0))
                print(f"  {fmt_size(info.file_size):>8}  {dt}  {info.filename}")

def main():
    p = argparse.ArgumentParser(description='Archive utility')
    sub = p.add_subparsers(dest='cmd')
    
    cr = sub.add_parser('create', help='Create archive')
    cr.add_argument('output', help='Output file (.tar.gz, .zip)')
    cr.add_argument('files', nargs='+')
    
    ex = sub.add_parser('extract', help='Extract archive')
    ex.add_argument('archive')
    ex.add_argument('-d', '--dest', default='.')
    
    ls = sub.add_parser('list', help='List archive contents')
    ls.add_argument('archive')
    
    args = p.parse_args()
    if not args.cmd: p.print_help(); return
    
    if args.cmd == 'create':
        if args.output.endswith('.zip'):
            create_zip(args.output, args.files)
        elif args.output.endswith('.tar.gz') or args.output.endswith('.tgz'):
            create_tar(args.output, args.files, 'gz')
        elif args.output.endswith('.tar.bz2'):
            create_tar(args.output, args.files, 'bz2')
        elif args.output.endswith('.tar'):
            create_tar(args.output, args.files, '')
        else:
            create_tar(args.output + '.tar.gz', args.files, 'gz')
    elif args.cmd == 'extract':
        extract(args.archive, args.dest)
    elif args.cmd == 'list':
        list_archive(args.archive)

if __name__ == '__main__':
    main()
