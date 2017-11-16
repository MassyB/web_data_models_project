from parser_xml_form_checker import XMLParser
from parser_dtd_form_checker import DTDParser


def parse(xml_file_path, dtd_file_path, verbose=True):
    xml_parser = XMLParser(xml_file_path)
    xml_is_well_formed = xml_parser.isWellFormed()
    if not xml_is_well_formed:
        if verbose:
            print("not well-formed")
            print("not valid")
        return
    else:
        if verbose:
            print("well-formed")

    dtd_parser = DTDParser(dtd_file_path)
    dtd_is_well_formed = dtd_parser.isWellFormed()

    # just in case there is an error in the DTD
    if not dtd_is_well_formed:
        if verbose:
            print("ERROR 0: BAD DTD !")
        return

    is_valid = xml_parser.isValid(dtd_parser)

    if is_valid:
        if verbose:
            print("valid")
    else:
        if verbose:
            print("not valid")