import re
from collections import defaultdict

EPSILON = '_'
O_PARENTHESIS = '('
C_PARENTHESIS = ')'
STAR = '*'
PLUS = '+'
OPTIONAL = '?'


class State:
    def __init__(self):
        self.transitions = defaultdict(lambda: None)

    def addTransition(self, letter, state: 'State'):
        self.transitions[letter] = state

    def addEpsilonTransition(self, state:'State'):
        self.transitions[EPSILON] = state

    def getNextState(self, letter):
        return self.transitions[letter]

    def getEpsilonState(self):
        self.getNextState(EPSILON)

    def clone(self):
        state = State()
        state.transitions = self.transitions
        return  state


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

    def addTransition(self,letter):
        if self.finalState is None:
            # the automaton was previously empty
            self.startingState = State()
            self.finalState = State()
            self.startingState.addTransition(letter,self.finalState)
        else:
            # the automaton was not empty
            state = State()
            self.finalState.addTransition(letter,state)
            self.finalState = state

    def concatenateWith(self, automaton: 'Automaton'):
        """modify this automaton and constructs another one: which is the concatenation of the two"""
        self.finalState.addEpsilonTransition(automaton.getStartingState())
        self.finalState = automaton.getFinalState()

    def iterateStar(self):
        """ build automaton* """
        self.startingState.addEpsilonTransition(self.finalState)
        self.finalState.addEpsilonTransition(self.startingState)

    def iteratePlus(self):
        """ build automaton+ """
        startingSateClone = self.startingState.clone()
        self.iterateStar()
        self.startingState = startingSateClone

    def iterateOptional(self):
        """ build automaton? """
        self.startingState.addEpsilonTransition(self.finalState)


def buildAutomaton(regex: str) -> 'Automaton':
    """ the regex is a valid non empty regular expression """
    i = 0
    while i < len(regex):



def checkRegExValidity(regex: str, languageSymboles: set):
    return areValideParenthesis(regex) and \
           areValideQuantifiers(regex) and \
           areValideSymboles(regex) and \
           areLanguageSymboles(regex, languageSymboles)


def areValideSymboles(regex: str):
    pattern = re.compile(r'(\w).*\1')
    return pattern.search(regex) is None


def areValideQuantifiers(regex: str):
    pattern = re.compile(r'(?<=[^\w)])[?*+]|^[?+*]')
    return pattern.search(regex) is None


def areLanguageSymboles(regex: str, languageSymboles: set):
    usedSymboles = set(re.sub(r'[?+*()]', '', regex))
    return languageSymboles.intersection(usedSymboles) == usedSymboles


def areValideParenthesis(regex: str):
    first = regex.find('(')
    if first == -1:
        return regex.rfind(')') == -1
    # open parenthesis detected
    last = regex.rfind(')')
    if last - first <= 1:
        return False
    return True and areValideParenthesis(regex[first + 1:last])
