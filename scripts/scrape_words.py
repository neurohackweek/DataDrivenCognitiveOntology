import sys
sys.path.append('/Users/tom/Desktop/PROJECT/DataDrivenCognitiveOntology')

from lisc.words import Words
from lisc.core.io import save_pickle_obj

###############################################################################
###############################################################################

TEST = False
TERMS_FILE = 'concepts_min'
S_NAME = 'concepts_min'

###############################################################################
###############################################################################

def main():
    """Run scrape of counts data."""

    words = Words()

    if TEST:
        words.set_terms([['P231']])
    else:
        words.set_terms_file(TERMS_FILE)

    print('\n\nSTARTING WORDS SCRAPE')

    words.run_scrape(db='pubmed', retmax='5000', use_hist=True, verbose=True)

    print('\n\nWORDS SCRAPE FINISHED\n\n')

    save_pickle_obj(words, S_NAME)

    print('\n\nWORDS SCRAPE SAVED\n\n')


if __name__ == "__main__":
    main()