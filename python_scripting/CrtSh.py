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

    def validate_url_string(self):
        """
        validate_url_string [Checks if the string seems to be a valid url using regex]
        Returns: True if match, false if not. 
        """

        if(re.fullmatch(r"[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)",self.url) != None):
            logging.info(f'Url {self.url} matches regex')
            return True
            
        logging.info(f'Url {self.url} does not match regex')
        return False
    
    def get_domains(self):
        """
        query_domain []
        Returns: Response object
        """

        payload = {'q': self.url}
        r = requests.get('https://crt.sh', params=payload)

        soup = BeautifulSoup(r.text, 'lxml')
        tables = soup.find_all('table')
        rows = tables[2].findAll('tr')
        domains_set = set()
        for row in rows:
            cells = row.findAll('td')

            if((len(cells)) > 3):
                logging.info(f'Adding {cells[4].text} to domains list')
                domains_set.add(cells[4].text)
                #Dont judge me for this triple replace:
                matching_ident = (str(cells[4])).replace('</br>', '\n').replace('<td>', '').replace('</td>', '')
                domains_set.add(matching_ident)
                
        print(domains_set)

    def sort_subdomains(self):
        pass

    def sort(self):
        pass

    def task_n(self):
        pass

if __name__ == "__main__":


    args = argument_setup()

    crt_sh = CrtSh(args.domain)

    crt_sh.check_crtsh()
    if not(crt_sh.validate_url_string()): 
        print('Not valid url, exiting')
        sys.exit(42)

    print(f'''
    https://crt.sh/ is online, url seems ok.
    Starting search for subdomains for {crt_sh.url}''')

    crt_sh.get_domains()