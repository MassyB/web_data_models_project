import re
from model_automaton import O_PARENTHESIS, C_PARENTHESIS, STAR, PLUS, OPTIONAL

# juste to encode the end of the expression and to recognise the final state
EOExpression = '_'


def get_follow_sets(regex: str) -> dict:
    """follow sets of each symbol"""
    pass


def get_follow_set(regex: str, index: int) -> set:
    """the followers of a set using glushkov construction
       the regex is considered transformed, we always have the whole regex
       the idea is to check the symbols after  the current index"""
    follow_set = set()
    if index >= len(regex):
        # end of expression
        follow_set.add(EOExpression)
        return follow_set
    current_symbol = regex[index]
    if isCharacter(current_symbol):  # the current next_symbol
        next_symbol = regex[index + 1]  # the next next_symbol
        if isCharacter(next_symbol):
            follow_set.add(next_symbol)
            return follow_set

        if next_symbol == O_PARENTHESIS:
            # the next_symbol after the opening parenthesis
            return get_follow_set(regex, index + 1)

        if next_symbol == C_PARENTHESIS:
            # the next symbol is a closing parenthesis
            # check the symbol after the closing parenthesis
            if index + 2 >= len(regex):
                follow_set.add(EOExpression)
            else:
                after_cp_symbol = regex[index + 2]
                if isQuantifier(after_cp_symbol):
                    #get the opening parenthesis
                    op_index = getOpeningParenthesisIndex(regex, index + 1)
                    follow_set.union(get_follow_set(regex, op_index))
                elif after_cp_symbol == O_PARENTHESIS:
                    follow_set.union(get_follow_set(regex,index + 2))
                else:
                    #it's a symbol
                    follow_set.add(after_cp_symbol)


            pass

    if current_symbol == O_PARENTHESIS:
        # get rid of the successive opening brackets
        while regex[index + 1] == O_PARENTHESIS:
            index +=1
        follow_set.add(regex[index + 1])

        cp_index = getClosedParenthesisIndex(regex, index)

        if cp_index + 1 >= len(regex):
            follow_set.add(EOExpression)
        else:
            after_cp_symbol = regex[cp_index + 1]
            if after_cp_symbol == STAR or after_cp_symbol == OPTIONAL:
                if cp_index + 2 >= len(regex):
                    follow_set.add(EOExpression)
                else:
                    after_quantifier_symbol = regex[cp_index + 2]
                    if isCharacter(after_quantifier_symbol):
                        follow_set.add(after_quantifier_symbol)
                    else:
                        # another opening bracket
                        follow_set.union(get_follow_set(regex, cp_index + 2))
            elif
        return follow_set


def isQuantifier(symbol: str) -> bool:
    return symbol == STAR or symbol == PLUS or symbol == OPTIONAL


def isParenthesis(symbol: str) -> bool:
    return symbol == O_PARENTHESIS or symbol == C_PARENTHESIS


def isCharacter(symbol: str) -> bool:
    return (not isQuantifier(symbol)) and (not isParenthesis(symbol)) and symbol != ""


def transformRegex(regex: str) -> str:
    """put parenthesis around quantified symbols, to simplify the DFN construction"""
    return re.sub(r'(\w)([?*+])', r'(\1)\2', regex)


def isValidRegex(regex: str, languageSymbols: set):
    return areValidParenthesis(regex) and \
           areValidQuantifiers(regex) and \
           areValidSymbols(regex) and \
           areLanguageSymbols(regex, languageSymbols)


def areValidSymbols(regex: str):
    pattern = re.compile(r'(\w).*\1')
    return pattern.search(regex) is None


def areValidQuantifiers(regex: str):
    pattern = re.compile(r'(?<=[^\w)])[?*+]|^[?+*]')
    return pattern.search(regex) is None


def areLanguageSymbols(regex: str, languageSymboles: set):
    usedSymbols = set(re.sub(r'[?+*()]', '', regex))
    return languageSymboles.intersection(usedSymbols) == usedSymbols


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


def getOpeningParenthesisIndex(regex: str, closedParenthesisIndex):
    reverse_regex = ""
    size = len(regex)
    for i in range(size):
        j = size - 1 - i
        if regex[j] == '(':
            reverse_regex += ')'
        elif regex[j] == ')':
            reverse_regex += '('
        else:
            reverse_regex += regex[j]

    op_index = len(regex) - closedParenthesisIndex - 1
    opening_parenthesis_index = len(regex) - 1 - getClosedParenthesisIndex(reverse_regex, op_index)
    return opening_parenthesis_index

def areValidParenthesis(regex: str):
    i = 0
    while i < len(regex):
        symbol = regex[i]
        if symbol == O_PARENTHESIS:
            j = getClosedParenthesisIndex(regex, i)
            if j - i <= 1:
                return False
            else:
                # todo i+= 1 (nested parenthesis)
                i = j + 1
        elif symbol == C_PARENTHESIS:
            return False
        else:
            i += 1
    return True
