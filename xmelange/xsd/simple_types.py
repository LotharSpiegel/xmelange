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

from xmelange.xsd.builtin_simple_types import *
from xmelange.xsd.elements import xsd, xsdElement


class xsdRestrictionFacet(xsd):
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


class xsdRestrictionMinExclusive(xsdRestrictionFacet):
    tag = 'minExclusive'


class xsdRestrictionMaxExclusive(xsdRestrictionFacet):
    tag = 'maxExclusive'


class xsdRestriction(xsd):

    tag = 'restriction'

    def __init__(self, base, facets):
        self.base = base
        self.facets = facets

    def xsd_attributes(self):
        attrib = super().xsd_attributes()
        if hasattr(self.base, 'tag'):
            attrib['base'] = self.build_xsd_type(self.base.tag)
        else:
            attrib['base'] = self.base
        return attrib

    def xsd(self, parent=None):
        el = super().xsd(parent=parent)
        for facet in self.facets:
            facet.xsd(parent=el)
        return el


class xsdSimpleType(xsdElement):

    tag = 'simpleType'

    def __init__(self, name, restriction):
        super().__init__(name=name, type=None)
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
