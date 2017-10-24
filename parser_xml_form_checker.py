import re
from model_xml_element import XMLElement
from model_stack import Stack

class XMLFormParser:

    # regular expression for the xml line
    linePattern = re.compile(r'(?P<opening>[01]) (?P<elementName>[\w\d]+)')
    openingGroup = "opening"
    elementNameGroup = "elementName"

    def checkWellFormedness(self, xml_path : str):
        # open a file
        # extrcat the lines
        # construct an xml_line on the rush
        # stack if it's a zero
        # if it's not check for the correspondig element

        wellFormed = True
        stack = Stack()

        xmlFile = open(xml_path)
        for line in xmlFile:
            match = XMLFormParser.linePattern.match(line)

            if match is None:
                wellFormed = False
                break

            opening = match.group(XMLFormParser.openingGroup)
            elementName = match.group(XMLFormParser.elementNameGroup)

            xmlElement = XMLElement(opening, elementName)

            if xmlElement.isOpening():
                stack.push(xmlElement)
            else:
                # closing element encountered
                if stack.last().isClosedBy(xmlElement):
                    wellFormedXmlNode = stack.pop()
                    # update the parent of the element
                    wellFormedXmlNode.setParent(stack.last())
                else:
                    wellFormed = False

        if not stack.isEmpty():
            wellFormed = False

        if wellFormed:
            print("XML well-formed")
            # return the Tree root
            return wellFormedXmlNode
        else:
            print("XML Not well-formed")