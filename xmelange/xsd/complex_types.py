"""
Complex types - in contrast to simple types - allow elements in their content
and can have attributes
"""

from lxml import etree

from xmelange.xsd.elements import xsd, xsdElement


class xsdAttribute(xsd):
    tag = 'attribute'


class xsdSequence(xsd):
    tag = 'sequence'

    def __init__(self, elements):
        super().__init__(name=None, type=None)
        self.elements = elements

    def xsd(self, parent=None):
        sequence_element = super().xsd(parent=parent)
        for element in self.elements:
            element.xsd(parent=sequence_element)
        return sequence_element


class xsdComplexType(xsdElement):
    tag = 'complexType'

    def __init__(self, name, sequence, attributes=None, type_prefix=None):
        super().__init__(name=name, type=None)
        self.sequence = sequence
        self.attributes = attributes or []
        self.type_prefix = type_prefix

    def xsd(self, parent=None):
        element = super().xsd(parent=parent)
        self.sequence.xsd(parent=element)
        for attribute in self.attributes:
            attribute.xsd(parent=element)
        return element
