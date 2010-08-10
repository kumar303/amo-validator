import os

import validator.submain as submain
from validator.errorbundler import ErrorBundle
from validator.xpi import XPIManager
from validator.constants import *

def _run_test(filename, expectation, should_fail=True, should_reject=False):
    
    name = "tests/resources/submain/%s" % filename
    pack = open(name)
    xpi = XPIManager(pack, name)
    err = ErrorBundle(None, True)
    
    submain._load_install_rdf(err, xpi, expectation)
    
    if should_fail:
        assert err.failed()
    else:
        assert not err.failed()
        assert err.get_resource("install_rdf")
    
    assert err.reject == should_reject
    
    return err


def test_load_irdf_pass():
    "Test that the loader works with a normal install.rdf file"
    
    dt = submain.typedetection.detect_type
    submain.typedetection.detect_type = lambda x, y, z: PACKAGE_ANY
    _run_test("install_rdf.xpi", PACKAGE_ANY, False)
    submain.typedetection.detect_type = dt


def test_load_irdf_unparsable():
    "Tests that the loader fails when the install.rdf is corrupt."
    
    _run_test("install_rdf_unparsable.xpi", None)


def test_load_irdf_no_type():
    "Tests that the loader fails when the type detection fails."
    
    dt = submain.typedetection.detect_type
    submain.typedetection.detect_type = lambda x, y, z: None
    _run_test("install_rdf.xpi", PACKAGE_ANY)
    submain.typedetection.detect_type = dt


def test_load_irdf_correct_type():
    "Tests that the loader passes with valid type detection."
    
    dt = submain.typedetection.detect_type
    submain.typedetection.detect_type = lambda x, y, z: PACKAGE_THEME
    err = _run_test("install_rdf.xpi", PACKAGE_ANY, False)
    submain.typedetection.detect_type = dt
    
    assert err.detected_type == PACKAGE_THEME


def test_load_irdf_expectation():
    "Tests that the loader fails with an invalid expectation."
    
    dt = submain.typedetection.detect_type
    submain.typedetection.detect_type = lambda x, y, z: PACKAGE_THEME
    _run_test("install_rdf.xpi", PACKAGE_EXTENSION, True, True)
    submain.typedetection.detect_type = dt
    
