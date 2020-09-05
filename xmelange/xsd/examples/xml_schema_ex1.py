"""
Recommended read: https://www.w3.org/TR/xmlschema-0/

Examples are mostly taken from this extensive description of xsd
"""

from xmelange.xsd.simple_types import *
from xmelange.xsd.complex_types import *
from xmelange.xsd.builtin_simple_types import *
from xmelange.xsd.utils import tostring


def build_ItemsType():
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
    return ItemsType


def build_UsAddressType():
    sequence = xsdSequence(elements=[
        xsdElement(name='name', type='string'),
        xsdElement(name='street', type='string'),
        xsdElement(name='city', type='string'),
        xsdElement(name='state', type='string'),
        xsdElement(name='zip', type='decimal')])
    UsAddressType = xsdComplexType(name='USAddress',
                                   sequence=sequence,
                                   attributes=[xsdAttribute(name="country", type="NMTOKEN")])
    return UsAddressType


def build_PurchaseOrderType(UsAddressType, ItemsType):
    sequence = xsdSequence(elements=[
        xsdElement(name='shipTo', type=UsAddressType),
        xsdElement(name='billto', type=UsAddressType),
        xsdElement(ref='comment', minOccurs='0'),
        xsdElement(name='items', type=ItemsType)
    ])
    PurchaseOrderType = xsdComplexType(name='PurchaseOrderType',
                                       sequence=sequence,
                                       attributes=[xsdAttribute(name='orderDate', type='date')])
    return PurchaseOrderType


def build_myIntegerType():
    return xsdSimpleType.restriction(name='myInteger',
                                     base=xsdInteger,
                                     facets=[xsdRestrictionMinIncluse(value="10000"),
                                             xsdRestrictionMaxIncluse(value="99999")])


def build_SKUType():
    return xsdSimpleType.restriction(name='SKU',
                                     base=xsdString,
                                     facets=[xsdRestrictionPattern(value="\d{3}-[A-Z]{2}")])


def main():
    print('myInteger type:')
    myIntegerType = build_myIntegerType()
    print(tostring(myIntegerType.xsd()))

    print('SKU type:')
    SKUType = build_SKUType()
    print(tostring(SKUType.xsd()))

    print('Items type:')
    ItemsType = build_ItemsType()
    print(tostring(ItemsType.xsd()))

    print('UsAddress type:')
    UsAddressType = build_UsAddressType()
    print(tostring(UsAddressType.xsd()))

    print('PurchaseOrder type')
    PurchaseOrderType = build_PurchaseOrderType(UsAddressType, ItemsType)
    print(tostring(PurchaseOrderType.xsd()))


if __name__ == '__main__':
    main()
