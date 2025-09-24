# remote-webshell-scanner

Tool for remotely scanning endpoint for possible webshells

## Description

This is a simples scanner that searches a target URL hierarchy for the presence of specific named files at specific endpoints.

Basic features:
* URL schema validation included
* Requests strings are URL-Encoded
* Cache bypass on requests
* Will not follow redirections
* Adds delays between requests

## Prerequisites

Requires Python 3.x (preferably 3.8+) and uses the following (entirely standard) libraries:
* sys
* argparse
* requests
* urllib.parse
* random
* typing
* time
* re

## How to Use

```
usage: webshell-scanner.py [-h] --webshells WEBSHELLS --directories DIRECTORIES --agents AGENTS --url URL

options:
  -h, --help                 show this help message and exit
  --webshells WEBSHELLS,     -w WEBSHELLS
  --directories DIRECTORIES, -d DIRECTORIES
  --agents AGENTS,           -a AGENTS
  --url URL,                 -u URL
```

```
./webshell-scanner.py --agents agents-list-example.txt \
  --directories directory-list-example.txt \
  --webshells webshell-name-list-example.txt \
  --url http://www.example.com
```

Note: All config files are user-defined, text-based, with one valid entry per line. Leading and trailing whitespaces should be avoided.

## Built With

* [Python](https://www.python.org) designed by Guido van Rossum

## Author

**Rick Pelletier**
