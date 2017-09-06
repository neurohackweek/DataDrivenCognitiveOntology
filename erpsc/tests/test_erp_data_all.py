"""Tests for the ERPDataAll() class and related functions from erpsc."""

from erpsc.erp_data_all import *
from erpsc.tests.utils import load_erp_data

###################################################################################
###################################################################################
###################################################################################

def test_erp_data_all():
    """
    Note: Constructor calls (& implicitly tests) the combine & create_freq funcs.
    """

    erp_dat = load_erp_data(add_dat=True, n=2)

    erp_dat_all = ERPDataAll(erp_dat)

    assert erp_dat_all

def test_check_funcs():
    """   """

    erp_dat = load_erp_data(add_dat=True, n=2)
    erp_dat_all = ERPDataAll(erp_dat)

    erp_dat_all.check_words(2)
    erp_dat_all.check_kws(2)

    assert True

def test_create_print_summary():
    """   """

    erp_dat = load_erp_data(add_dat=True, n=2)
    erp_dat_all = ERPDataAll(erp_dat)

    erp_dat_all.create_summary()

    assert erp_dat_all.summary

    erp_dat_all.print_summary()

    assert True
