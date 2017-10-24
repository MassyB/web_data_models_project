from model_xml_element import XMLElement


class XMLTree:
    def __init__(self, root=None, elementNames=set()):
        self.root = root
        self.elementNames = elementNames

    def getElementNames(self):
        return self.elementNames

    def addElementName(self, elementName: str):
        self.elementNames.add(elementName)

    def setRoot(self, root: 'XMLElement'):
        self.root = root

    def getRoot(self, ) -> 'XMLElement':
        return self.root
