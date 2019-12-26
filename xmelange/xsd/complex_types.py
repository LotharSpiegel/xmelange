"""
Complex types - in contrast to simple types - allow elements in their content
and can have attributes
"""

from lxml import etree

from elements import xsdElement


class xsdAttribute(xsdElement):
    pass


class xsdSequence(xsdElement):
    tag = 'sequence'

    def __init__(self, elements):
        super().__init__(name=None, xsd_type=None)
        self.elements = elements

    def xsd(self, parent=None):
        sequence_element = super().xsd(parent=parent)
        for element in self.elements:
            element.xsd(parent=sequence_element)
        return sequence_element


class xsdComplexType(xsdElement):
    tag = 'complexType'

    def __init__(self, name, sequence, attributes, type_prefix=None):
        super().__init__(name=name, xsd_type=None)
        self.sequence = sequence
        self.type_prefix = type_prefix

    def xsd(self, parent=None):
        element = super().xsd(parent=parent)
        self.sequence.xsd(parent=element)
        return element


def tostring(element, pretty_print=True, xml_declaration=True, encoding='UTF-8'):
    return etree.tostring(
            element,
            pretty_print=pretty_print,
            xml_declaration=xml_declaration,
            encoding=encoding).decode()


if __name__ == '__main__':
    sequence = xsdSequence(elements=[
        xsdElement(name='name', xsd_type='string'),
        xsdElement(name='street', xsd_type='string'),
        xsdElement(name='city', xsd_type='string'),
        xsdElement(name='state', xsd_type='string'),
        xsdElement(name='zip', xsd_type='decimal')])
    el = xsdComplexType(name='USAddress',
            sequence=sequence,
            attributes=[xsdAttribute(name="country", xsd_type="NMTOKEN")])
    xsd_el = el.xsd()
    print(tostring(xsd_el))

    sequence = xsdSequence(elements=[
        xsdElement(name='shipTo', xsd_type=el),
        xsdElement(name='billto', xsd_type=el)])
    el = xsdComplexType(name='PurchaseOrderType',
            sequence=sequence,
            attributes=[xsdAttribute(name='orderDate', xsd_type='date')])
    xsd_el = el.xsd()
    print(tostring(xsd_el))