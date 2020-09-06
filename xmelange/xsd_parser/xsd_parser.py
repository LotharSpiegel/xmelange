from lxml import etree

from xmelange.xsd.builtin_simple_types import XsdBoolean, XsdPositiveInteger, XsdInteger, XsdString
from xmelange.xsd.elements import XmlNameSpace, XsdElement
from xmelange.xsd.schema import XsdSchema
from xmelange.xsd.simple_types import XsdSimpleType, XsdRestriction, \
    XsdRestrictionPattern, XsdRestrictionMinInclusive, XsdRestrictionMaxInclusive, \
    XsdRestrictionMinExclusive, XsdRestrictionMaxExclusive

TAG_TO_CLASS_MAP = {
    'boolean': XsdBoolean,
    'integer': XsdInteger,
    'positiveinteger': XsdPositiveInteger,
    'string': XsdString,
    'pattern': XsdRestrictionPattern,
    'mininclusive': XsdRestrictionMinInclusive,
    'maxinclusive': XsdRestrictionMaxInclusive,
    'minexclusive': XsdRestrictionMinExclusive,
    'maxexclusive': XsdRestrictionMaxExclusive,
}


class XsdParser:
    """
        Base class to parse (i.e. deserialize) an xml schema (xsd file) into an AST represented
        by python classes.
    """

    def __init__(self, name_space=XmlNameSpace):
        self._name_space = name_space
        self._tag_to_class_map = dict(TAG_TO_CLASS_MAP)

    def qname(self, tag):
        if "{" in tag:
            return etree.QName(tag)
        if ":" in tag:
            ns, tag = tag.split(":")
            return etree.QName(ns, tag)
        return etree.QName(self._name_space.xsd_prefix, tag)

    def tag_to_qname(self, element):
        return self.qname(element.tag)

    def tag_localname(self, element):
        # todo: add null checks
        qname = self.tag_to_qname(element)
        return qname.localname.lower()

    def get_class_by_tag(self, tag):
        return self._tag_to_class_map.get(tag.lower())

    def parse(self, xml):
        """Parses xsd (xml schema)
            :param xml: string containing the xsd
        """

        root = etree.fromstring(xml)
        return self.parse_node(root)

    def parse_not_implemented(self, element_tag):
        raise Exception(f"parse_{element_tag} not implemented")

    def parse_node(self, node):
        element_tag = self.tag_localname(node)
        print("parse_node, element_tag: " + element_tag)
        method_name = f'parse_{element_tag}'
        method = getattr(self, method_name, None)
        if method is None:
            return self.parse_not_implemented(element_tag)
        else:
            return method(node)

    def parse_schema(self, node):
        schema = XsdSchema()
        for child in node:
            schema.append_node(self.parse_node(child))
        return schema

    def parse_element(self, node):
        # todo: handle: ref="", minOccurs=""
        name = node.get("name")
        type_ = node.get("type")
        return XsdElement(name=name,
                          tpye=type_)  # todo: pass parent = ..

    def parse_simpletype(self, node):
        name = node.get("name")
        restriction_child = node.find("xsd:restriction", namespaces=self._name_space.nsmap)
        if restriction_child is not None:
            restriction = self.parse_restriction(restriction_child)
            return XsdSimpleType(name=name, restriction=restriction)
        return None

    def parse_restriction(self, node):
        base_attr = node.get("base")
        base_qname = self.qname(base_attr)  # or wrap qname in constructor of XsdRestriction ?
        base = self.get_class_by_tag(base_qname.localname)
        facets = []
        for facet_node in node:
            facet = self.parse_facet(facet_node)
            if facet is not None:
                facets.append(facet)
        return XsdRestriction(base=base, facets=facets)

    def parse_facet(self, node):
        facet_type = self.get_class_by_tag(self.tag_localname(node))
        if facet_type is None:
            return None
        return facet_type(value=node.get("value"))
