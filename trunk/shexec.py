#!/usr/bin/python
# -*- coding: utf-8 -*-

# shexec.py  from the usbmanager pack
#
# Copyright (c) 2008 Magnun Leno da Silva
#
# Author: Magnun Leno da Silva <magnun.leno@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2 of
# the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USAA.

__version__ = "1.0"
__author__ = "Magnun Leno da Silva <magnun.leno@gmail.com>"


import os
import subprocess as sp
FORMATING_DIC = {"mkfs.vfat":"VFAT",
                 "mkfs.ntfs":"NTFS",
                 #"mkfs.ext2":"EXT2",
                 #"mkfs.ext3":"EXT3",
                 #"mkfs.ext4":"EXT4",
                }

SUPPORTED_FS = {}
ret = sp.Popen(shell = False, stdin = sp.PIPE, stdout = sp.PIPE,
               stderr = sp.PIPE, args = ["whereis", "mkfs"])
ret = ret.communicate()[0].split(' ')[1:]
for fs in ret:
    fs = fs.split('/')[-1]
    if FORMATING_DIC.has_key(fs):
        if FORMATING_DIC[fs] == "VFAT":
            SUPPORTED_FS["FAT32"] = fs
            SUPPORTED_FS["FAT16"] = fs
        else:
            SUPPORTED_FS[FORMATING_DIC[fs]] = fs

def whereis_command(command):
    ret = sp.Popen(shell = False, stdin = sp.PIPE, stdout = sp.PIPE,
                   stderr = sp.PIPE, args = ["whereis", command])
    ret = ret.communicate()
    try:
        ret = ret[0].split(' ')[1]
    except:
        return False
    return ret

def run_sudo_command(command):
    print ' * Attention: Going sudo!'
    print ' **', command
    ret = sp.Popen(shell = False, stdin = sp.PIPE, stdout = sp.PIPE,
                   stderr = sp.PIPE, args = ["gksudo", command])

    return ret.communicate()

def format(new_fs, new_label, block_device, fs_options, out_func):
    command = 'gksudo "'+SUPPORTED_FS[new_fs]+' '+block_device +' '
    if new_fs == "FAT16":
        decode_func = fat16_decode
    if new_fs == "FAT32":
        decode_func = fat32_decode
    if new_fs == "NTFS":
        decode_func = ntfs_decode
    if new_fs == "EXT2":
        decode_func = ext2_decode
    if new_fs == "EXT3":
        decode_func = ext3_decode
    if new_fs == "EXT4":
        decode_func = ext4_decode

    command += decode_func(new_label, fs_options)

    out_func("# "+command+"\n\n")
    print ' * Formating:',command
    proc = sp.Popen([command], shell=True, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    while True:
        out = proc.stdout.read(1)
        out_func(out)
        if len(out) == 0 and proc.poll() == 0:
            break
    return proc.stderr.readlines()


def fat16_decode(new_label, fs_options):
    command = '-F 16 -v '
    bad_blocks = fs_options[0]

    if bad_blocks is True:
        command += '-c '

    if new_label != "":
        if len(new_label) > 11:
            new_label = new_label[:11]
        command += '-n '+new_label
    command += '"'
    return command

def fat32_decode(new_label, fs_options):
    command = '-F 32 -v '
    bad_blocks = fs_options[0]

    if bad_blocks is True:
        command += '-c '

    if new_label != "":
        if len(new_label) > 11:
            new_label = new_label[:11]
        command += '-n '+new_label
    command += '"'
    return command

def ntfs_decode(new_label, fs_options):
    quick_format = fs_options[0]
    compression = fs_options[1]

    command = '-v '

    if quick_format:
        command += '-f '

    if compression:
        command += '-C '

    if new_label != "":
        command += '-L '+new_label
    command += '"'
    return command

def ext2_decode(new_label, dev, fs_options, bar):
    pass

def ext3_decode(new_label, dev, fs_options, bar):
    pass

def ext4_decode(new_label, fs_options, out_func):
    pass
# TODO: Add functions to format volumes (NTFS, EXT2, EXT3 and EXT4)
