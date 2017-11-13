from parser_xml_form_checker import XMLFormParser
import sys
from model_automaton_builder import makeAutomaton

automaton = makeAutomaton("a*", set("a"))

d = automaton.matches("aaa")