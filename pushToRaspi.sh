./clean.sh
#scp -r run.py ./machinery ./webserver pi@192.168.0.42:Development/Jursi/src
rsync -au --stats --exclude=.git --exclude=.gitignore . pi@192.168.0.42:Development/Jursi/src
