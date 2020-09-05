"""
Complex types - in contrast to simple types - allow elements in their content
and can have attributes
"""

from xmelange.xsd.elements import xsd, xsdElement


class xsdAttribute(xsd):
    tag = 'attribute'


class xsdSequence(xsd):
    tag = 'sequence'

    def __init__(self, elements):
        super().__init__(name=None, type=None)
        self.elements = elements

    def xsd(self, parent=None):
        sequence_element = super().xsd(parent=parent)
        for element in self.elements:
            element.xsd(parent=sequence_element)
        return sequence_element


class xsdComplexType(xsdElement):
    tag = 'complexType'

    def __init__(self, name, sequence=None, attributes=None, type_prefix=None):
        super().__init__(name=name, type=None)
        self.sequence = sequence
        self.attributes = attributes or []
        self.type_prefix = type_prefix

    def xsd(self, parent=None):
        element = super().xsd(parent=parent)
        if self.sequence is not None:
            self.sequence.xsd(parent=element)
        for attribute in self.attributes:
            attribute.xsd(parent=element)
        return element


class xsdSequenceBuilder:

    def __init__(self, host_builder=None):
        self._sequence = None
        self._elements = []
        self._host_builder = host_builder

    def build(self):
        self._sequence = xsdSequence(elements=self._elements)
        if self._host_builder is None:
            return self._sequence
        return self._host_builder

    def element(self, **kwargs):
        self._elements.append(xsdElement(**kwargs))
        return self

    @property
    def sequence(self):
        return self._sequence


class xsdComplexTypeBuilder:

    def __init__(self):
        self._name = None
        self._sequence_builder = None
        self._attributes = []
        self._type_prefix = None

    def build(self):
        return xsdComplexType(name=self._name,
                              sequence=self._sequence_builder.sequence if self._sequence_builder is not None else None,
                              attributes=self._attributes,
                              type_prefix=self._type_prefix)

    def name(self, name):
        self._name = name
        return self

    def attribute(self, **kwargs):
        self._attributes.append(xsdAttribute(**kwargs))
        return self

    def sequence(self):
        self._sequence_builder = xsdSequenceBuilder(host_builder=self)
        return self._sequence_builder
