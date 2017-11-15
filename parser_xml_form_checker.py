import re
from model_xml_element import XMLElement
from model_stack import Stack
from model_xml_tree import XMLTree


class XMLParser:
    # regular expression for the xml line
    linePattern = re.compile(r'(?P<opening>[01]) (?P<elementName>[\w\d]+)')
    openingGroup = "opening"
    elementNameGroup = "elementName"

    def __init__(self, xml_path: str):
        self.xml_tree = None
        self.xml_path = xml_path

    def isWellFormed(self):
        wellFormed = True
        stack = Stack()

        xmlFile = open(self.xml_path)
        for line in xmlFile:
            match = XMLParser.linePattern.match(line)

            if match is None:
                wellFormed = False
                break

            opening = match.group(XMLParser.openingGroup)
            elementName = match.group(XMLParser.elementNameGroup)

            xmlElement = XMLElement(opening, elementName)

            if xmlElement.isOpening():
                stack.push(xmlElement)

            else:
                # closing element encountered
                if not stack.isEmpty() and stack.last().isClosedBy(xmlElement):
                    lastXMLNode = stack.pop()
                    # update the parent of the element
                    lastXMLNode.setParent(stack.last())
                else:
                    wellFormed = False
                    break

        if not stack.isEmpty():
            wellFormed = False

        if wellFormed:
            # update the xml_tree
            self.xml_tree = XMLTree(lastXMLNode)

        return wellFormed
