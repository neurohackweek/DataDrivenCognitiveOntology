"""Tests for the ERPData() class and related functions from erpsc."""

from py.test import raises

from erpsc.erp_data import *
from erpsc.tests.utils import TestDB as TDB
from erpsc.tests.utils import load_erp_data

######################################################################################
############################## TESTS - ERPSC - ERP_DATA ##############################
######################################################################################

def test_erp_data():
    """Test the ERPData object."""

    # Check that ERPData returns properly.
    assert ERPData('test', ['test'])

def test_add_id():
    """   """

    erp_dat = load_erp_data()
    erp_dat.add_id(1)

    assert erp_dat.ids

def test_add_title():
    """   """

    erp_dat = load_erp_data()
    erp_dat.add_title('title')

    assert erp_dat.titles

def test_add_authors():
    """   """

    erp_dat = load_erp_data()
    erp_dat.add_authors(('Last', 'First', 'IN', 'School'))

    assert erp_dat.authors

def test_add_journal():
    """   """

    erp_dat = load_erp_data()
    erp_dat.add_journal('Journal name', 'J abbrev')

    assert erp_dat.journals

def test_add_erp_dat():
    """   """

    erp_dat = load_erp_data()
    erp_dat.add_words(['new', 'erp_dat'])

    assert erp_dat.words

def test_add_kws():
    """   """

    erp_dat = load_erp_data()
    erp_dat.add_kws(['list', 'of', 'kws'])

    assert erp_dat.kws

def test_add_pub_date():
    """   """

    erp_dat = load_erp_data()
    erp_dat.add_pub_date((2000, 'Feb'))

    assert erp_dat.years
    assert erp_dat.months

def test_add_doi():
    """   """

    erp_dat = load_erp_data()
    erp_dat.add_doi('doi_str')

    assert erp_dat.dois

def test_increment_n_articles():
    """   """

    erp_dat = load_erp_data()
    erp_dat.increment_n_articles()

    assert erp_dat.n_articles

def test_check_results():
    """   """

    erp_dat = load_erp_data(add_dat=True)

    erp_dat.check_results()

    erp_dat.n_articles += 1

    with raises(InconsistentDataError):
        assert erp_dat.check_results()

def test_update_history():
    """   """
    pass

def test_save():
    """   """

    tdb = TDB()

    erp_dat = load_erp_data(add_dat=True)

    erp_dat.save(tdb)

    assert True

def test_load():
    """   """

    tdb = TDB()

    erp_dat = ERPData('test')
    erp_dat.load(tdb)

    assert erp_dat

def test_clear():
    """   """

    erp_dat = load_erp_data(add_dat=True)
    erp_dat.clear()
    erp_dat.check_results()
    assert erp_dat.n_articles == 0

def test_save_n_clear():
    """   """

    erp_dat = load_erp_data(add_dat=True)
    erp_dat.save_n_clear()

    assert erp_dat.n_articles == 0
