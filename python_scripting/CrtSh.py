#!/usr/bin/env python3

import requests
import argparse
import sys
import logging
import re
import json
import os
import time
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import date

logging.basicConfig(filename='./crtsh.log',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')

def argument_setup():
    """Parses arguments from CLI

    Returns: 
        namespace object : Object containing the names and values of arguments.
    """
    parser = argparse.ArgumentParser(description="crt_sh subdomain searcher")
    parser.add_argument('--domain', metavar='domain', 
    help='the domain to check for subdomains (default: betauia.net)',
    default="betauia.net")
    return parser.parse_args()

class CrtSh:
    def __init__(self, url: str):
        """Constructor for CrtSh.
        """

        self._url=url
        self._live_domains = []
        self._dead_domains = []
        self.valid_domains = []
        self._date= date.today().strftime("%d-%m-%Y")
        self._titles = {}

    def check_connectivity(self):
        """Checks if crt.sh responds with 200

        Returns:
            r: Response object
            Throws exception SystemExit if status code is != 200
        """

        r = requests.get('https://crt.sh/')
        if(r.status_code != 200):
            logging.error(f'https://crt.sh/ returned {r.status_code}, exiting program.')
            sys.exit(69)
        return r

    def validate_url_string(self, url:str):
        """Checks if the string seems to be a valid url using regex

        Returns: True if match, false if not. 
        """

        if(re.fullmatch(r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", url) != None):
            logging.info(f'Url {url} matches regex')
            return True
            
        logging.info(f'Url {url} does not match regex')
        return False
    
    def get_domains(self):
        """Finds subdomains!

        Returns:
            set: Set of subdomains. Single entry 'NaN' if no results are found.
        """
        print(f'\nStarting search for subdomains for {self._url}')

        payload = {'q': self._url}
        r = requests.get('https://crt.sh', params=payload)

        soup = BeautifulSoup(r.text, 'lxml')
        tables = soup.find_all('table')

        domains_set = set()
  
        # The web page has 3 nested tables, whithout any ID. We want the 3rd.
        # Table headers: 
        # [crt.sh ID, Logged at, Not Before, Not After,
        # Common Name, Matching identities, Issuer Name]

        if(len(tables) < 3):
            domains_set.add('NaN')
            return domains_set
        rows = tables[2].findAll('tr')
        
        for row in rows:
            cells = row.findAll('td')
            if((len(cells)) > 3):
                
                #We add the Common Name to our domains_set first
                domains_set.add(cells[4].text)

                # Matchin Identitites column can contain several domains separated with a <br>-tag:
                matching_idents = (str(cells[5]).replace('<td>', '').replace('</td>', '').split('<br/>'))
                
                for ident in matching_idents:
                    domains_set.add(ident)
        logging.info(f'Adding {domains_set} to domains set')
        return domains_set
    
    def valid_subdomain(self, domain: set):
        """Validates a set of domains.

        Args:
            domains_set (set): A set of domains to be validated.

        Returns:
            set: A set of valid domains. Empty set if none are found.
        """
        if self.validate_url_string(domain):
            return domain

    def write_titles_to_file(self):
        if os.path.exists(f'{self._url}-{self._date}.json'):
            logging.info(f'Removing existing file {self._url}-{self._date}.json')
            os.remove(f'{self._url}-{self._date}.json')

        with open(f'{self._url}-{self._date}.json', "a") as write_file:
            json.dump(self._titles, write_file)
            logging.info(f'Finished writing titles to file {self._url}-{self._date}.json')

    def print_titles(self):
        """Prints titles from local JSON-file
        """

        with open(f'{self._url}-{self._date}.json') as read_file:
            parsed = json.load(read_file)
        print(json.dumps(parsed, indent=2, sort_keys=True))

    def print_domains(self):
        """Prints all alive and all dead domains, showing the percentage
        of each
        """

        print(f'Found {len(self.valid_domains)} subdomains.')
        
        print('\nLiving Domains ({:.2f}%)'.format(float(len(self._live_domains))/float(len(self.valid_domains))*100))
        for domain in self._live_domains:
            print(domain)
            
        print('\nDead Domains ({:.2f}%)'.format(float(len(self._dead_domains))/float(len(self.valid_domains))*100))
        for domain in self._dead_domains:
            print(domain)

    async def fetch(self, url, session):
        try:
            async with session.get(url) as response:
                if(response.status==200):
                    self._live_domains.append(url)
                    try:
                        self._titles[url] = BeautifulSoup(await response.text(), 'lxml').find('title').text
                    except:
                        self._titles[url] = 'NaN'
                else:
                    self._dead_domains.append(url)

        except aiohttp.ClientConnectionError as e:
            logging.warning(e.args)

    async def check_subdomains(self, domains):
        tasks = []
        
        # Fetch all responses within one Client session,
        # keep connection alive for all requests.
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for domain in domains:
                task = asyncio.ensure_future(self.fetch(f'http://{domain}', session))
                tasks.append(task)

            await asyncio.gather(*tasks)


if __name__ == "__main__":
    args = argument_setup()
    crt_sh = CrtSh(args.domain)
    
    crt_sh.check_connectivity()

    if not(crt_sh.validate_url_string(args.domain)): 
        print('Not valid url, exiting')
        sys.exit(42)

    print(f'\ncrt.sh is online, url seems ok.')

    domains = crt_sh.get_domains()

    for domain in domains:
        crt_sh.valid_domains.append(crt_sh.valid_subdomain(domain))

    loop = asyncio.get_event_loop()

    future = asyncio.ensure_future(crt_sh.check_subdomains(crt_sh.valid_domains))

    loop.run_until_complete(future)

    crt_sh.print_domains()
    crt_sh.write_titles_to_file()
    crt_sh.print_titles()