import pytest

from xmelange.xsd.elements import XsdElement


def test_xsdElement_xsdFactory():
    element = XsdElement(name='testElement', type='string')
    xsd = element.xsd()

    assert 'element' in xsd.tag
    assert xsd.attrib['name'] == 'testElement'
    assert 'string' in xsd.attrib['type']
