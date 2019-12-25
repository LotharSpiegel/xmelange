from lxml import etree


class XmlBuilder:

    xsd_prefix = 'xsd'
    soap_prefix = 'soap'
    add_nsmap_to_elements = True

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

    def build_element(self, tag):
        if self.add_nsmap_to_elements:
            nsmap = self.nsmap
        else:
            nsmap = None
        return etree.Element(tag, nsmap=nsmap)

    def tostring(self, element, pretty_print=True, xml_declaration=True, encoding='UTF-8'):
        return etree.tostring(
            element,
            pretty_print=pretty_print,
            xml_declaration=xml_declaration,
            encoding=encoding)