import re

class DTDFormChecker:

    ##linePattern = re.compile(r'(?P<elementName>[\w\d]+) (?P<elementRegEx>[\w\d]+)')
    ##nameGroup = "elementName"
    ##regExGroup = "elementRegEx"

    # elementNames is going to contain the allowed element names
    def __init__(self, elementNames):
        self.elementNames = elementNames

    def checkWellFormedness(self, dtdPath: str):
        pass
