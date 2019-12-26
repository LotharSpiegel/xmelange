from lxml import etree


class XmlBuilder:

    xsd_prefix = 'xsd'
    soap_prefix = 'soap'

    def __init__(self):
        self.setup_basic_namespaces()

    def set_xml_namespace(self, key, url):
        self.nsmap[key] = url

    def setup_basic_namespaces(self):
        self.nsmap = {}
        self.set_xml_namespace(self.xsd_prefix, "http://www.w3.org/2001/XMLSchema")
        self.set_xml_namespace(self.soap_prefix, "http://schemas.xmlsoap.org/soap/envelope/")

    def build_xsd_tag(self, type):
        return etree.QName(self.nsmap[self.xsd_prefix], type)

    def build_element(self, tag, parent=None):
        if parent is None:
            return etree.Element(tag, nsmap=self.nsmap)
        else:
            return etree.SubElement(parent, tag)

    def buld_xsd_element(self, name, type, value, parent=None):
        tag = self.build_xsd_tag(type='element')
        el = self.build_element(tag=tag, parent=parent)
        el.text = value
        return el

    def tostring(self, element, pretty_print=True, xml_declaration=True, encoding='UTF-8'):
        return etree.tostring(
            element,
            pretty_print=pretty_print,
            xml_declaration=xml_declaration,
            encoding=encoding)