"""
University	Reverse_Search_Name	Reverse_Search_Mail_Address	Status	Check_Method
"""
import logging
from typing import Any, Dict, List

from land_grab.db.gristdb import GristDB

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def write_search_results(reverse_search_names, names, reverse_search_addresses, addresses):
    pass


def main():
    try:
        db = GristDB()
        universities = []  # TODO
        for univ in universities:
            reverse_search_names = univ['Reverse_Search_Name'].split('\n')  # TODO
            reverse_search_addresses = univ['Reverse_Search_Mail_Address'].split('\n')  # TODO
            names: List[List[Dict[str, Any]]] = [
                db.search_indexed_text_column('regrid', 'owner', name)
                for name in reverse_search_names
            ]
            addresses: List[List[Dict[str, Any]]] = [
                db.search_indexed_text_column('regrid', 'owner', address)
                for address in reverse_search_addresses
            ]
            write_search_results(reverse_search_names, names, reverse_search_addresses, addresses)
    except Exception as err:
        log.error(err)


if __name__ == '__main__':
    main()
