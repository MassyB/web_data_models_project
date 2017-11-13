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
        self.final = False
        self.epsilonTransitions = set()

    def getTransitions(self):
        return self.transitions

    def isFinal(self):
        return self.final

    def setFinal(self, final):
        self.final = final

    def addTransition(self, letter, state: 'State'):
        self.transitions[letter] = state

    def addEpsilonTransition(self, state: 'State'):
        self.epsilonTransitions.add(state)

    def getNextState(self, letter)->'State':
        return self.transitions[letter]

    def getEpsilonStates(self) -> set:
        return self.epsilonTransitions

    def getEpsilonAccessibleStates(self) -> set:
        statesToVisit = self.getEpsilonStates()
        statesVisited = {self}
        statesToAdd = set()

        while len(statesToVisit) != 0:
            for state in statesToVisit:
                statesToAdd = statesToAdd.union(state.getEpsilonStates())
            statesVisited = statesVisited.union(statesToVisit)
            statesToVisit = statesToAdd.difference(statesVisited)
            statesToAdd = set()
        return statesVisited

    def getSymbolEpsilonStar(self, symbol):
        state = self.getNextState(symbol)
        if state is None: return None
        return state.getEpsilonStates()

    def clone(self):
        state = State()
        state.transitions = self.transitions
        return state


class DFAAutomaton:
    def __init__(self):
        self.startingState = None

    def matches(self, string):
        """ true if the automaton matches the string, false otherwise"""
        state = self.startingState
        for c in string:
            state = state.getNextState(c)
            if state is None: return False
        return state.isFinal()


class NFAAutomaton:
    def __init__(self):
        self.startingState = None
        self.finalState = None

    def toDFA(self) -> 'DFAAutomaton':

        statesToVisit = {self.startingState}
        statesVisited = set()
        transitionTable = {}
        symbols = "symbols"

        while len(statesToVisit) != 0:
            for state in statesToVisit:
                statesVisited.add(state)
                # put the transition of the state in the table
                transitionTable[state] = {symbols: state.getTransitions(),
                                          EPSILON: state.getEpsilonAccessibleStates()}


    def isFinal(self, state: 'State'):
        return self.finalState == state

    def getFinalState(self):
        return self.finalState

    def getStartingState(self):
        return self.startingState

    def setFinalState(self, finalState):
        self.finalState = finalState

    def setStartingState(self, startingState):
        self.startingState = startingState

    def addTransition(self, letter):
        if self.finalState is None:
            # the automaton was previously empty
            self.startingState = State()
            self.finalState = State()
            self.startingState.addTransition(letter, self.finalState)
        else:
            # the automaton was not empty
            state = State()
            self.finalState.addTransition(letter, state)
            self.finalState = state

    def concatenateWith(self, automaton: 'NFAAutomaton'):
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

    def iterateQuantifier(self, quantifier):
        if quantifier == STAR:
            self.iterateStar()
        elif quantifier == PLUS:
            self.iteratePlus()
        elif quantifier == OPTIONAL:
            self.iterateOptional()

    def isEmpty(self):
        return self.finalState is None
