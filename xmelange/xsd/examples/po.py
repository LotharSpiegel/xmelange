"""
Recommended read: https://www.w3.org/TR/xmlschema-0/

Examples are mostly taken from this extensive description of xsd
"""

from xmelange.xsd.simple_types import *
from xmelange.xsd.complex_types import *
from xmelange.xsd.builtin_simple_types import *

quantityInlineType = xsdSimpleType(
    name=None,
    restriction=xsdRestriction(
        base=xsdPositiveInteger,
        facets=[xsdRestrictionMaxExclusive(value='100')]
    )
)
sequence = xsdSequence(elements=[
    xsdElement(name='productName', type='string'),
    xsdElement(name='quantity', type=quantityInlineType)
])
itemElementInlineType = xsdComplexType(
    name=None,  # itemElement has inline type (i.e. anonymous type)
    sequence=sequence,
    attributes=[xsdAttribute(name='partNum', type='SKU',
                             use='required')]
)
itemElement = xsdElement(name='item', type=itemElementInlineType,
                         minOccurs='0', maxOccurs='unbounded')
sequence = xsdSequence(elements=[
    itemElement
])
ItemsType = xsdComplexType(name='Items',
                           sequence=sequence)

sequence = xsdSequence(elements=[
    xsdElement(name='name', type='string'),
    xsdElement(name='street', type='string'),
    xsdElement(name='city', type='string'),
    xsdElement(name='state', type='string'),
    xsdElement(name='zip', type='decimal')])
UsAddressType = xsdComplexType(name='USAddress',
                               sequence=sequence,
                               attributes=[xsdAttribute(name="country", type="NMTOKEN")])

PurchaseOrderType = \
    xsdComplexTypeBuilder().name('PurchaseOrderType') \
        .sequence() \
        .element(name='shipTo', type=UsAddressType) \
        .element(name='billto', type=UsAddressType) \
        .element(ref='comment', minOccurs='0') \
        .element(name='items', type=ItemsType) \
        .build() \
        .attribute(name='orderDate', type='date') \
        .build()


# def build_myIntegerType():
#    return xsdSimpleType.restriction(name='myInteger',
#                                     base=xsdInteger,
#                                     facets=[xsdRestrictionMinIncluse(value="10000"),
#                                             xsdRestrictionMaxIncluse(value="99999")])


SKUType = xsdSimpleType.restriction(name='SKU',
                                     base=xsdString,
                                     facets=[xsdRestrictionPattern(value="\d{3}-[A-Z]{2}")])


def print_xsd(heading, xsd_type):
    print(heading)
    print(xsd_type)


def main():
    # print('myInteger type:')
    # myIntegerType = build_myIntegerType()
    # print(tostring(myIntegerType.xsd()))

    print_xsd('SKUType:', SKUType)
    print_xsd('ItemsType:', ItemsType)
    print_xsd('UsAddressType:', UsAddressType)
    print_xsd('PurchaseOrderType:', PurchaseOrderType)


if __name__ == '__main__':
    main()
