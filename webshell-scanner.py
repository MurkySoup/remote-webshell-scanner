#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Remote Webshell Scanner, Version 0.4.9-beta (do not distribute)
By Rick Pelletier (galiagante@gmail.com), 01 May 2024
Last update: 23 September 2025

---

Basic features:
- URL schema validation
- Cache bypass on requests
- Will not follow redirections
- Adds delays between requests

Example useage:
# ./webshell-scanner.py --agents agents-list-example.txt --directories directory-list-example.txt --webshells webshell-name-list-example.txt --url http://www.example.com

Note: All config files are user-defined, text-based, with one valid entry per line.
Leading and trailing whitespaces should be avoided.
"""


import sys
import argparse
import requests
import urllib.parse
import random
from typing import List
import time
import re


def read_config_file(config_filename:str) -> List[str]:
    try:
        with open(config_filename, 'r') as config_data:
            return [line.strip() for line in config_data.readlines()]
    except IOError as e:
        raise RuntimeError(f'Failed to read config file {config_filename}: {e}')


def scan_url(url:str, agent:str) -> int:
    local_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent':f'{agent}'
    }

    try:
        r = requests.get(f'{url}', headers = local_headers, timeout = 30, allow_redirects = False)
        r.raise_for_status()

        return r.status_code
    except Exception as e:
        return r.status_code


def generate_128bit_hex() -> str:
    return f'{random.getrandbits(128):032x}'


def wait_random_time() -> None:
    delay = random.uniform(0.0, 0.5)
    time.sleep(delay)


def scan_controller(url:str, config_data:list, fuzz_data:list, agent_string:str) -> None:
    target_list = list()
    clean_url = url[:-1] if url.endswith('/') else url

    for a in config_data:
        target_list.append(f'{clean_url}/{urllib.parse.quote(a)}?q={generate_128bit_hex()}')

        for y in fuzz_data:
            endpoint = urllib.parse.quote(f'{y}/{a}')
            target_list.append(f'{clean_url}/{endpoint}?q={generate_128bit_hex()}')

    for target_url in target_list:
        if (response_code := scan_url(target_url, agent_string)) == 200:
            print(f'{target_url}')

        wait_random_time()


def is_valid_url(url: str, *, allowed_schemes: set[str] | None = None) -> bool:
    msg = 'Invalid URL'
    url = url.strip()
    parsed = urllib.parse.urlparse(url)

    if not parsed.scheme:
        raise RuntimeError(msg)

    if allowed_schemes is not None and parsed.scheme.lower() not in allowed_schemes:
        raise RuntimeError(msg)

    if not parsed.netloc:
        raise RuntimeError(msg)

    host = parsed.hostname

    if host is None:
        raise RuntimeError(msg)

    if re.search(r'[a-zA-Z0-9.-]+', host) is None:
        raise RuntimeError(msg)

    if (not host or host == 'localhost' or host == '127.0.0.1' or host.startswith('[')) and parsed.port is None:
        pass
    elif "." not in host:
        raise RuntimeError(msg)

    return url


if __name__ == '__main__':
    exit_value = 0
    parser = argparse.ArgumentParser()

    parser.add_argument("--webshells", "-w", type=str, required=True)
    parser.add_argument("--directories", "-d", type=str, required=True)
    parser.add_argument("--agents", "-a", type=str, required=True)
    parser.add_argument("--url", "-u", type=str, required=True)

    args = parser.parse_args()

    try:
        user_agent_data = read_config_file(args.agents)
        config_data = read_config_file(args.webshells)
        fuzz_data = read_config_file(args.directories)
        url_data = is_valid_url(args.url)
    except RuntimeError as err:
        print(err)
        sys.exit(1)

    scan_controller(url_data, config_data, fuzz_data, random.choice(user_agent_data))

    sys.exit(0)
else:
    sys.exit(1)

# end of script
