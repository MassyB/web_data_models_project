from parser_xml_form_checker import XMLFormParser
import sys

xmlFileArgIndex = 1

xmlFilePath = sys.argv[xmlFileArgIndex]
xmlFormParser = XMLFormParser()

xmlFormParser.checkWellFormedness(xmlFilePath)