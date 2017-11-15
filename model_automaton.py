from collections import defaultdict

EPSILON = '_'
O_PARENTHESIS = '('
C_PARENTHESIS = ')'
STAR = '*'
PLUS = '+'
OPTIONAL = '?'
AND = '&'


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

    def getTransitions(self):
        return self.transitions

    def setTransitions(self, transitions):
        self.transitions = transitions


class NFA:
    def __init__(self, starting_state=None, final_state=None, symbols=set()):
        self.start_state = starting_state
        self.final_state = final_state
        self.symbols = symbols
        self.states = None
        self.epsilonClosures = None

    def initStates(self):
        self.states = self.visitDFS(self.start_state)

    def getStates(self):
        return self.states

    def toDFA(self):
        self.initStates()
        self.setEpsilonClosures()
        transition_table = defaultdict(lambda: defaultdict(lambda: None))
        tuple_state = defaultdict(lambda: State())
        dfa_start_state = None
        dfa_final_states = set()

        states_todo = list()
        epsilon_closure_start_state = tuple(self.epsilonClosures[self.start_state])
        states_todo.append(epsilon_closure_start_state)
        dfa_start_state = tuple_state[epsilon_closure_start_state]
        states_done = set()

        while len(states_todo) > 0:
            ts = states_todo.pop()
            states_done.add(ts)
            current_state = tuple_state[ts]
            if self.final_state in ts:
                dfa_final_states.add(current_state)

            current_transitions = transition_table[current_state]
            for s in self.symbols:
                reached_states = tuple(self.getEpsilonReachableFromStates(ts, s))
                if len(reached_states) == 0:
                    current_transitions[s] = None
                else:
                    current_transitions[s] = tuple_state[reached_states]
                    if reached_states not in states_done:
                        states_todo.append(reached_states)

        # construct the dfa from the table of transitions
        for state, transitions in transition_table.items():
            state.setTransitions(transitions)

        return DFA(dfa_start_state, dfa_final_states)

    def getEpsilonReachableFromStates(self, states, letter):
        reachable_from_states = set()
        for state in states:
            reachable_from_state = self.getEpsilonReachableFromState(state, letter)
            reachable_from_states = reachable_from_states.union(reachable_from_state)
        return reachable_from_states

    def getEpsilonReachableFromState(self, state, letter):
        """get all the states reachable from 'state' having 'letter' in the input"""
        next_state = state.getNextState(letter)
        if next_state is None:
            return set()
        return self.epsilonClosures[next_state]

    def setEpsilonClosures(self):
        """ we suppose that we already computed the list of states"""
        epsilon_closures_dict = {}
        for state in self.states:
            epsilon_closures_dict[state] = self.getEpsilonClosure(state, set())
        self.epsilonClosures = epsilon_closures_dict

    def getEpsilonClosure(self, state, visited_epsilon_neighbors=set()):
        """computes all the states accessible by state using zero or more epsilon transitions"""
        visited_epsilon_neighbors.add(state)
        for epsilon_neighbor in state.getEpsilonStates():
            if epsilon_neighbor not in visited_epsilon_neighbors:
                self.getEpsilonClosure(epsilon_neighbor, visited_epsilon_neighbors)
        return visited_epsilon_neighbors

    def visitDFS(self, state, visited_states=set()):
        # mark the current state
        visited_states.add(state)
        # visit the epsilon neighbors
        epsilon_neighbors = state.getEpsilonStates()
        for neighbor in epsilon_neighbors:
            if neighbor not in visited_states:
                self.visitDFS(neighbor, visited_states)

        for symbol, neighbor in state.getTransitions().items():
            if symbol != EPSILON:
                if neighbor not in visited_states:
                    self.visitDFS(neighbor, visited_states)

        return visited_states

    @staticmethod
    def createNFAFromLetter(letter: str) -> 'NFA':
        start_state = State()
        final_state = State()
        start_state.addTransition(letter, final_state)
        nfa = NFA(start_state, final_state, {letter})
        return nfa

    def getFinalState(self):
        return self.final_state

    def getSymbols(self):
        return self.symbols

    def setSymbols(self, symbols):
        self.symbols = symbols

    def getStartState(self):
        return self.start_state

    def setFinalState(self, finalState):
        self.final_state = finalState

    def setStartingState(self, startingState):
        self.start_state = startingState

    def concatenateWith(self, nfa: 'NFA'):
        "the current nfa is the result of the concatenation between the two"
        nfa_transitions = nfa.getStartState().getTransitions()
        self.final_state.setTransitions(nfa_transitions)
        # update the sates and symbols
        self.final_state = nfa.getFinalState()
        self.setSymbols(self.symbols.union(nfa.getSymbols()))

    def iterateStar(self):
        "the current nfa is the result of the concatenation"
        new_start_state = State()
        new_final_state = State()
        self.final_state.addEpsilonTransition(self.start_state)
        self.final_state.addEpsilonTransition(new_final_state)
        new_start_state.addEpsilonTransition(self.start_state)
        new_start_state.addEpsilonTransition(new_final_state)

        # update of the final and start state
        self.start_state = new_start_state
        self.final_state = new_final_state

    def iteratePlus(self):
        new_start_state = State()
        new_final_state = State()
        self.final_state.addEpsilonTransition(self.start_state)
        self.final_state.addEpsilonTransition(new_final_state)
        new_start_state.addEpsilonTransition(self.start_state)
        # update of the states
        self.start_state = new_start_state
        self.final_state = new_final_state

    def iterateOptional(self):
        new_start_state = State()
        new_final_state = State()
        new_start_state.addEpsilonTransition(self.start_state)
        new_start_state.addEpsilonTransition(new_final_state)
        self.final_state.addEpsilonTransition(new_final_state)
        # update of the states
        self.start_state = new_start_state
        self.final_state = new_final_state

    def iterateQuantifier(self, quantifier):
        if quantifier == STAR:
            self.iterateStar()
        elif quantifier == PLUS:
            self.iteratePlus()
        elif quantifier == OPTIONAL:
            self.iterateOptional()

    def isEmpty(self):
        pass


class DFA:
    def __init__(self, start_state, final_states):
        self.start_state = start_state
        self.final_states = final_states

    def match(self, string: str):
        c_state = self.start_state
        symbols_read = 0
        for s in string:
            if c_state is not None:
                c_state = c_state.getNextState(s)
                symbols_read += 1
            else:
                break
        if symbols_read < len(string) or c_state not in self.final_states:
            return False
        return True