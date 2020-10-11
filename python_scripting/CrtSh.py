#!/usr/bin/env python3

#TODO: Make sure that PEP8 (style), PEP484 (type hints)
# as well as PEP257 (docstrings) is followed.

import requests
import argparse
import sys
import logging
import re
import json
from bs4 import BeautifulSoup
from datetime import date

def argument_setup():
    """
    argument_setup [Set-up for command-line interface]

    Returns: 
        namespace object
    """
    parser = argparse.ArgumentParser(description="crt_sh subdomain searcher")
    parser.add_argument('--domain', metavar='domain', 
    help='the domain to check for subdomains (default: betauia.net)',
    default="betauia.net")
    return parser.parse_args()  

class CrtSh:
    def __init__(self, url: str):
        """
        Constructor for CrtSh.

        Parameters:

        Args:
            url (str): [The url of to check for subdomains]

        Returns:

        """

        self.url = url
        self.live_domains = []
        self.dead_domains = []
        self.date = date.today().strftime("%d-%m-%Y")

    def check_crtsh(self):
        """Checks if https://crt.sh/ responds with 200

        Returns:
            r: Response object
            Throws exception SystemExit if status code is != 200
        """

        r = requests.get('https://crt.sh/')
        if(r.status_code != 200):
            logging.info(f'https://crt.sh/ returned {r.status_code}, exiting program.')
            sys.exit(69)
        return r

    def validate_url_string(self, url:str):
        """Checks if the string seems to be a valid url using regex
        
        Returns: True if match, false if not. 
        """

        if(re.fullmatch(r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", url) != None):
            logging.info(f'Url {self.url} matches regex')
            return True
            
        logging.info(f'Url {self.url} does not match regex')
        return False
    
    def get_domains(self):
        """
        query_domain []
        Returns:
        set of str
        """

        payload = {'q': self.url}
        r = requests.get('https://crt.sh', params=payload)

        soup = BeautifulSoup(r.text, 'lxml')
        tables = soup.find_all('table')

        domains_set = set()
  
        # The web page has 3 tables, whithout any ID, nested inside each other. 
        # We want the third table
        # Table headers: 
        # [crt.sh ID, Logged at, Not Befor, Not After, Common Name, Matchin identities, Issuer Name]

        if(len(tables) < 3):
            domains_set.add('NaN')
            return domains_set
        rows = tables[2].findAll('tr')
        
        for row in rows:
            cells = row.findAll('td')
            if((len(cells)) > 3):
                
                #We add the Common Name to our domains_set first
                logging.info(f'Adding {cells[4].text} to domains list')
                domains_set.add(cells[4].text)

                # Matchin Identitites column can contain several domains separated with a <br>-tag:
                matching_idents = (str(cells[5]).replace('<td>', '').replace('</td>', '').split('<br/>'))
                
                for ident in matching_idents:
                    domains_set.add(ident)
        return domains_set
    
    def valid_subdomains(self, domains_set: set):
        valid_domains = set()
        for domain in domains_set:
            if self.validate_url_string(domain):
                valid_domains.add(domain)
        return valid_domains


    def check_subdomains(self, valid_set: set):
        for domain in valid_set:
            try:
                r = requests.get(f'http://{domain}', timeout=2)
                if(r.status_code == 200):
                    self.live_domains.append(domain)
            except:
                self.dead_domains.append(domain)

    #TODO: Visit each active domain and grep header and store it together
    # with the domain in a JSON file
    # Vi vil ha <title>
    
    def grep_title(self):
        titles = {}
        for domain in self.live_domains:
            r = requests.get(f'http://{domain}', timeout=3)
            try:
                title = BeautifulSoup(r.text, 'lxml').find('title').text
            except:
                title = 'NaN'
            titles[domain] = title

        with open(f'titles_{self.date}.json', "a") as write_file:
            json.dump(titles, write_file)

    def print_titles(self):
        with open(f'titles_{self.date}.json') as read_file:
            parsed = json.load(read_file)
        print(json.dumps(parsed, indent=2, sort_keys=True))
                

if __name__ == "__main__":
    args = argument_setup()
    crt_sh = CrtSh(args.domain)
    crt_sh.check_crtsh()

    if not(crt_sh.validate_url_string(args.domain)): 
        print('Not valid url, exiting')
        sys.exit(42)

    print(f'\ncrt.sh is online, url seems ok. \nStarting search for subdomains for {crt_sh.url}')
    valid_domains = crt_sh.valid_subdomains(crt_sh.get_domains())
    print(f'Found {len(valid_domains)} subdomains.')
    crt_sh.check_subdomains(valid_domains)
    
    print(f'\nLiving Domains ({float(len(crt_sh.live_domains))/float(len(valid_domains))*100}%)')
    for domain in crt_sh.live_domains:
        print(domain)
        
    print(f'\nDead Domains ({float(len(crt_sh.dead_domains))/float(len(valid_domains))*100}%)')
    for domain in crt_sh.dead_domains:
        print(domain)

    print(f'\nLooking for titles.')
    crt_sh.grep_title()
    crt_sh.print_titles()