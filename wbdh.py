"""
wbdh.py - Windows Bluray Disc Hasher
"""

import os
import sys
import pick
import psutil
import hashlib
import win32api
import win32file
import progressbar

BD_SECTOR_SIZE = 2048


def main():
    print('wdh v0.1\nFinding disc drives...')

    discs = []
    drive_strings = win32api.GetLogicalDriveStrings()
    for d in drive_strings.split('\x00')[:-1]:
        if win32file.GetDriveType(d) == win32file.DRIVE_CDROM:
            discs.append(d)
    if len(discs) < 1:
        print('Error! No discs found.')
        return 1

    disc_path, _ = pick.pick(discs, 'Select disc to hash:', indicator='->')

    sectors = psutil.disk_usage(disc_path).total // BD_SECTOR_SIZE
    bar = progressbar.ProgressBar(max_value=sectors)

    md5sum = hashlib.md5()
    sha1sum = hashlib.sha1()

    full_disc_path = '\\\\.\\{D}:'.format(D=disc_path[0])
    disc_descriptor = os.open(full_disc_path, os.O_RDONLY|os.O_BINARY)

    with os.fdopen(disc_descriptor, 'rb+') as disc:
        print('Hashing {d} (go grab some coffee)...'.format(d=disc_path))
        for counter, _ in enumerate(range(sectors)):
            raw_data = disc.read(BD_SECTOR_SIZE)
            md5sum.update(raw_data)
            sha1sum.update(raw_data)
            bar.update(counter)

    print('\nmd5: {md5}\nsha1: {sha1}'.format(
        md5=md5sum.hexdigest(), sha1=sha1sum.hexdigest()
    ))
    return 0


if __name__ == '__main__':
    sys.exit(main())
