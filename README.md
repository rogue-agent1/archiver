# archiver
Create and extract tar/zip archives with listing support.
```bash
python archiver.py create backup.tar.gz src/ docs/
python archiver.py create files.zip *.txt
python archiver.py list backup.tar.gz
python archiver.py extract backup.tar.gz -d /tmp/out
```
## Zero dependencies. Python 3.6+.
