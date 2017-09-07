"""  """

import datetime
import numpy as np
from bs4 import BeautifulSoup

import sys
sys.path.append('/Users/tom/Desktop/Neurohackweek/PROJECT/DataDrivenCognitiveOntology/')

from lisc.core.utils import comb_terms, extract
from lisc.core.urls import URLS
from lisc.core.requester import Requester

##############################################################################################################
##############################################################################################################

def scrape_cooc(terms_lst_a, terms_lst_b=[], excl_lst_a=[], excl_lst_b=[], db='pubmed', verbose=False):
    """Search through pubmed for all abstracts for co-occurence.

    Parameters
    ----------
    terms_lst_a : list of list of str
        Search terms
    terms_lst_b : list of list of str, optional
        xx
    excl_lst_a : list of list of str, optional
        xx
    excl_lst_b : list of list of str, optional
        xx
    db : str
        xx
    verbose : bool
        xx

    Returns
    -------

    The scraping does an exact word search for two terms.

    The HTML page returned by the pubmed search includes a 'count' field.
    This field contains the number of papers with both terms. This is extracted.
    """

    # Requester object
    req = Requester()

    # Set date of when data was scraped
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    # Get e-utils URLS object. Set retmax as 0, since not using UIDs in this analysis
    urls = URLS(db=db, retmax='0', retmode='xml', field='TIAB')
    urls.build_info(['db'])
    urls.build_search(['db', 'retmax', 'retmode', 'field'])

    # Sort out terms
    n_terms_a = len(terms_lst_a)
    if len(terms_lst_b) == 0:
	    terms_lst_b = terms_lst_a
	    excl_lst_b = excl_lst_a
    n_terms_b = len(terms_lst_b)

    #
    terms_a_counts = np.zeros([n_terms_a])
    terms_b_counts = np.zeros([n_terms_b])

    #
    dat_numbers = np.zeros([n_terms_a, n_terms_b])
    dat_percent = np.zeros([n_terms_a, n_terms_b])

    # Get current information about database being used
    get_db_info(req, urls.info)

    # Initialize count variables to the correct length
    term_a_counts = np.zeros([n_terms_a])
    term_b_counts = np.zeros([n_terms_b])

    # Initialize right size matrices to store data
    dat_numbers = np.zeros([n_terms_a, n_terms_b], dtype=int)
    dat_percent = np.zeros([n_terms_a, n_terms_b])

    # Loop through each ERP term
    for term_a in terms_lst_a:

        # Get the index of the current erp
        a_ind = terms_lst_a.index(term_a)

        # Print out status
        if verbose:
            print('Running counts for: ', terms_lst_a[0])

        # Get number of results for current term search
        url = urls.search + _mk(terms_lst_a[a_ind]) + \
              _mk(excl_lst_a[a_ind], 'NOT')
        term_a_counts[a_ind] = _get_count(req, url)

        # For each ERP, loop through each term term
        for term_b in terms_lst_b:

            # Get the indices of the current term
            b_ind = terms_lst_b.index(term_b)

            # Get number of results for just term search
            url = urls.search + _mk(terms_lst_b[b_ind]) + \
            	_mk(excl_lst_b[b_ind], 'NOT')
            term_b_counts[b_ind] = _get_count(req, url)

            # Make URL - Exact Term Version, using double quotes, & exclusions
            url = urls.search + _mk(terms_lst_a[a_ind]) + \
                    _mk(excl_lst_a[a_ind], 'NOT') + \
                    _mk(terms_lst_b[b_ind], 'AND') + \
                    _mk(excl_lst_b[b_ind], 'NOT')
            print(url)

            count = _get_count(req, url)
            dat_numbers[a_ind, b_ind] = count
            dat_percent[a_ind, b_ind] = count / term_a_counts[a_ind]

    # Set Requester object as finished being used
    req.close()

    return dat_numbers, dat_percent


def get_db_info(req, info_url):
    """Calls EInfo to get info and status of db to be used for scraping.

    Parameters
    ----------
    info_url : str
        URL to request db information from.

    Returns
    -------
    db_info : dict
    	Database information.
    """

    # Get the info page and parse with BeautifulSoup
    info_page = req.get_url(info_url)
    info_page_soup = BeautifulSoup(info_page.content, 'lxml')

    # Set list of fields to extract from eInfo
    fields = ['dbname', 'menuname', 'description', 'dbbuild', 'count', 'lastupdate']

    # Extract basic infomation into a dictionary
    db_info = dict()
    for field in fields:
        db_info[field] = extract(info_page_soup, field, 'str')

    return db_info

##############################################################################################################
##############################################################################################################

def _get_count(req, url):
    """Get the count of how many articles listed on search results URL.

    Parameters
    ----------
    url : str
        URL to search with.
    """

    # Request page from URL
    page = req.get_url(url)
    page_soup = BeautifulSoup(page.content, 'lxml')

    # Get all count tags
    counts = extract(page_soup, 'count', 'all')

    return int(counts[0].text)


def _mk(t_lst, cm=''):
    """Create search term component."""

    if t_lst[0]:
        return cm + comb_terms(t_lst, 'or')
    else:
        return ''
