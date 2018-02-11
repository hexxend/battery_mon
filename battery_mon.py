#!/bin/env python
#
#  monitor the current battery percentage
#  hexxend 2/10/2018

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
    cur_stat = get_status()
    cur_charge = get_bat_info()
    while True:
        try:
            if cur_stat != get_status():
                print("\aBattery status changed from %s to %s" % (cur_stat, get_status()))
                cur_stat = get_status()

            elif cur_charge == "1.00%" and cur_stat == "Full":
                print("\aBattery fully charged")

            elif float(cur_charge.strip('%')) <= 0.20 and cur_stat == "Discharging":
                print("\a") 
                print("Batery level critical!", get_bat_info(), get_status())
                    
        except KeyboardInterrupt:
            print("\n%s exiting..." % argv[0])
            exit(0)

        sleep(5)

def get_mode():
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

