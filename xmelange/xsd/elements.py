from lxml import etree


class xmlNamespace:

    xsd_prefix = 'xsd'

    nsmap = {
        xsd_prefix: 'http://www.w3.org/2001/XMLSchema',
        # 'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
    }


class xsd(xmlNamespace):

    tag = None
    name = None
    xsd_type = None

    def build_tag(self, tag_name, prefix=None):
        if prefix is None:
            return tag_name
        return etree.QName(prefix, tag_name)

    def build_xsd_tag(self, type):
        return etree.QName(self.nsmap[self.xsd_prefix], type)

    def build_xsd_type(self, type_name):
        return '{xsd_prefix}:{type_name}'.format(
            xsd_prefix=self.xsd_prefix, type_name=type_name)

    def xsd_attributes(self):
        attrib = {}
        if self.name is not None:
            attrib['name'] = self.name
        if self.xsd_type is not None:
            attrib['type'] = self.build_xsd_type(self.xsd_type)
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
        tag = self.build_tag(tag_name=self.name)
        if parent is None:
            el = etree.Element(tag, nsmap=self.nsmap)
        else:
            el = etree.SubElement(parent, tag)
        if value is not None:
            el.text = value
        return el


class xsdElement(xsd):

    tag = 'element'

    def __init__(self, name, xsd_type):
        self.name = name
        self.xsd_type = xsd_type



class xsdAttribute:

    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value


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