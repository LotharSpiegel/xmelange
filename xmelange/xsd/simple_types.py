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
    <xsd:pattern value="\\d{3}-[A-Z]{2}"/>
  </xsd:restriction>
</xsd:simpleType>

! Simple types cannot have attributes
"""

from xmelange.xsd.elements import Xsd, XsdElement


class XsdRestrictionFacet(Xsd):
    tag = None

    def __init__(self, value):
        super().__init__()
        self.value = value

    def xsd_attributes(self):
        return {
            'value': self.value
        }


class XsdRestrictionPattern(XsdRestrictionFacet):
    tag = 'pattern'


class XsdRestrictionMinInclusive(XsdRestrictionFacet):
    tag = 'minInclusive'


class XsdRestrictionMaxInclusive(XsdRestrictionFacet):
    tag = 'maxInclusive'


class XsdRestrictionMinExclusive(XsdRestrictionFacet):
    tag = 'minExclusive'


class XsdRestrictionMaxExclusive(XsdRestrictionFacet):
    tag = 'maxExclusive'


class XsdRestriction(Xsd):
    tag = 'restriction'

    def __init__(self, base, facets):
        super().__init__()
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


class XsdSimpleType(XsdElement):
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
        xsd_restriction = XsdRestriction(base=base, facets=facets)
        simple_type = XsdSimpleType(name=name, restriction=xsd_restriction)
        return simple_type
