import pytest

from xmelange.xsd.elements import xsdElement


def test_xsdElement_xsdFactory():
    element = xsdElement(name='testElement', type='string')
    xsd = element.xsd()

    assert 'element' in xsd.tag
    assert xsd.attrib['name'] == 'testElement'
    assert 'string' in xsd.attrib['type']