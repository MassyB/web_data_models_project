from model_automaton_builder import getNFAFromPostfix
from pprint import pprint

nfa = getNFAFromPostfix("ab?&")
print(nfa.getSymbols())

nfa.toDFA()
print("hello")


