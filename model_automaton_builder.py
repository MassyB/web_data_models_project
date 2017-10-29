import re
from model_automaton import Automaton
from model_automaton import O_PARENTHESIS, C_PARENTHESIS, STAR, PLUS, OPTIONAL


def makeAutomaton(regex: str, languageSymbols: set) -> 'Automaton':
    if not isValidRegex(regex, languageSymbols):
        return None
    regexWithParenthesis = transformRegex(regex)
    automaton = buildAutomaton(regexWithParenthesis)
    return automaton


def buildAutomaton(regex: str) -> 'Automaton':
    """ the regex is a valid non empty regular expression """
    i = 0
    automaton = Automaton()
    subAutomaton = None
    while i < len(regex):
        symbol = regex[i]
        if symbol.isalpha():
            automaton.addTransition(symbol)
            i += 1

        elif symbol == O_PARENTHESIS:

            closedPraenthesisIndex = getClosedParenthesisIndex(regex, i)
            subRegex = regex[i + 1: closedPraenthesisIndex]
            subAutomaton = buildAutomaton(subRegex)
            i = closedPraenthesisIndex + 1

        elif symbol == STAR or symbol == PLUS or symbol == OPTIONAL:
            subAutomaton.iterateQuantifier(symbol)
            if automaton.isEmpty():
                automaton = subAutomaton
            else:
                automaton.concatenateWith(subAutomaton)
            subAutomaton = None
            i += 1

    if subAutomaton is not None:
        if automaton.isEmpty():
            automaton = subAutomaton
        else:
            automaton.concatenateWith(subAutomaton)

    return automaton


def transformRegex(regex: str) -> str:
    """put brackets around quantified symbols, to simplify the DFN construction"""
    return re.sub(r'(\w)([?*+])', r'(\1)\2', regex)


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
