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

    def isWellFormed(self)-> bool:
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

    def isValid(self, dtd_parser) -> bool:
        return self.isValidNode(self.xml_tree.getRoot(), dtd_parser)

    def isValidNode(self, node, dtd_parser) -> bool:
        """check the validity of tree using recursion"""
        if node.isLeaf():
            return dtd_parser.isValidElement(node.getName(), "")
        else:
            # get all the children
            children = node.getChildren()
            # if one child is not valid  then the element is not valid too

            for child in children:

                if not self.isValidNode(child, dtd_parser):
                    return False

            # verify if the element is valid
            children_string = node.getChildrenAsString()
            return dtd_parser.isValidElement(node.getName(), children_string)