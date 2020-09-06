"""
Recommended read: https://www.w3.org/TR/xmlschema-0/

Examples are mostly taken from this extensive description of xsd
"""

from xmelange.xsd.simple_types import *
from xmelange.xsd.complex_types import *
from xmelange.xsd.builtin_simple_types import *

quantityInlineType = XsdSimpleType(
    name=None,
    restriction=XsdRestriction(
        base=XsdPositiveInteger,
        facets=[XsdRestrictionMaxExclusive(value='100')]
    )
)

# itemElement has inline type (i.e. anonymous type)
itemElementInlineType = XsdComplexTypeBuilder() \
    .name(None) \
    .sequence() \
    .element(name='productName', type='string') \
    .element(name='quantity', type=quantityInlineType) \
    .build_sequence() \
    .attribute(name='partNum', type='SKU', use='required') \
    .build()

ItemsType = XsdComplexTypeBuilder().name('Items') \
    .sequence() \
    .element(name='item', type=itemElementInlineType,
             minOccurs='0', maxOccurs='unbounded') \
    .build_sequence() \
    .build()

UsAddressType = XsdComplexTypeBuilder().name('USAddress') \
    .sequence() \
    .element(name='name', type='string') \
    .element(name='street', type='string') \
    .element(name='city', type='string') \
    .element(name='state', type='string') \
    .element(name='zip', type='decimal') \
    .build_sequence() \
    .attribute(name="country", type="NMTOKEN") \
    .build()

PurchaseOrderType = \
    XsdComplexTypeBuilder().name('PurchaseOrderType') \
        .sequence() \
        .element(name='shipTo', type=UsAddressType) \
        .element(name='billto', type=UsAddressType) \
        .element(ref='comment', minOccurs='0') \
        .element(name='items', type=ItemsType) \
        .build_sequence() \
        .attribute(name='orderDate', type='date') \
        .build()

# def build_myIntegerType():
#    return xsdSimpleType.restriction(name='myInteger',
#                                     base=xsdInteger,
#                                     facets=[xsdRestrictionMinIncluse(value="10000"),
#                                             xsdRestrictionMaxIncluse(value="99999")])


SKUType = XsdSimpleType.restriction(name='SKU',
                                    base=XsdString,
                                    facets=[XsdRestrictionPattern(value="\d{3}-[A-Z]{2}")])


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
