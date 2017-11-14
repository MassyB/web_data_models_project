import re
from model_automaton import NFAAutomaton



def makeAutomaton(regex: str, languageSymbols: set) -> 'NFAAutomaton':
    if not isValidRegex(regex, languageSymbols):
        return None
    regexWithParenthesis = transformRegex(regex)
    automaton = buildAutomaton(regexWithParenthesis)
    return automaton


def buildAutomaton(regex: str) -> 'NFAAutomaton':
    """ the regex is a valid non empty regular expression """
    i = 0
    automaton = NFAAutomaton()
    subAutomaton = None
    while i < len(regex):
        symbol = regex[i]
        if symbol.isalpha():
            automaton.addTransition(symbol)
            i += 1

        elif symbol == O_PARENTHESIS:

            closedPraenthesisIndex = getClosedParenthesisIndex(regex, i)
            subRegex = regex[i + 1: closedPraenthesisIndex]
            subAutomaton = buildAutomaton(subRegex)
            i = closedPraenthesisIndex + 1

        elif symbol == STAR or symbol == PLUS or symbol == OPTIONAL:
            subAutomaton.iterateQuantifier(symbol)
            if automaton.isEmpty():
                automaton = subAutomaton
            else:
                automaton.concatenateWith(subAutomaton)
            subAutomaton = None
            i += 1

    if subAutomaton is not None:
        if automaton.isEmpty():
            automaton = subAutomaton
        else:
            automaton.concatenateWith(subAutomaton)

    return automaton
