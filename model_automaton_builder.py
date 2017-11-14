import re
from model_automaton import Automaton
from model_automaton import O_PARENTHESIS, C_PARENTHESIS, STAR, PLUS, OPTIONAL
from model_stack import Stack

AND = '&'


def addAndSymbols(regex: str) -> str:
    tr_regex = ""
    while tr_regex != regex:
        tr_regex = regex
        regex = re.sub(r'([\w+?*)])([\w(])', r'\1&\2', regex)
    return regex


def infixToPostfix(regex: str) -> str:
    s = Stack()
    regex = addAndSymbols(regex)
    postfix_regex = ""
    for c in regex:
        if isSymbol(c):
            postfix_regex += c
        elif isOperator(c):
            if isQuantifier(c):
                s.push(c)
            else:
                # it's the and operator
                while not s.isEmpty() and isQuantifier(s.last()):
                    postfix_regex += s.pop()
                s.push(c)
        elif c == O_PARENTHESIS:
            s.push(c)
        elif c == C_PARENTHESIS:
            while not s.isEmpty() and s.last() != O_PARENTHESIS:
                postfix_regex += s.pop()
            if not s.isEmpty():
                s.pop()
    while not s.isEmpty():
        postfix_regex += s.pop()
    return postfix_regex


def isQuantifier(c: str) -> bool:
    return re.match(r'[+*?]', c) is not None


def isOperator(c: str) -> bool:
    return re.match(r'[?+*&]', c) is not None


def isSymbol(c: str) -> bool:
    return re.match(r'[a-zA-Z]', c) is not None


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
