class XMLElement:
    openingSymbole = "0"
    closingSymbole = "1"

    def __init__(self, opening, elementName, parent=None, children=list()):
        self.opening = opening
        self.elementName = elementName
        self.parent = parent
        self.children = children

    def setParent(self, parentNode: 'XMLElement'):
        if parentNode is not None:
            self.parent = parentNode
            parentNode.getChildren().append(self)

    def isOpening(self):
        return self.opening == XMLElement.openingSymbole

    def isClosedBy(self, elem: 'XMLElement'):
        return self.isOpening() and elem.isClosing() and (self.elementName == elem.getName())

    def isClosing(self):
        return not self.isOpening()

    def getName(self):
        return self.elementName

    def getChildren(self):
        return self.children

    def getChildrenAsString(self):
        children_string = ""
        for childe in self.children:
            children_string += childe.getName()
        return children_string
