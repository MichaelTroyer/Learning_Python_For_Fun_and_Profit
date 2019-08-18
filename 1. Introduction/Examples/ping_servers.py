from datetime import datetime
import csv
import os
import re
import shlex  
from subprocess import check_output, Popen, PIPE, STDOUT


"""
mtroyer
3/1/2019

Ping each server in server list n times
and write datetime and resuts to csv.
"""


def get_cmd_output(cmd):
    """
    Execute a terminal command and return its output.
    Print errors to the console.
    """
    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=STDOUT).communicate()[0]


def get_ping_times(host, nPings):
    """
    ping host with nPing number of pings and return
    a dict of host, date, and (time, TTL) tuples.
    """
    now = datetime.now()
    results = {
        'Year'   : now.year,
        'Month'  : now.month,
        'Day'    : now.day,
        'Hour'   : now.hour,
        'Host'   : host,
        'Replies': []
        }

    cmd = 'ping -n {} {}'.format(nPings, host)
    output = get_cmd_output(cmd)
    output = [item for item in output.split('\n') if item.startswith('Reply')]
    
    regex = 'time=([0-9]+)ms TTL=([0-9]+)'
    for item in output:
        match = re.search(regex, item)
        if match:
            time = match.group(1)
            ttl  = match.group(2)
            results['Replies'].append((time, ttl))
        
    return results


def write_results_to_csv(results, csv_path):
    """
    Write get_ping_times results dict to a csv.
    Will create csv if it does not already exist.
    """
    mode = 'ab' if os.path.exists(csv_path) else 'wb'
    header = ('Year', 'Month', 'Day', 'Hour', 'Host', 'Latency(ms)', 'TTL')
    with open(csv_path, mode) as csvfile:
        csvwriter = csv.writer(csvfile)
        if mode == 'wb':
            csvwriter.writerow(header)
        for reply in results['Replies']:
            row = (
                results['Year'],
                results['Month'],
                results['Day'],
                results['Hour'],
                results['Host'],
                ) + reply
            csvwriter.writerow(row)


def ping_servers(hosts, output_csv, nPings=10, skip_network=None):

    # Don't run on home network..
    if not skip_network in check_output("netsh wlan show interfaces"):
        for host in hosts:
            print 'Pinging host: {}'.format(host)
            ping_times = get_ping_times(host, nPings)
            print 'Result: {}'.format(ping_times)
            write_results_to_csv(ping_times, output_csv)


if __name__ == '__main__':

    servers = [
        'ILMOCOP3CT08-11',
        'ILMOCOP3CT08-12',
        'ILMOCOP3CT08-13',
        'ILMOCOP3CT08-14',
        'ILMOCOP3CT08-15',
        'ILMOCOP3CT08-16',
        'ILMOCOP3CT08-17',
        'ILMOCOP3CT08-18',
        'ILMOCOP3CT08-19',
        'ILMOCOP3CT08-20',
        ]

    output_csv = r'C:\Users\mtroyer\python\outputs\ping_results.csv'

    nPings = 10

    skip_network = 'The Floo Network'

    ping_servers(servers, output_csv, nPings, skip_network)
