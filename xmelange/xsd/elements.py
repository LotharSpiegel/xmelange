from lxml import etree


class xmlNamespace:

    xsd_prefix = 'xsd'

    nsmap = {
        xsd_prefix: 'http://www.w3.org/2001/XMLSchema',
        # 'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    }


class xsd(xmlNamespace):

    tag = None
    attrib = None
    type_prefix = xmlNamespace.xsd_prefix

    def __init__(self, **attrib):
        """attrib-dict:
            name:
            type:
            ref: reference an existing element instead of declaring a new one
        """
        self.attrib = dict(attrib)

    @staticmethod
    def build_tag(tag_name, prefix=None):
        if prefix is None:
            return tag_name
        return etree.QName(prefix, tag_name)

    def build_xsd_tag(self, type):
        return etree.QName(self.nsmap[self.xsd_prefix], type)

    def build_xsd_type(self, xsd_type):
        if xsd_type is None:
            return None
        if isinstance(xsd_type, xsdElement):
            type_name = xsd_type.name
            type_prefix = xsd_type.type_prefix
        else:
            type_name = xsd_type
            type_prefix = self.type_prefix
        if type_prefix is None:
            return type_name
        return '{type_prefix}:{type_name}'.format(
            type_prefix=type_prefix, type_name=type_name)

    def xsd_attributes(self):
        if self.attrib is None:
            return {}
        attrib = {}
        for key, value in self.attrib.items():
            if key == 'type':
                value = self.build_xsd_type(value)
            if value is None:
                continue
            attrib[key] = value
        return attrib

    def xsd(self, parent=None):
        tag = self.build_xsd_tag(type=self.tag)
        attrib = self.xsd_attributes()
        if parent is None:
            return etree.Element(tag, attrib=attrib, nsmap=self.nsmap)
        else:
            if tag is None:
                raise Exception('tag is None')
            return etree.SubElement(parent, tag, attrib=attrib)

    def xml(self, value, parent=None):
        tag = xsd.build_tag(tag_name=self.name)
        if parent is None:
            el = etree.Element(tag, nsmap=self.nsmap)
        else:
            el = etree.SubElement(parent, tag)
        if value is not None:
            el.text = value
        return el

    def __getattr__(self, key):
        if key == 'attrib' or self.attrib is None:
            raise AttributeError()
        if key in self.attrib:
            return self.attrib[key]


class xsdElement(xsd):
    tag = 'element'

    def xsd(self, parent=None):
        el = super().xsd(parent=parent)
        # handle inline types:
        if isinstance(self.type, xsdElement):
            if self.type.name is None:
                inline_type = self.type.xsd(parent=el)
        return el


def tostring(element, pretty_print=True, xml_declaration=True, encoding='UTF-8'):
    return etree.tostring(
        element,
        pretty_print=pretty_print,
        xml_declaration=xml_declaration,
        encoding=encoding).decode()


if __name__ == '__main__':
    el = xsdElement(name='comment', xsd_type='string')
    xsd_el = el.xsd()
    xml_el = el.xml(value="bla")
    print(tostring(xsd_el))
    print(tostring(xml_el))
