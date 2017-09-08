import sys
sys.path.append('/Users/tom/Desktop/PROJECT/DataDrivenCognitiveOntology')

from lisc.count import Count
from lisc.core.io import save_pickle_obj

###############################################################################
###############################################################################

TEST = False
TERMS_FILE = 'concepts'
S_NAME = 'concepts'

###############################################################################
###############################################################################

def main():
    """Run scrape of counts data."""

    counts = Count()

    if TEST:
        counts.set_terms([['language'], ['visual']])
    else:
        counts.terms['A'].set_terms_file(TERMS_FILE)

        # Reduce number of terms
        counts.terms['A'].terms = counts.terms['A'].terms[:40]
        counts.terms['A'].labels = counts.terms['A'].labels[:40]
        print('N terms:', len(counts.terms['A'].terms))

    print('\n\nSTARTING COUNTS SCRAPE')
    print('RUNNING TERMS TYPE: ', TERMS_FILE, '\n\n')

    counts.run_scrape(verbose=True)

    print('\n\nCOUNTS SCRAPE FINISHED\n\n')

    save_pickle_obj(counts, S_NAME)

    print('\n\nCOUNTS SCRAPE SAVED\n\n')


if __name__ == "__main__":
    main()