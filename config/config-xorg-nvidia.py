#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#       config-xorg-nvidia.py -- Customise the xorg.conf for nvidia hardware
#       
#       Copyright 2009 Alberto Milone <alberto.milone@canonical.com>
#       Copyright 2010 Adam McDaniel <adam@jolicloud.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import XKit.xutils, XKit.xorgparser
import sys
import getopt


class XorgConfig:
    source = '/etc/X11/xorg.conf'
    destination = '/etc/X11/xorg.conf'
    
    def __init__(self, custom_source=None, custom_destination=None):
        if custom_source:
            self.source = custom_source
        
        if custom_destination:
            self.destination = custom_destination
        
        try:
            self.xorg_conf = XKit.xutils.XUtils(self.source)
        except (XKit.xorgparser.ParseException, IOError):
            # if the xorg.conf doesn't exist or doesn't validate
            # start with an empty one
            self.xorg_conf = XKit.xutils.XUtils()

    def customiseConfig(self):
        # set DefaultDepth to 24; X.org does not work otherwise
        if len(self.xorg_conf.globaldict['Screen']) == 0:
            # Make Screen section
            screen = self.xorg_conf.makeSection('Screen', identifier='Default Screen')
        self.xorg_conf.addOption('Screen', 'DefaultDepth', '24', position=0, prefix='')

        device = 0
        if len(self.xorg_conf.globaldict['Device']) == 0:
            # Make Device section
            device = self.xorg_conf.makeSection('Device', identifier='Configured Video Device')

        # Set the driver in the Device section:
        self.xorg_conf.setDriver('Device', 'nvidia', device)
        self.xorg_conf.addOption('Screen', 'NoLogo', 'True', optiontype='Option')
        self.xorg_conf.addOption('Screen', 'NoBandwidthTest', 'True', optiontype='Option')

        # Write the changes to the destination file
        self.xorg_conf.writeFile(self.destination)



def usage():
    instructionsList = ['The only accepted parameters are:'
    '\n  -i', '\tUse a custom xorg.conf to read the configuration.',
    
    '\n  -o', '\tUse a custom xorg.conf to write the configuration..',
    
    '\n  -h', '\tShow the help page.',
    ]

    print ''.join(instructionsList)

def main():
    err = 'Error: parameters not recognised'
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'i:o:h', [])
    except getopt.GetoptError, err:
        # print help information and exit:
        sys.stderr.write(str(err)+"\n") # will print something like 'option -a not recognized'
        usage()
        sys.exit(2)
    
    
    
    # If called with no args, show the help page
#    if not opts:
#        usage()
#        sys.exit()
    
    
    source = None
    destination = None
    
    
    for o, a in opts:
        if o in ('-i'):
            source = a
        elif o in ('-o'):
            destination = a
        elif o in ('-h'):
            usage()
            sys.exit()
        else:
            assert False, 'unhandled option'
    
    xconfig = XorgConfig(custom_source=source, custom_destination=destination)
    xconfig.customiseConfig()

if __name__ == '__main__':
    main()
