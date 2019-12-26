from elements import xsdElement


class xsdBuiltinSimpleType(xsdElement):
    pass


class xsdBoolean(xsdBuiltinSimpleType):
    tag = 'boolean'


class xsdInteger(xsdBuiltinSimpleType):
    tag = 'integer'


class xsdString(xsdBuiltinSimpleType):
    tag = 'string'