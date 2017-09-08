"""Classe for Count analysis (key word co-occurences in papers)."""

import datetime
import numpy as np
from bs4 import BeautifulSoup

from lisc.base import Base
from lisc.core.urls import URLS
from lisc.core.utils import comb_terms, extract
from lisc.scrape import scrape_counts

##############################################################################################
#################################### LISC - COUNT - CLASS ####################################
##############################################################################################

class Count(object):
    """This is a class for counting co-occurence of pre-specified ERPs & terms.

    Attributes
    ----------
    terms : dict()
        xx
    dat_numbers :
        xx
    dat_percent :
        xc
    """

    def __init__(self):
        """Initialize LISC Count() object."""

        #
        self.terms = dict()
        for dat in ['A', 'B']:
            self.terms[dat] = Base()
            self.terms[dat].counts = np.zeros(0)

        # Initialize data output variables
        self.dat_numbers = np.zeros(0)
        self.dat_percent = np.zeros(0)


    def set_terms(self, terms, dim='A'):
        """   """

        self.terms[dim].set_terms(terms)
        self.terms[dim].counts = np.zeros(self.terms[dim].n_terms)


    def set_exclusions(self, exclusions, dim='A'):
        """   """

        self.terms[dim].set_exclusions(exclusions)


    def run_scrape(self, db='pubmed', verbose=False):
        """   """

        # Run single list of terms against themselves
        if not self.terms['B'].has_dat:
            print('RUNNING A by A')
            self.dat_numbers, self.dat_percent, self.terms['A'].counts, self.terms['B'].counts, self.meta_dat = \
                scrape_counts(
                    terms_lst_a = self.terms['A'].terms,
                    excls_lst_a = self.terms['A'].exclusions,
                    db=db, verbose=verbose)

        # Run two different sets of terms
        else:
            self.dat_numbers, self.dat_percent, self.terms['A'].counts, self.terms['B'].counts, self.meta_dat = \
                scrape_counts(
                    terms_lst_a = self.terms['A'].terms,
                    excls_lst_a = self.terms['A'].exclusions,
                    terms_lst_b = self.terms['B'].terms,
                    excls_lst_b = self.terms['B'].exclusions,
                    db=db, verbose=verbose)


    def check_cooc(self, dim='A'):
        """"Prints out the terms most associatied with each ERP."""

        # Loop through each erp term, find maximally associated term term and print out
        for term_ind, term in enumerate(self.terms[dim].labels):

            # Find the index of the most common association for current term
            assoc_ind = np.argmax(self.dat_percent[term_ind, :])

            # Print out the results
            print("For the  {:5} the most common association is \t {:18} with \t %{:05.2f}"
                  .format(term, self.terms[dim].labels[term_ind], \
                  self.dat_percent[term_ind, assoc_ind]*100))


    def check_top(self, dim='A'):
        """Check the terms with the most papers."""

        # Find and print the term for which the most papers were found
        print("The most studied term is  {:6}  with {:8.0f} papers"
              .format(self.terms[dim].labels[np.argmax(self.terms[dim].counts)], \
              self.terms[dim].counts[np.argmax(self.terms[dim].counts)]))


    def check_counts(self, dim='A'):
        """Check how many papers found for each term.

        Parameters
        ----------

        """

        # Check counts for all terms
        for ind, term in enumerate(self.terms[dim].labels):
            print('{:5} - {:8.0f}'.format(term, self.terms[dim].counts[ind]))


    def drop_data(self, n, dim='A'):
        """Drop terms based on number of article results.

        Parameters
        ----------
        n : int
            Mininum number of articles to keep each term.
        dim : ?
            xx
        """

        keep_inds = np.where(self.terms[dim].counts > n)[0]

        self.terms[dim].terms = [self.terms[dim].terms[i] for i in keep_inds]
        self.terms[dim].labels = [self.terms[dim].labels[i] for i in keep_inds]
        self.terms[dim].counts = self.terms[dim].counts[keep_inds]

        self.terms[dim].n_terms = len(self.terms[dim].terms)

        if dim == 'A':
            self.dat_numbers = self.dat_numbers[keep_inds, :]
            self.dat_percent = self.dat_percent[keep_inds, :]
        if dim == 'B':
            self.dat_numbers = self.dat_numbers[:, keep_inds]
            self.dat_percent = self.dat_percent[:, keep_inds]
