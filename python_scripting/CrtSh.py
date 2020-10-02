#!/usr/bin/env python3

import requests
import argparse
import sys
import logging
import re
from bs4 import BeautifulSoup

def argument_setup():
    """
    argument_setup [Set-up for command-line interface]

    Returns: Args (from parser???? hva faen slags objektype er dette a??)
        
    """
    parser = argparse.ArgumentParser(description="crt_sh subdomain searcher")
    parser.add_argument('--domain', metavar='domain', 
    help='the domain to check for subdomains (default: betauia.net)',
    default="betauia.net")
    return parser.parse_args()

class CrtSh:
    def __init__(self, url: str):
        """
        __init__ [summary]

        [extended_summary]

        Args:
            url (str): [The url of to check for subdomains]
        """

        self.url = url
        self.live_domains = []
        self.dead_domains = []

    def check_crtsh(self):
        """
        check_crtsh [Checks if https://crt.sh/ responds with 200]

        Returns:
            [response]: [return http response object]
            Throws exception SystemExit if status code is != 200
        """

        r = requests.get('https://crt.sh/')
        if(r.status_code != 200):
            logging.info(f'https://crt.sh/ returned {r.status_code}, exiting program.')
            sys.exit(69)
        return r

    def validate_url_string(self, url:str):
        """
        validate_url_string [Checks if the string seems to be a valid url using regex]
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
                self.live_domains.append(domain)
            except:
                self.dead_domains.append(domain)

    def sort(self):
        pass

    def task_n(self):
        pass

if __name__ == "__main__":
    args = argument_setup()
    crt_sh = CrtSh(args.domain)
    crt_sh.check_crtsh()

    if not(crt_sh.validate_url_string(args.domain)): 
        print('Not valid url, exiting')
        sys.exit(42)

    print(f'crt.sh is online, url seems ok. \nStarting search for subdomains for {crt_sh.url}')
    valid_domains = crt_sh.valid_subdomains(crt_sh.get_domains())
    print(f'Found {len(valid_domains)} subdomains.')
    crt_sh.check_subdomains(valid_domains)
    
    print()
    print(f'Living Domains ({float(len(crt_sh.live_domains))/float(len(valid_domains))*100}%)')
    for domain in crt_sh.live_domains:
        print(domain)
    
    print()
    print(f'Dead Domains ({float(len(crt_sh.dead_domains))/float(len(valid_domains))*100}%)')
    for domain in crt_sh.dead_domains:
        print(domain)