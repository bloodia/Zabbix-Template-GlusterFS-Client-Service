#!/usr/bin/python
# coding: utf-8
# ------------------------------------------------------------------------------
# Script Name  : lld-glusterfs-fuse.py
# Tool Version : 1.0.0
# Arguments    : -
# Options      : -h, --help     show this help message and exit
#              : -v, --version  show version and exit
#              : -t, --fstype   select virtual file system type
#              : -n, --fsname   select virtual file system name
# Usage        : $0 [Option]
# Return       : -
# -------------+-------------------------------------------+--------------------
# Date         | Changes                                   | Author
# -------------+-------------------------------------------+--------------------
# 2017/07/18   | New Creation                              | @bloodia
# ------------------------------------------------------------------------------
# --+----1----+----2----+----3----+----4----+----5----+----6----+----7----+----8

import json
import subprocess
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
                       '-v', '--version',
                       action='version',
                       version='1.0.0',
                       help='show version and exit'
                   )
parser.add_argument(
                       '-t', '--fstype',
                       action='store',
                       help='select virtual file system type'
                   )
parser.add_argument(
                       '-n', '--fsname',
                       action='store',
                       help='select virtual file system name'
                   )
args = parser.parse_args()

if __name__ == '__main__':
    p1 = subprocess.Popen(['cat', '/proc/mounts'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['awk', '{print $2,$3}'],stdin=p1.stdout,stdout=subprocess.PIPE)
    p3 = subprocess.Popen(['grep', '-v', 'sr|loop|ram'], stdin=p2.stdout, stdout=subprocess.PIPE)
    stdout, stderr = p3.communicate()
    data = list()
    for line in stdout.split(b'\n'):
        if line:
            fs = line.split()
            fsname = fs[0].decode('utf-8')
            fstype = fs[1].decode('utf-8')
            if args.fstype:
                if fstype == args.fstype:
                    if args.fsname:
                        m = re.match(r"(%s)" % args.fsname, fsname)
                        if m:
                            data.append({"{#FSNAME}": fsname, "{#FSTYPE}": fstype})
                    else:
                        data.append({"{#FSNAME}": fsname, "{#FSTYPE}": fstype})
            else:
                data.append({"{#FSNAME}": fsname, "{#FSTYPE}": fstype})
    print(json.dumps({"data": data}, indent=4))
