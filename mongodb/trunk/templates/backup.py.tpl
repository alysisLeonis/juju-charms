#!/usr/bin/env python
"""Generate the cronjob to backup with mongodbump."""

from os import chdir
from os import listdir
from os import remove
from os.path import exists
from os.path import join
from datetime import datetime
from shutil import rmtree
import subprocess
from tempfile import mkdtemp


when = datetime.now()
backupdir = '$backup_directory'
tmpdir = mkdtemp()

# Make sure the directory to stick tarballs exist.
if not exists(backupdir):
    subprocess.call([
        'mkdir',
        '-p',
        backupdir,
    ])

# Clean up any old backup copies.
current_backups = listdir(backupdir)
current_backups.sort()
for file in current_backups[0:-$backup_copies]:
    remove(join(backupdir, file))

chdir(tmpdir)

# Generate a pretty unique backup filename.
# The unique name might have slashes in it so replace them.
backup_filename = "%s/%s-%s.tar.gz" % (
    backupdir,
    '$unique_name'.replace('/', '-'),
    when.strftime("%Y%m%d-%H%M%S"),
)

# mongodump creates a directory per db. Drop them all in a tmpdir and then
# we'll tar it up as step 2.
dump = '/usr/bin/mongodump --host 127.0.0.1:$port'
subprocess.call(dump, shell=True)

# Generate the ta
tar = 'tar czvf %s dump/*' % backup_filename
subprocess.call(tar, shell=True)

# Clean up the tmpdir.
rmtree(tmpdir)
