"""
Examples:
<xsd:simpleType name="myInteger">
  <xsd:restriction base="xsd:integer">
    <xsd:minInclusive value="10000"/>
    <xsd:maxInclusive value="99999"/>
  </xsd:restriction>
</xsd:simpleType>

<xsd:simpleType name="SKU">
  <xsd:restriction base="xsd:string">
    <xsd:pattern value="\d{3}-[A-Z]{2}"/>
  </xsd:restriction>
</xsd:simpleType>

! Simple types cannot have attributes
"""

from lxml import etree
from builtin_simple_types import *
from elements import xsdElement


class xsdRestrictionFacet(xsdElement):
    tag = None

    def __init__(self, value):
        self.value = value

    def xsd_attributes(self):
        return {
            'value': self.value
        }


class xsdRestrictionPattern(xsdRestrictionFacet):
    tag = 'pattern'


class xsdRestrictionMinIncluse(xsdRestrictionFacet):
    tag = 'minInclusive'


class xsdRestrictionMaxIncluse(xsdRestrictionFacet):
    tag = 'maxInclusive'


class xsdRestriction(xsdElement):

    tag = 'restriction'

    def __init__(self, base, facets):
        self.base = base
        self.facets = facets

    def xsd_attributes(self):
        attrib = super().xsd_attributes()
        attrib['base'] = self.build_xsd_type(self.base.tag)
        return attrib

    def xsd(self, parent=None):
        el = super().xsd(parent=parent)
        for facet in self.facets:
            facet.xsd(parent=el)
        return el


class xsdSimpleType(xsdElement):

    tag = 'simpleType'

    def __init__(self, name, restriction):
        super().__init__(name=name, xsd_type=None)
        self.restriction = restriction

    def xsd(self, parent=None):
        el = super().xsd(parent=parent)
        self.restriction.xsd(parent=el)
        return el

    @classmethod
    def restriction(cls, name, base, facets):
        xsd_restriction = xsdRestriction(base=base, facets=facets)
        simple_type = xsdSimpleType(name=name, restriction=xsd_restriction)
        return simple_type



def tostring(element, pretty_print=True, xml_declaration=True, encoding='UTF-8'):
    return etree.tostring(
            element,
            pretty_print=pretty_print,
            xml_declaration=xml_declaration,
            encoding=encoding).decode()



if __name__ == '__main__':
    el = xsdSimpleType.restriction(name='myInteger',
        base=xsdInteger,
        facets=[xsdRestrictionMinIncluse(value="10000"),
                xsdRestrictionMaxIncluse(value="99999")])
    xsd_el = el.xsd()
    print(tostring(xsd_el))

    el = xsdSimpleType.restriction(name='SKU',
        base=xsdString,
        facets=[xsdRestrictionPattern(value="\d{3}-[A-Z]{2}")])
    print(tostring(el.xsd()))