import re
from model_automaton_builder import getDFAFromRegex


class DTDParser:
    linePattern = re.compile(r'(?P<elementName>\w) (?P<elementRegEx>.+)')
    element_name_group = "elementName"
    element_regex_group = "elementRegEx"

    def __init__(self, dtd_path):
        self.element_dfa_dict = None
        self.dtd_path = dtd_path

    def isWellFormed(self)-> bool:

        dtd_file = open(self.dtd_path)
        well_formed = True
        element_dfa_dict = {}
        for line in dtd_file:
            match = DTDParser.linePattern.match(line)
            if match is None:
                well_formed = False
                break

            element_name = match.group(DTDParser.element_name_group)
            element_regex = match.group(DTDParser.element_regex_group)
            element_dfa = getDFAFromRegex(element_regex)
            if element_dfa is None:
                well_formed = False
                break
            element_dfa_dict[element_name] = element_dfa
        if well_formed:
            self.element_dfa_dict = element_dfa_dict
        return well_formed

    def isValidElement(self, element_name, children: str):
        if element_name not in self.element_dfa_dict:
            return None
        return self.element_dfa_dict[element_name].match(children)