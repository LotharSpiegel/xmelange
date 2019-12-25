import pytest

from xmelange.xsd.xml_builder import XmlBuilder


class TestXmlBuilder:

    @classmethod
    def setup_class(cls):
        cls.builder = XmlBuilder()

    def test_build_xsd_tag(self):
        tag = self.builder.build_xsd_tag(type='element')
        print(tag)

    def test_build_element(self):
        tag = self.builder.build_xsd_tag(type='element')
        element = self.builder.build_element(tag=tag)
        print(element)

    def test_tostring(self):
        tag = self.builder.build_xsd_tag(type='element')
        element = self.builder.build_element(tag=tag)
        print(self.builder.tostring(element))