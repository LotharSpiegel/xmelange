import pytest

from xmelange.xsd_parser.xsd_parser import XsdParser

XSD_SCHEMA = '<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">'
XSD_SCHEMA_CLOSE = '</xsd:schema>'


def add_xsd_namespace(xml):
    return f"{XSD_SCHEMA}{xml}{XSD_SCHEMA_CLOSE}"


SIMPLE_TYPE_RESTRICTION_SAMPLE_XML = add_xsd_namespace("""
            <xsd:simpleType>
                <xsd:restriction base="xsd:positiveInteger">
                    <xsd:maxExclusive value="100"/>
                </xsd:restriction>
            </xsd:simpleType>
        """)


@pytest.fixture
def simple_type_restriction_sample_schema():
    return XsdParser().parse(SIMPLE_TYPE_RESTRICTION_SAMPLE_XML)


class TestXsdParser_SimpleTypeParsing:

    def test_simpleType_basics(self, simple_type_restriction_sample_schema):
        schema = simple_type_restriction_sample_schema
        assert len(schema.elements) == 1
        simple_type_node = schema.elements[0]
        assert simple_type_node.tag == "simpleType"
        assert simple_type_node.name is None

    def test_simpleType_restriction_basics(self, simple_type_restriction_sample_schema):
        simple_type_node = simple_type_restriction_sample_schema.elements[0]
        assert simple_type_node.restriction is not None
        assert simple_type_node.restriction.tag == "restriction"
        assert simple_type_node.restriction.base.tag == "positiveInteger"
