#!/usr/bin/python
# -*- coding: utf-8 -*-

# usbdbus.py from the USBManager Package
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

__version__ = "0.9"
__author__ = "Magnun Leno da Silva <magnun.leno@gmail.com>"

import dbus
import shexec

RENAME_COMMANDS = {"vfat":("mlabel", "-i %(block_device)s ::%(new_label)s", "mtools"),
                   "ntfs":("ntfslabel", "%(block_device)s %(new_label)s", "ntfsprogs"),
                   "ntfs-3g":("ntfslabel", "%(block_device)s %(new_label)s", "ntfsprogs"),
                   "ext2":("e2label", "%(block_device)s %(new_label)s", "e2fsprogs"),
                   "ext3":("e2label", "%(block_device)s %(new_label)s", "e2fsprogs"),
                   "ext4":("e2label", "%(block_device)s %(new_label)s", "e2fsprogs")}

class Device:
    def __init__(self, volume, storage, usb_device, devices):
        self.volume = volume
        self.usb_device = usb_device
        self.storage = storage
        self.devices = devices
        self.bus = self.devices.bus

        self.label = None

        self.vendor = None
        self.size = None
        self.is_mounted = None
        self.read_only = None

        self.mount_point = None
        self.block_device = None
        self.fs_type = None
        self.fs_version = None
        self.category = None
        self.product = None
        self.model = None

        self.vendor_full_name = None
        self.product = None
        self.serial = None

        self.command = None
        self.rename_info = None
        self.blocked = False

        self.udi = volume.GetProperty("info.udi")
        obj = self.bus.get_object ("org.freedesktop.Hal", self.udi)
        print " * New device:",
        self.get_info()
        print self.label + " ("+self.block_device+")"
        obj.connect_to_signal("PropertyModified", self.on_device_properties_change, path_keyword='path')

    def get_info(self):
        # Label
        self.label = str(self.volume.GetProperty("volume.label")).strip()

        self.vendor = str(self.storage.GetProperty("storage.vendor")).strip()
        self.size = self.convert_bytes(self.volume.GetProperty("volume.size")).strip()
        self.is_mounted = int(self.volume.GetProperty("volume.is_mounted"))
        self.read_only = int(self.volume.GetProperty("volume.is_mounted_read_only"))

        self.mount_point = str(self.volume.GetProperty("volume.mount_point")).strip()
        self.block_device = str(self.volume.GetProperty("block.device")).strip()
        self.fs_type = str(self.volume.GetProperty('volume.fstype')).strip()
        self.fs_version = str(self.volume.GetProperty('volume.fsversion')).strip()
        self.category = str(self.storage.GetProperty('info.category')).strip()
        self.model = str(self.storage.GetProperty('storage.model')).strip()

        self.vendor_full_name = str(self.usb_device.GetProperty('usb_device.vendor')).strip()
        self.product = str(self.usb_device.GetProperty('usb_device.product')).strip()
        self.serial = str(self.usb_device.GetProperty('usb_device.serial')).strip()

    def convert_bytes(self, size, base=0):
        if type(size) is int:
            size = float(size)

        if size >= 1024.0:
            base = base + 1
            size = size/1024.0
            return self.convert_bytes(size, base)
        else:
            return "%.2lf"%round(size,2) + " " + ['Bytes','KBytes','MBytes','GBytes','PBytes','EBytes','ZBytes','YBytes','BBytes'][base]

    def mount(self):
        print " * Mounting", self.label+'...',
        obj = self.bus.get_object("org.freedesktop.Hal", self.udi)
        try:
            obj.Mount('', '', '', dbus_interface="org.freedesktop.Hal.Device.Volume")
        except dbus.DBusException, msg:
            print 'Erro!'
            return False, msg
        print  'OK'
        return True, None

    def umount(self):
        print " * Umounting", self.label+'...',
        obj = self.bus.get_object("org.freedesktop.Hal", self.udi)
        try:
            obj.Unmount([''], dbus_interface="org.freedesktop.Hal.Device.Volume")
            #obj.Eject([''], dbus_interface="org.freedesktop.Hal.Device.Volume")
        except dbus.DBusException, msg:
            print 'Erro!'
            return False, msg
        print  'OK'
        return True, None

    def is_renamable(self):
        exec_command = False
        self.command = None
        self.rename_info = None
        if RENAME_COMMANDS.has_key(self.fs_type):
            self.rename_info = RENAME_COMMANDS[self.fs_type]
            exec_command = shexec.whereis_command(self.rename_info[0])
            if exec_command:
                self.command = exec_command + " " + self.rename_info[1]
                return True
        return False

    def set_label(self, label):
        if self.command is None:
            return (False, None)
        print  ' * Preparing to rename from', self.label, 'to', label, '...'
        comm = self.command%{"block_device":self.block_device, "new_label":label}
        try:
            (output, error) = shexec.run_sudo_command(comm)
        except:
            return (False, None)

        if len(error) is not 0:
            print '*** erro:',error
            return (False, error)

        self.blocked = True
        print ' * Device', self.label,"("+self.block_device+") is now locked!"
        return (True, None)

    def format(self, new_label, new_fs, fs_options, out_func):
        format_func = None
        return shexec.format(new_fs, new_label, self.block_device, fs_options, out_func)

    def on_device_properties_change(self, key, was_added=None, was_removed=None, path=None):
        self.get_info()
        self.devices.master.device_properties_changed(self)

