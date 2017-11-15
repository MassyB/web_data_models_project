from model_xml_element import XMLElement


class XMLTree:
    def __init__(self, root):
        self.root = root

    def getRoot(self) -> 'XMLElement':
        return self.root
