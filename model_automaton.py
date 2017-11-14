from collections import defaultdict
from model_automaton_builder import EPSILON


class State:
    def __init__(self):
        self.transitions = defaultdict(lambda: None)
        self.transitions[EPSILON] = set()

    def addTransition(self, letter, state: 'State'):
        self.transitions[letter] = state

    def addEpsilonTransition(self, state: 'State'):
        self.transitions[EPSILON].add(state)

    def getNextState(self, letter):
        return self.transitions[letter]

    def getEpsilonStates(self):
        return self.transitions[EPSILON]


class NFA:
    def __init__(self):
        self.startingState = None
        self.finalState = None
        self.symbols = set()

    def getFinalState(self):
        return self.finalState

    def getStartingState(self):
        return self.startingState

    def setFinalState(self, finalState):
        self.finalState = finalState

    def setStartingState(self, startingState):
        self.startingState = startingState

    def toDFA(self):
        pass

    def addTransition(self, letter):
        pass

    def concatenateWith(self, automaton: 'Automaton'):
        pass

    def iterateStar(self):
        pass

    def iteratePlus(self):
        pass

    def iterateOptional(self):
        pass

    def iterateQuantifier(self, quantifier):
        pass

    def isEmpty(self):
        pass


class DFA(NFA):
    def match(self, s: str):
        pass