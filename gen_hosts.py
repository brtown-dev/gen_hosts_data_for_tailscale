#!/usr/bin/env python3
import argparse
import platform
import subprocess
import re

__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"

default = {
    "target_user": "os-node@",
    "target_ip": "10.0.64.108/24",
    "exceptions": { 
        "jp010-2-via-10": ["fd7a:115c:a1e0:b1a:0:a:a00:416c", "jp010-2"] 
    }
}

def main(args):
    pf = platform.system()

    if pf == "Darwin":
        cmd_status = ["/Applications/Tailscale.app/Contents/MacOS/Tailscale", "status"]
        cmd_whois = ["/Applications/Tailscale.app/Contents/MacOS/Tailscale", "whois"]
        cmd_debug = ["/Applications/Tailscale.app/Contents/MacOS/Tailscale", "debug", "via"]
        msg = 'please add above lines to "/private/etc/hosts".'
    elif pf == "Windows":
        cmd_status = [r"C:\Program Files\Tailscale\tailscale.exe", "status"]
        cmd_whois = [r"C:\Program Files\Tailscale\tailscale.exe", "whois"]
        cmd_debug = [r"C:\Program Files\Tailscale\tailscale.exe", "debug", "via"]
        msg = r'please add above lines to "C:\windows\system32\drivers\etc\hosts".'


    if cmd_status and cmd_whois and cmd_debug:
        # "tailscale status"
        # get list of "tailscale ip of AIO" and "tailscale hostname"
        lines = subprocess.check_output(cmd_status).decode().split('\n')
        status = [re.sub(r'\s+', ' ', x).split(' ')[:2] for x in lines if args.target_user[0] in x and re.search(r'jp.+via', x)]

        # "tailscale whois"
        # identify site-id from "AllowedIPs"
        whois = list()
        for x in status:
            if x[1] not in default["exceptions"]:
                lines = subprocess.check_output(cmd_whois + [x[0]]).decode().split('\n')
                allowedips = [re.findall(r'fd7a.*/120', y) for y in lines if re.search(r'AllowedIPs:', y)]
                site_id_hex = allowedips[0][0].split(':')[5]
                site_id = str(int(site_id_hex, 16))

                ipv6 = subprocess.check_output(cmd_debug + [site_id, args.target_ip]).decode().split("/")[0]


                hostname = x[1].split('-via')[0]
                if args.hostname_suffix:
                    hostname = f'{hostname}-{args.hostname_suffix}'

                print(f'{ipv6} {hostname}')
        print()
        print(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--suffix", action="store", dest="hostname_suffix")
    parser.add_argument("-u", "--user", action="store", dest="target_user", default=default["target_user"])
    parser.add_argument("-i", "--ip", action="store", dest="target_ip", default=default["target_ip"])
    args = parser.parse_args()
    main(args)
