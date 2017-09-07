"""Scraper functions for LISC."""

import datetime
import numpy as np
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords

import sys
sys.path.append('/Users/tom/Desktop/Neurohackweek/PROJECT/DataDrivenCognitiveOntology/')

from lisc.core.utils import comb_terms, extract, CatchNone, CatchNone2
from lisc.data import Data
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
    db_info = _get_db_info(req, urls.info)

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


def scrape_dat_words(terms, labels, exclusions, db='pubmed', retmax=None, use_hist=False, verbose=False):
    """Search through pubmed for all abstracts referring to a given ERP.

    The scraping does an exact word search for the ERP term given.
    It then loops through all the artciles found about that data.
    For each article, pulls title, year and word data.

    Notes
    -----
    - Pulls data using the hierarchical tag structure that organize the articles.
    - Initially, the procedure was to pull all tags of a certain type.
        For example: extract all 'DateCreated' tags.
        This procedure fails (or badly organizes data) when an articles is
            missing a particular tag.
        Now: take advantage of the hierarchy, loop through each article tag.
            From here, pull out the data, if available.
            This way, can deal with cases of missing data.

    NOTE: retmax currently not used when use_hist is True (will scrape all)
    """

    # Requester object
    req = Requester()

    # Set date of when data was collected
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    # Get e-utils URLS object
    hist_val = 'y' if use_hist else 'n'
    urls = URLS(db=db, usehistory=hist_val, retmax=retmax, retmode='xml', field='TIAB', auto_gen=False)
    urls.build_info(['db'])
    urls.build_search(['db', 'usehistory', 'retmax', 'retmode', 'field'])
    urls.build_fetch(['db', 'retmode'])

    # Get current information about database being used
    db_info = _get_db_info(req, urls.info)

    # Loop through all the erps
    for ind, lab in enumerate(labels):

        # Print out status
        if verbose:
            print('Scraping words for: ', lab)

        # Initiliaze object to store data for current erp papers
        cur_dat = Data(lab, terms[ind])

        # Set up search terms - add exclusions, if there are any
        if exclusions[ind][0]:
            term_arg = comb_terms(terms[ind], 'or') + comb_terms(exclusions[ind], 'not')
        else:
            term_arg = comb_terms(terms[ind], 'or')

        # Create the url for the erp search term
        url = urls.search + term_arg

        # Get page and parse
        page = req.get_url(url)
        page_soup = BeautifulSoup(page.content, 'lxml')

        # Using history
        if use_hist:

            #
            ret_start = 0
            ret_max = 100

            #
            count = int(page_soup.find('count').text)
            web_env = page_soup.find('webenv').text
            query_key = page_soup.find('querykey').text

            # Update History
            cur_dat.update_history('Start Scrape')

            #
            while ret_start < count:

                #
                art_url = urls.fetch + '&WebEnv=' + web_env + '&query_key=' + query_key + \
                          '&retstart=' + str(ret_start) + '&retmax=' + str(ret_max)
                art_page = req.get_url(art_url)
                art_page_soup = BeautifulSoup(art_page.content, "xml")

                # Pull out articles
                articles = art_page_soup.findAll('PubmedArticle')

                # Loop through each article, extracting relevant information
                for ind, art in enumerate(articles):

                    # Get ID of current article
                    new_id = _process_ids(extract(art, 'ArticleId', 'all'), 'pubmed')

                    # Extract and add all relevant info from current articles to Data object
                    cur_dat = _extract_add_info(cur_dat, new_id, art)

                #
                ret_start += ret_max

        # Without using history
        else:

            # Get all ids
            ids = page_soup.find_all('id')

            # Convert ids to string
            ids_str = _ids_to_str(ids)

            # Get article page
            art_url = urls.fetch + '&id=' + ids_str
            art_page = req.get_url(art_url)
            art_page_soup = BeautifulSoup(art_page.content, "xml")

            # Pull out articles
            articles = art_page_soup.findAll('PubmedArticle')

            # Update History
            cur_dat.update_history('Start Scrape')

            # Loop through each article, extracting relevant information
            for ind, art in enumerate(articles):

                # Get ID of current article
                new_id = int(ids[ind].text)

                # Extract and add all relevant info from current articles to Data object
                cur_dat = _extract_add_info(cur_dat, new_id, art)

        # Check consistency of extracted results
        cur_dat.check_results()
        cur_dat.update_history('End Scrape')

        # Save out and clear data
        cur_dat.save_n_clear()

    # Set Requester object as finished being used
    req.close()


##############################################################################################################
##############################################################################################################

def _get_db_info(req, info_url):
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


