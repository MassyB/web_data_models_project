import re
from model_automaton import Automaton
from model_automaton import O_PARENTHESIS, C_PARENTHESIS, STAR, PLUS, OPTIONAL



def addAndSymbols(regex: str) -> str:
    tr_regex = ""
    while tr_regex != regex:
        tr_regex = regex
        regex = re.sub(r'([\w+?*)])([\w(])', r'\1&\2', regex)
    return regex


def infixToPostfix(regex: str) -> str:
    pass


def isValidRegex(regex: str, languageSymbols: set):
    return areValidParenthesis(regex) and \
           areValidQuantifiers(regex) and \
           areValidSymbols(regex) and \
           areLanguageSymbols(regex, languageSymbols)


def areValidSymbols(regex: str):
    pattern = re.compile(r'(\w).*\1')
    return pattern.search(regex) is None


def areValidQuantifiers(regex: str):
    pattern = re.compile(r'(?<=[^\w)])[?*+]|^[?+*]')
    return pattern.search(regex) is None


def areLanguageSymbols(regex: str, languageSymboles: set):
    usedSymbols = set(re.sub(r'[?+*()]', '', regex))
    return languageSymboles.intersection(usedSymbols) == usedSymbols


def getClosedParenthesisIndex(regex: str, openParenthesisIndex):
    i = openParenthesisIndex + 1
    while i < len(regex):
        symbol = regex[i]
        if symbol == C_PARENTHESIS:
            return i

        elif symbol == O_PARENTHESIS:
            j = getClosedParenthesisIndex(regex, i)
            if j == -1:
                return -1
            i = j + 1
        else:
            i += 1
    return -1


def areValidParenthesis(regex: str):
    i = 0
    while i < len(regex):
        symbol = regex[i]
        if symbol == O_PARENTHESIS:
            j = getClosedParenthesisIndex(regex, i)
            if j - i <= 1:
                return False
            else:
                i = j + 1
        elif symbol == C_PARENTHESIS:
            return False
        else:
            i += 1
    return True
