#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  dependabot_alerts.py
#
#  Copyright 2017 Rajiv Gangadharan <rajiv.gangadharan@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
import os
import sys
import getopt
import requests

def get_dependabot_alerts(org, repos, token):
    headers = {"Authorization": f"Bearer {token}"}
    alerts = []

    if repos:
        repositories = repos.split(",")
        for repo in repositories:
            url = f"https://api.github.com/repos/{org}/{repo}/vulnerability-alerts"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                alerts.extend(response.json())
    else:
        url = f"https://api.github.com/orgs/{org}/vulnerability-alerts"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            alerts = response.json()

    return alerts

def print_table(alerts):
    print("ID\t\tSeverity\tOwner\t\tCreated On")
    print("---------------------------------------------------")
    for alert in alerts:
        alert_id = alert["id"]
        severity = alert["severity"]
        owner = alert["repository"]["owner"]["login"]
        created_on = alert["created_at"]
        print(f"{alert_id}\t{severity}\t\t{owner}\t\t{created_on}")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["org=", "repos=", "with-token"])
    except getopt.GetoptError:
        print("Usage: python program.py --org <organization> [--repos <repositories>] [--with-token]")
        sys.exit(2)

    org = None
    repos = None
    token = os.environ.get("GITHUB_TOKEN")

    for opt, arg in opts:
        if opt == "-h":
            print("Usage: python program.py --org <organization> [--repos <repositories>] [--with-token]")
            sys.exit()
        elif opt == "--org":
            org = arg
        elif opt == "--repos":
            repos = arg
        elif opt == "--with-token":
            token = input("Enter your personal access token (PAT): ")

    if not org:
        print("Organization name is required.")
        sys.exit(2)

    alerts = get_dependabot_alerts(org, repos, token)
    print_table(alerts)

if __name__ == "__main__":
    main()
