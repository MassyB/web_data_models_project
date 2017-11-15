from parser_xml_form_checker import XMLParser
from parser_dtd_form_checker import DTDParser

xml_file_path = "example.xml"
dtd_file_path = "example.dtd"


xml_parser = XMLParser(xml_file_path)
xml_is_well_formed= xml_parser.isWellFormed()
if not xml_is_well_formed:
    print("xml not well-formed")
else:
    print("xml well-formed")

dtd_parser = DTDParser(dtd_file_path)
dtd_is_well_formed = dtd_parser.isWellFormed()

if not dtd_is_well_formed:
    print("dtd not well-formed")
else:
    print("dtd well-formed")

is_valid = xml_parser.isValid(dtd_parser)

if is_valid:
    print("valid")
else:
    print("valid")


