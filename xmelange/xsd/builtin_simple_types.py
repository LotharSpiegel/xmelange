from xmelange.xsd.elements import XsdElement


class XsdBuiltinSimpleType(XsdElement):
    pass


class XsdBoolean(XsdBuiltinSimpleType):
    tag = 'boolean'


class XsdInteger(XsdBuiltinSimpleType):
    tag = 'integer'


class XsdPositiveInteger(XsdBuiltinSimpleType):
    tag = 'positiveInteger'


class XsdString(XsdBuiltinSimpleType):
    tag = 'string'
