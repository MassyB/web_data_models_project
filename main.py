from model_automaton_builder import getNFAFromPostfix
from pprint import pprint

nfa = getNFAFromPostfix("ab?&")
print(nfa.getSymbols())

dfa = nfa.toDFA()
print(dfa.match("ab"))
print(dfa.match("a"))
print(dfa.match(""))
print(dfa.match("c"))
print(dfa.match("azertyhujl"))


