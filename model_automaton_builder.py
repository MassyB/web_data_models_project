import re
from model_automaton import NFA, DFA, O_PARENTHESIS, C_PARENTHESIS, AND, EPSILON
from model_stack import Stack


def getDFAFromRegex(regex: str):
    if regex == EPSILON:
        return DFA.getTrivialDFA()

    nfa = getNFAFromRegex(regex)
    if nfa is not None:
        return nfa.toDFA()
    # there is an error in the regex (it's not a valid one)
    return None


def getNFAFromRegex(regex: str):
    """ first we will check the validity of the regex, if it's not
        the automaton won't be constructed"""
    if not isValidRegex(regex):
        return None
    postfix_regex = convertFromInfixToPostfix(addAndSymbols(regex))
    return getNFAFromPostfix(postfix_regex)


def getNFAFromPostfix(regex: str) -> 'NFA':
    """ we will use a stack which will contain automatons
        the evaluation of the regex will be the construction,
        step by step, of the automaton"""
    s = Stack()
    for c in regex:
        if isSymbol(c):
            nfa = NFA.createNFAFromLetter(c)
            s.push(nfa)

        elif isQuantifier(c):
            nfa = s.pop()
            nfa.iterateQuantifier(c)
            s.push(nfa)

        elif c == AND:
            nfa2 = s.pop()
            nfa1 = s.pop()
            nfa1.concatenateWith(nfa2)
            s.push(nfa1)
    # the final result the automaton
    nfa = s.pop()
    return nfa


def addAndSymbols(regex: str) -> str:
    tr_regex = ""
    while tr_regex != regex:
        tr_regex = regex
        regex = re.sub(r'([\w+?*)])([\w(])', r'\1&\2', regex)
    return regex


def convertFromInfixToPostfix(regex: str) -> str:
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


def isValidRegex(regex: str):
    return areValidParenthesis(regex) and \
           areValidQuantifiers(regex) and \
           areValidSymbols(regex) and \
           areValidCharacters(regex)


def areValidSymbols(regex: str):
    pattern = re.compile(r'(\w).*\1')
    return pattern.search(regex) is None


def areValidCharacters(regex: str):
    """check that the string contains only symbols, quantifiers, and parenthesis"""
    return re.match(r'[^A-Za-z?+*()]', regex) is None


def areValidQuantifiers(regex: str):
    pattern = re.compile(r'(?<=[^\w)])[?*+]|^[?+*]')
    return pattern.search(regex) is None


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
