"""Base object for ERP-SCANR."""

import pkg_resources as pkg
from bs4 import BeautifulSoup

from erpsc.core.utils import extract
from erpsc.core.requester import Requester
from erpsc.core.errors import InconsistentDataError

######################################################################################
############################### ERPSC - GENERAL - BASE ###############################
######################################################################################

class Base(object):
    """Base class for ERPSC analyses.

    Attributes
    ----------
    db_info : dict()
        Stores info about the database used for scarping data.
    terms_type : {'cognitive', 'disease'}
        Type of terms used.
    labels : list of str
        Label to reference each ERP.
    erps : list of list of str
        Name(s) for each ERP (used as search terms).
    exclusions : list of list str
        Exclusion words for each ERP, used to avoid unwanted articles.
    terms : list of list of str
        Terms words.
    term_labels : list of str
        Labels for each term.
    n_erps : int
        Number of erps.
    n_terms : int
        Number of terms.
    req : Requester() object
        Object to handle URL requests.
    date : str
        Date data was collected.
    """

    def __init__(self):
        """Initialize ERP-SCANR Base() object."""

        # Initialize dictionary to store db info
        self.db_info = dict()

        # Initialize variable to keep track of term type used
        self.terms_type = str()

        # Initialize list of erps & term terms to use, including labels
        self.labels = list()
        self.erps = list()
        self.exclusions = list()
        self.terms = list()
        self.term_labels = list()

        # Initialize counters for numbers of terms
        self.n_erps = int()
        self.n_terms = int()

        # Requester object for handling URL calls
        self.req = Requester()

        # Initialize for date that data is collected
        self.date = str()


    def set_erps(self, erps):
        """Sets the given list of strings as erp terms to use.

        Parameters
        ----------
        erps : list of str OR list of list of str
            List of ERP terms to be used.
        """

        # Unload previous terms if some are already loaded
        self.unload_erps()

        # Set given list as erp words
        for erp in erps:
            erp = _check_type(erp)
            self.labels.append(erp[0])
            self.erps.append(erp)

        # Set the number of erps
        self.n_erps = len(erps)


    def set_erps_file(self):
        """Load ERP terms from a txt file."""

        # Unload previous terms if some are already loaded
        self.unload_erps()

        # Get erps from module data file
        labels = _terms_load_file('erp_labels')
        erps = _terms_load_file('erps')

        # Set the number of erps
        self.n_erps = len(erps)

        # Drop number indices, add labels & erps (as list)
        for i in range(self.n_erps):
            self.labels.append(labels[i][3:])
            self.erps.append(erps[i][3:].split(','))


    def check_erps(self):
        """Print out the current list of erps."""

        # Print out header and all current ERPs
        print('List of ERPs used: \n')
        for lab, erp_lst in zip(self.labels, self.erps):
            print(lab + "\t : " + ", ".join(erp for erp in erp_lst))


    def unload_erps(self):
        """Unload the current set of ERP words."""

        # Check if exclusions are loaded, to empty them if so.
        if self.erps:

            # Print status that ERPs are being unloaded
            print('Unloading previous ERP words.')

            # Reset ERP variables to empty
            self.labels = list()
            self.erps = list()
            self.n_erps = int()


    def set_exclusions(self, exclusions):
        """Sets the given list of strings as exclusion words.

        Parameters
        ----------
        exclusions : list of str OR list of list of str
            List of exclusion words to be used.
        """

        # Unload previous terms if some are already loaded
        self.unload_exclusions()

        # Set given list as erp exclusion words
        for exclude in exclusions:
            self.exclusions.append(_check_type(exclude))

        # Check that the number of exclusions matches n_erps
        if len(exclusions) != self.n_erps:
            raise InconsistentDataError('Mismatch in number of exclusions and erps!')


    def set_exclusions_file(self):
        """Load exclusion words from a txt file."""

        # Unload previous terms if some are already loaded
        self.unload_exclusions()

        # Get exclusion words from module data file
        exclusions = _terms_load_file('erps_exclude')

        # Check that the number of exclusions matches n_erps
        if len(exclusions) != self.n_erps:
            raise InconsistentDataError('Mismatch in number of exclusions and erps!')

        # Drop number indices for exclusions, and set as list
        for i in range(self.n_erps):
            self.exclusions.append(exclusions[i][3:].split(','))


    def check_exclusions(self):
        """Print out the current list of exclusion words."""

        # Print out header and all exclusion words
        print('List of exclusion words used: \n')
        for lab, excs in zip(self.labels, self.exclusions):
            print(lab + "\t : " + ", ".join(exc for exc in excs))


    def unload_exclusions(self):
        """Unload the current set of exclusion words."""

        # Check if exclusions are loaded. If so, print status and empty.
        if self.exclusions:

            # Print status that exclusion words are being unloaded
            print('Unloading previous exclusion words.')

            # Reset exclusions variables to empty
            self.exclusions = list()


    def set_terms(self, terms):
        """Sets the given list of strings as terms to use.

        Parameters
        ----------
        terms : list of str OR list of list of str
            List of terms to be used.
        """

        # Unload previous terms if some are already loaded
        self.unload_terms()

        # Set given list as the terms
        for term in terms:
            self.terms.append(_check_type(term))

        # Set the number of terms
        self.n_terms = len(terms)


    def set_terms_file(self, terms_type):
        """Load terms from a txt file."""

        # Unload previous terms if some are already loaded
        self.unload_terms()

        # Set the type of terms
        self.terms_type = terms_type

        # Get terms from module data file
        terms = _terms_load_file(terms_type)

        # Set the number of terms
        self.n_terms = len(terms)

        # Set as list, and attach to object
        for i in range(self.n_terms):
            self.terms.append(terms[i][:].split(','))


    def check_terms(self):
        """Print out the current list of terms."""

        # Print out header and all term words
        print('List of terms used: \n')
        for terms_ls in self.terms:
            print(", ".join(term for term in terms_ls))


    def unload_terms(self):
        """Unload the current set of terms."""

        # Check if exclusions are loaded, to empty them if so.
        if self.terms:

            # Print status that term words are being unloaded
            print('Unloading previous terms words.')

            # Reset term variables to empty
            self.terms_type = str()
            self.terms = list()
            self.n_terms = int()


    def get_term_labels(self):
        """Get term labels."""

        self.term_labels = [term[-1] for term in self.terms]


    def get_db_info(self, info_url):
        """Calls EInfo to get info and status of db to be used for scraping.

        Parameters
        ----------
        info_url : str
            URL to request db information from.
        """

        # Get the info page and parse with BeautifulSoup
        info_page = self.req.get_url(info_url)
        info_page_soup = BeautifulSoup(info_page.content, 'lxml')

        # Set list of fields to extract from eInfo
        fields = ['dbname', 'menuname', 'description', 'dbbuild', 'count', 'lastupdate']

        # Extract basic infomation into a dictionary
        for field in fields:
            self.db_info[field] = extract(info_page_soup, field, 'str')

##########################################################################################
##########################################################################################
##########################################################################################

def _check_type(term):
    """Check type of input term, and return as a list.

    Parameters
    ----------
    term : str OR list of str
        New term to add to the object.

    Returns
    -------
    list of str
        New term, set as a list.
    """

    # Check the type of the given item, return as list
    if isinstance(term, str):
        return [term]
    elif isinstance(term, list):
        return term

def _terms_load_file(dat_name):
    """Loads a terms data file from within the module.

    Parameters
    ----------
    dat_name : str
        Name of the terms data file to load.

    Returns
    -------
    dat : list of str
        Data from the file.
    """

    # Open file
    f_name = 'terms/' + dat_name + '.txt'
    f_path = pkg.resource_filename(__name__, f_name)
    terms_file = open(f_path, 'r')

    # Pull out data from file
    dat = terms_file.read().splitlines()

    return dat
