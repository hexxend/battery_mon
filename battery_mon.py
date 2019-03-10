#!/bin/env python
#
# monitor the current battery percentage
# on non-graphical linux systems
#
# Requires python3.x
#
#Copyright (C) 2019  HexXend
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#hexxend@protonmail.com

from os import system
from os import path
from sys import argv, exit
from time import sleep

def get_bat_info():
    """
    Get the current battery life form Linux systems
    and display it as a precentage
    """
    charge_full = "/sys/class/power_supply/BAT1/charge_full"
    charge_now = "/sys/class/power_supply/BAT1/charge_now"

    if path.isfile(charge_full) == False:
        print("Error %s missing" % charge_full)
        exit()

    if path.isfile(charge_now) == False:
        print("Error %s misssing" % charge_now)
        exit()
    
    with open(charge_full, 'r') as charge_cap:
        with open(charge_now, 'r') as charge_percent:
            full = file.read(charge_cap)
            current_level = file.read(charge_percent)
            full = float(full)
            current_level  = float(current_level)

            
    percent = current_level / full
    precent = "%.2f%%" % percent
    display_string = str(precent)
    return display_string

def get_status():
    """
    Get the current battery status
    """
    status = "/sys/class/power_supply/BAT1/status"
    with open(status) as status_read:
        current_status = file.read(status_read)
    current_status = current_status.strip("\n")
    return current_status


def daemon_mode():
    """
    Monitor the battery in the background
    """
    cur_stat = get_status()
    cur_charge = get_bat_info()
    alert = False
    cur_msg = "Current Battery Status: %s %s\n" % (cur_charge, cur_stat)
    print('%s' % cur_msg)
    while alert == False:
        try:
            sleep(5)
            if cur_charge == "1.00%" and cur_stat == "Full":
                update_msg = "\aBattery fully charged"
                alert = True 
                print('%s' % update_msg)
                while alert == True:
                    if get_status() == "Discharging":
                        alert = False
                    else:
                        alert = True

            elif float(cur_charge.strip('%')) <= 0.20 and cur_stat == "Discharging":
                print("\a") 
                update_msg = "Batery level critical! %s %s" % (get_bat_info(), get_status())
                alert = True
                print('%s' % update_msg)
                while alert == True:
                    if get_status() == "Charging":
                        alert = False
                    else:
                        alert = True
                    
            if cur_stat != get_status():
                update_msg = "\aBattery status changed from %s to %s" % (cur_stat, get_status())
                print('%s' % update_msg)
                cur_stat = get_status()

        except KeyboardInterrupt:
            print("\n%s exiting..." % argv[0])
            exit(0)

def get_mode():
    """
    parse commandline arguments
    """
    try:
        mode = argv[1]
        if mode == "-s" or mode == "--status":
            print(get_bat_info(), get_status())
        elif mode == "-d" or mode == "--daemon":
            daemon_mode()
    except IndexError:
        print("usage: %s [options]\nOptions:\n-s, --status    print the current battery status and quit\n-d, --daemon    monitor the battery status in the background and report when the precent drops to 20 or lower" % argv[0])

get_mode()
exit()

