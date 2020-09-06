import pytest

from xmelange.xsd.elements import XsdElement


# TODO: write test class for every class in xmelange.xsd.elements

def test_XsdElement_xsdFactory():
    element = XsdElement(name='testElement', type='string')
    xsd = element.xsd()

    assert 'element' in xsd.tag
    assert xsd.attrib['name'] == 'testElement'
    assert 'string' in xsd.attrib['type']