#######################################################################################################
################################# ERPSC - WORDS - FUNCTIONS (PRIVATE) #################################
#######################################################################################################

def _extract_add_info(cur_dat, new_id, art):
    """Extract information from article web page and add to

    Parameters
    ----------
    cur_dat : Data() object
        Object to store information for the current ERP term.
    new_id : int
        Paper ID of the new paper.
    art : bs4.element.Tag() object
        Extracted pubmed article.

    NOTES
    -----
    - Data extraction is all in try/except statements in order to
    deal with missing data, since fields may be missing.
    """

    # Add ID of current article
    cur_dat.add_id(new_id)
    cur_dat.add_title(extract(art, 'ArticleTitle', 'str'))
    cur_dat.add_authors(_process_authors(extract(art, 'AuthorList', 'raw')))
    cur_dat.add_journal(extract(art, 'Title', 'str'), extract(art, 'ISOAbbreviation', 'str'))
    cur_dat.add_words(_process_words(extract(art, 'AbstractText', 'str')))
    cur_dat.add_kws(_process_kws(extract(art, 'Keyword', 'all')))
    cur_dat.add_pub_date(_process_pub_date(extract(art, 'PubDate', 'raw')))
    cur_dat.add_doi(_process_ids(extract(art, 'ArticleId', 'all'), 'doi'))

    # Increment number of articles included in Data
    cur_dat.increment_n_articles()

    return cur_dat


def _ids_to_str(ids):
    """Takes a list of pubmed ids, returns a str of the ids separated by commas.

    Parameters
    ----------
    ids : bs4.element.ResultSet
        List of pubmed ids.

    Returns
    -------
    ids_str : str
        A string of all concatenated ids.
    """

    # Check how many ids in list
    n_ids = len(ids)

    # Initialize string with first id
    ids_str = str(ids[0].text)

    # Loop through rest of the id's, appending to end of id_str
    for i in range(1, n_ids):
        ids_str = ids_str + ',' + str(ids[i].text)

    # Return string of ids
    return ids_str


@CatchNone
def _process_words(text):
    """Processes abstract text - sets to lower case, and removes stopwords and punctuation.

    Parameters
    ----------
    text : str
        Text as one long string.

    Returns
    -------
    words_cleaned : list of str
        List of words, after processing.
    """

    # Tokenize input text
    words = nltk.word_tokenize(text)

    # Remove stop words, and non-alphabetical tokens (punctuation). Return the result.
    return [word.lower() for word in words if ((not word.lower() in stopwords.words('english'))
                                               & word.isalnum())]


@CatchNone
def _process_kws(keywords):
    """Processes keywords - extract the keywords from tags and converts to strings.

    Parameters
    ----------
    kws : bs4.element.ResultSet
        List of all the keyword tags.

    Returns
    -------
    list of str
        List of all the keywords.
    """

    # NOTE: UPDATE WITH MOVE TO PY35
    return [kw.text.lower() for kw in keywords]
    #return [kw.text.encode('ascii', 'ignore') for kw in keywords]


@CatchNone
def _process_authors(author_list):
    """

    Parameters
    ----------
    author_list : bs4.element.Tag
        AuthorList tag, which contains tags related to author data.

    Returns
    -------
    out : list of tuple of (str, str, str, str)
        List of authors, each as (LastName, FirstName, Initials, Affiliation).
    """

    # Pull out all author tags from the input
    authors = extract(author_list, 'Author', 'all')

    # Initialize list to return
    out = []

    # Extract data for each author
    for author in authors:
        out.append((extract(author, 'LastName', 'str'), extract(author, 'ForeName', 'str'),
                    extract(author, 'Initials', 'str'), extract(author, 'Affiliation', 'str')))

    return out


@CatchNone2
def _process_pub_date(pub_date):
    """

    Parameters
    ----------
    pub_date : bs4.element.Tag
        PubDate tag, which contains tags with publication date information.

    Returns
    -------
    year : int
        xx
    month : str
        xx
    """

    # Extract year, convert to int if not None
    year = extract(pub_date, 'Year', 'str')
    if year: year = int(year)

    # Extract month
    month = extract(pub_date, 'Month', 'str')

    return year, month


@CatchNone
def _process_ids(ids, id_type):
    """

    Parameters
    ----------
    ids : bs4.element.ResultSet
        All the ArticleId tags, with all IDs for the article.

    Returns
    -------
    str or None
        The DOI if available, otherwise None.
    """

    lst = [str(i.contents[0]) for i in ids if i.attrs == {'IdType' : id_type}]

    if lst == []: return None
    else: return lst[0]

