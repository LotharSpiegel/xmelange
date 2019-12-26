"""
Complex types - in contrast to simple types - allow elements in their content
and can have attributes
"""

from lxml import etree

from elements import xsd, xsdElement


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


def tostring(element, pretty_print=True, xml_declaration=True, encoding='UTF-8'):
    return etree.tostring(
            element,
            pretty_print=pretty_print,
            xml_declaration=xml_declaration,
            encoding=encoding).decode()


if __name__ == '__main__':

    from simple_types import xsdSimpleType, xsdRestriction, xsdRestrictionMaxExclusive
    from builtin_simple_types import xsdPositiveInteger

    quantityRestriction = xsdRestriction(
        base=xsdPositiveInteger,
        facets=[xsdRestrictionMaxExclusive(value='100')]
    )
    quantityInlineType = xsdSimpleType(
        name=None,
        restriction=quantityRestriction
    )
    sequence = xsdSequence(elements=[
        xsdElement(name='productName', type='string'),
        xsdElement(name='quantity', type=quantityInlineType)
    ])
    itemElementInlineType = xsdComplexType(
        name=None, # itemElement has inline type (i.e. anonymous type)
        sequence=sequence,
        attributes=[xsdAttribute(name='partNum', type='SKU',
            use='required')]
    )
    itemElement = xsdElement(name='item', type=itemElementInlineType,
        minOccurs='0', maxOccurs='unbounded')
    sequence = xsdSequence(elements=[
        itemElement
    ])
    Items = xsdComplexType(name='Items',
        sequence=sequence)

    xsd_el = Items.xsd()
    print(tostring(xsd_el))

    # sequence = xsdSequence(elements=[
    #     xsdElement(name='name', type='string'),
    #     xsdElement(name='street', type='string'),
    #     xsdElement(name='city', type='string'),
    #     xsdElement(name='state', type='string'),
    #     xsdElement(name='zip', type='decimal')])
    # UsAddress = xsdComplexType(name='USAddress',
    #     sequence=sequence,
    #     attributes=[xsdAttribute(name="country", type="NMTOKEN")])
    # xsd_el = UsAddress.xsd()
    # print(tostring(xsd_el))

    # sequence = xsdSequence(elements=[
    #     xsdElement(name='shipTo', type=UsAddress),
    #     xsdElement(name='billto', type=UsAddress),
    #     xsdElement(ref='comment', minOccurs='0'),
    #     xsdElement(name='items', type=Items)
    # ])
    # PurchaseOrderType = xsdComplexType(name='PurchaseOrderType',
    #         sequence=sequence,
    #         attributes=[xsdAttribute(name='orderDate', type='date')])
    # xsd_el = PurchaseOrderType.xsd()
    # print(tostring(xsd_el))