class XMLElement:

    openingSymbole = "0"
    closingSymbole = "1"

    def __init__(self, opening, elementName, parent=None, children=list()):
        self.opening = opening
        self.elementName = elementName
        self.parent = parent
        self.children = children
        self.nbWellFormed = 0 # the number of well-formed children

    def toString(self):
        return self.elementName

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

    def getNbChildren(self):
        return len(self.getChildren())

    def getNbWellFormed(self):
        return self.nbWellFormed

    def incNbWellFormed(self):
        self.nbWellFormed += 1

    def isRoot(self):
        return self.parent is None

    def getParent(self):
        return self.parent

    def getAncestor(self, index):
        pass

    def getSibling(self):
        pass

    def getChild(self, index):
        pass
