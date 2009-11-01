#!/usr/bin/python

# Copyright Hugh Perkins 2009
# hughperkins@gmail.com http://manageddreams.com
# 
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
#  more details.
#
# You should have received a copy of the GNU General Public License along
# with this program in the file licence.txt; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-
# 1307 USA
# You can find the licence also on the web at:
# http://www.opensource.org/licenses/gpl-license.php
#
# ======================================================================================
#

import sys
import os
import subprocess

vboxmanagepath = None

def run(commandandarglist):
   popen = subprocess.Popen( commandandarglist, stdout = subprocess.PIPE, stderr = subprocess.PIPE )
   popen.wait()
   (stdout,stderr) = popen.communicate(None)

   return ( stdout, stderr )

def vboxmanage(commandlist):
   (stdout,stderr) = run(  [vboxmanagepath, '--nologo'] + commandlist)
   return (stdout,stderr)

def getvms():
   (stdout,stderr) = vboxmanage( ['list', 'vms' ])
   vms = []
   for line in stdout.split("\n"):
      if line.strip() != '':
         vms.append(line.split('"')[1])
   return vms

def createvm( vmname ):
   print vboxmanage(['createvm','--name',vmname,'--register'])[0]

def setmemory(vmname, megabytes ):
   print vboxmanage(['modifyvm',vmname, '--memory', str(megabytes)+'MB'])[0]   

def setnic(vmname, nicnumber, type ):
   print vboxmanage(['modifyvm',vmname, '--nic' + str(nicnumber), type ])[0]   

def setharddrive(vmname, harddrivenumber, imagefilepath ):
   print vboxmanage(['modifyvm',vmname, '--hd' + 'abcdef'[harddrivenumber - 1:harddrivenumber], type ])[0]   

def addSharedFolder( vmname, sharedfoldername, sharedfolderhostpath, readonly = True ):
   args = [ 'sharedfolder','add', vmname, '--name', vmname, '--hostpath', sharedfolderhostpath ]
   if readonly:
      args.append('--readonly')
   print vboxmanage( args )

def removeSharedFolder( vmname, sharedfoldername ):
   args = [ 'sharedfolder','remove', vmname, '--name', vmname ]
   print vboxmanage( args )

def importAppliance( ovffilepath ):
   print "Importing appliance " + ovffilepath + " ..."
   print vboxmanage(['import',ovffilepath ])[0]

def getvminfo( vmname ):
   stdout = vboxmanage( ['showvminfo',vmname ])[0]
   print stdout
   vminfo = {}
   vminfo['nics'] = {}
   for line in stdout.split("\n"):
      if line.startswith( "UUID:" ):
         vminfo['uuid'] = line[17:]
      if line.startswith( "Memory size:" ):
         vminfo['memory'] = line[17:]
      if line.startswith( "NIC" ):
         nicnumber = int(line[4:5])
         vminfo['nics'][nicnumber] = {}
         nicline = line[17:]
         if nicline.find('NAT') != -1:
            vminfo['nics'][nicnumber]['type'] = 'nat'
         if nicline.find('Host-only Interface') != -1:
            vminfo['nics'][nicnumber]['type'] = 'hostonly'
         if nicline.find('disabled') != -1:
            vminfo['nics'][nicnumber] = None
   return vminfo