class Devices:
    '''
        Class that holds all USB Storage device information and controls
        it's adding/removing signals.
    '''
    def __init__(self, master):
        '''
            Starts the class adding:
             - Holds a link tho the master class (in main.py);
             - The devices dictionary;
             - The dbus instance (bus);
             - The HAL Manager instance (hal_manager);
             - Connects the class to the add/remove device signal.
        '''

        self.devices = {}
        self.master = master

        # Starting DBUS
        print "Starting HAL..."
        self.bus = self.master.bus
        self.hal_manager_obj = self.bus.get_object("org.freedesktop.Hal", "/org/freedesktop/Hal/Manager")
        self.hal_manager = dbus.Interface(self.hal_manager_obj, "org.freedesktop.Hal.Manager")

        # Connects to the add/remove device signal
        print "Connecting to signals..."
        self.hal_manager.connect_to_signal("DeviceAdded", self.on_device_add)
        self.hal_manager.connect_to_signal("DeviceRemoved", self.on_device_removed)

        # Loads all devices
        print "Building devices list..."
        self.build_device_list()

    def build_device_list(self):
        '''
            It loads all existing devices. Must be calling only during
            startup. The devices will be atomaticaly added/removed
            in signal functions (on_device_add e on_device_removed).

            For each device founded is added a Device instance and it's
            UDI is used as key in the devices dictionary.
        '''
        self.devices = {}
        self.volume_udi_list = self.hal_manager.FindDeviceByCapability('volume')
        for volume_udi in self.volume_udi_list:
            # DBUS Volume
            volume_obj = self.bus.get_object ("org.freedesktop.Hal", volume_udi)
            volume = dbus.Interface(volume_obj, "org.freedesktop.Hal.Device")

            # DBUS storage
            storage_udi = volume.GetProperty ('block.storage_device')
            storage_obj = self.bus.get_object ("org.freedesktop.Hal", storage_udi)
            storage = dbus.Interface(storage_obj, "org.freedesktop.Hal.Device")

            # Only USB
            if storage.GetProperty("storage.bus") == 'usb':
                # USB Mass Storage Interface
                tmp_udi = storage.GetProperty ('storage.originating_device')
                tmp_obj = self.bus.get_object ("org.freedesktop.Hal", tmp_udi)
                tmp = dbus.Interface(tmp_obj, "org.freedesktop.Hal.Device")

                # USB Device
                tmp_udi = tmp.GetProperty ('info.parent')
                tmp_obj = self.bus.get_object ("org.freedesktop.Hal", tmp_udi)
                usb_device = dbus.Interface(tmp_obj, "org.freedesktop.Hal.Device")

                self.devices[str(volume_udi)] = Device(volume, storage, usb_device, self)


    def add_new_device(self, volume_udi, volume, storage, usb_device):
        '''
            Adds a new device to the Devices instance.
            This function must be called by the on_device_add function.
        '''
        # Create a new device and add it
        new_device = Device(volume, storage, usb_device, self)
        self.devices[str(volume_udi)] = new_device
        return new_device

    def is_usb_storage_device(self, volume_udi):
        '''
            This function analyzes the device to ensure that it is an
            USB Storage Device.
        '''
        # Get volume and volume_obj
        volume_obj = self.bus.get_object ("org.freedesktop.Hal", volume_udi)
        volume = dbus.Interface(volume_obj, "org.freedesktop.Hal.Device")

        # If isn't a volume discard it (Return False)
        if not volume.QueryCapability("volume"):
            return False

        # Get storade and storage object
        storage_udi = volume.GetProperty ('block.storage_device')
        storage_obj = self.bus.get_object ("org.freedesktop.Hal", storage_udi)
        storage = dbus.Interface(storage_obj, "org.freedesktop.Hal.Device")

        # If doesn't use USB discard it (Return False)
        if storage.GetProperty("storage.bus") != 'usb':
            return False

        tmp_udi = storage.GetProperty ('storage.originating_device')
        tmp_obj = self.bus.get_object ("org.freedesktop.Hal", tmp_udi)
        tmp = dbus.Interface(tmp_obj, "org.freedesktop.Hal.Device")

        # USB Device
        tmp_udi = tmp.GetProperty ('info.parent')
        tmp_obj = self.bus.get_object ("org.freedesktop.Hal", tmp_udi)
        usb_device = dbus.Interface(tmp_obj, "org.freedesktop.Hal.Device")

        return [volume, storage, usb_device]

    def list_udi_only(self):
        '''
            This function is responsible for listing the UDI for all
            connected devides. A new dbus querry is made.
        '''
        udis = []
        self.volume_udi_list = self.hal_manager.FindDeviceByCapability('volume')
        for volume_udi in self.volume_udi_list:
            # DBUS Volume
            volume_obj = self.bus.get_object ("org.freedesktop.Hal", volume_udi)
            volume = dbus.Interface(volume_obj, "org.freedesktop.Hal.Device")

            # DBUS storage
            storage_udi = volume.GetProperty ('block.storage_device')
            storage_obj = self.bus.get_object ("org.freedesktop.Hal", storage_udi)
            storage = dbus.Interface(storage_obj, "org.freedesktop.Hal.Device")

            # Only USB
            if storage.GetProperty("storage.bus") == 'usb':
                udis.append(volume_udi)
        return udis

    def get_device_by_udi(self, udi):
        if self.devices.has_key(udi):
            return self.devices[udi]
        return None

    def remove_device(self, udi):
        if self.devices.has_key(udi):
            return self.devices.pop(udi)

    def get_supported_fs(self):
        return shexec.SUPPORTED_FS.keys()

    def on_device_add(self, volume_udi):
        '''
            Function connected to the 'DeviceAdded' signal.
            It adds the new device and notify it to it's master
        '''
        # Ensures it is an USB storage device
        ret = self.is_usb_storage_device(volume_udi)
        if ret is False:
            return
        # Unpack the variables
        volume, storage, usb_device = ret[0], ret[1], ret[2]
        # Adds the new device
        new_device = self.add_new_device(volume_udi, volume, storage, usb_device)
        # Notify the master
        self.master.new_device_added(new_device)

    def on_device_removed(self, volume_udi=None):
        '''
            Functino connected to the 'DeviceRemoved' signal.
            It removes all the obsolete devices and notify it to it's
            master.
        '''
        # List all current connected devices and the old devices
        current_udis = [str(udi) for udi in self.list_udi_only()]
        #old_udis = [udi for udi, device in self.devices]
        old_udis = [udi for udi in self.devices]
        # Finds out witch devices were removed
        removed_udi_list = list(set(old_udis) - set(current_udis))

        # For each removed device
        for removed_udi in removed_udi_list:
            removed_device = self.remove_device(removed_udi)
            self.master.device_removed(removed_device)

    def __len__(self):
        '''
            Return the number of managed devices.
        '''
        return len(self.devices)

    def __getitem__(self, key):
        '''
            Gives the Devices class the capability to work with
            iteraction.
        '''
        return self.devices.items()[key]
