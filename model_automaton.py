import re
from collections import defaultdict

EPSILON= '_'
O_PARENTHESIS= '('
C_PARENTHESIS= ')'
STAR= '*'
PLUS= '+'
OPTIONAL= '?'

class State:
    def __init__(self):
        self.transitions = defaultdict(lambda: None)
        self.starting = False
        self.final = False

    def addTransition(self, letter, node: 'Node'):
        self.transitions[letter] = node

    def getNextState(self, letter):
        return self.transitions[letter]

    def getEpsilonState(self):
        self.getNextState(EPSILON)

    def setFinalState(self, final):
        self.final = final

    def isFinal(self):
        return self.final

    def setStarting(self, starting):
        self.starting = starting

    def isStarting(self):
        return self.starting


class Automaton:
    def __init__(self):
        self.startingState = None
        self.finalState = None

    def getFinalState(self):
        return self.finalState

    def getStartingState(self):
        return self.startingState

    def setFinalState(self, finalState):
        self.finalState = finalState

    def setStartingState(self, startingState):
        self.startingState = startingState


def buildAutomaton(regex:str)->'Automaton':
    i = 0
    while i < len(regex):
        pass

def checkRegExValidity(regex:str, languageSymboles:set):
    return areValideParenthesis(regex) and \
           areValideQuantifiers(regex) and \
           areValideSymboles(regex) and \
           areLanguageSymboles(regex, languageSymboles)

def areValideSymboles(regex:str):
    pattern = re.compile(r'(\w).*\1')
    return pattern.search(regex) is None

def areValideQuantifiers(regex:str):
    pattern = re.compile(r'(?<=[^\w)])[?*+]|^[?+*]')
    return pattern.search(regex) is None

def areLanguageSymboles(regex:str, languageSymboles:set):
    usedSymboles = set(re.sub(r'[?+*()]','',regex))
    return languageSymboles.intersection(usedSymboles) == usedSymboles

def areValideParenthesis(regex:str):
    first = regex.find('(')
    if first == -1:
        return regex.rfind(')') == -1
    #open parenthesis detected
    last = regex.rfind(')')
    if last - first <= 1:
        return False
    return True and areValideParenthesis(regex[first+1:last])
