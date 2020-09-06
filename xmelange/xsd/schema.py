from xmelange.xsd.elements import Xsd


class XsdSchema(Xsd):

    tag = 'schema'

    def __init__(self):
        super().__init__()
        self.elements = []

    def append_node(self, element):
        self.elements.append(element)
