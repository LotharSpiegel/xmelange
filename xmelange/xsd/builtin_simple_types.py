from xmelange.xsd.elements import xsdElement


class xsdBuiltinSimpleType(xsdElement):
    pass


class xsdBoolean(xsdBuiltinSimpleType):
    tag = 'boolean'


class xsdInteger(xsdBuiltinSimpleType):
    tag = 'integer'


class xsdPositiveInteger(xsdBuiltinSimpleType):
    tag = 'positiveInteger'


class xsdString(xsdBuiltinSimpleType):
    tag = 'string'