import re
class Grammar:
    def __init__(self, rules):
        self.rules = rules
        self.symbol = None

    def addRules(self, nonTerminals, productions):
        if nonTerminals not in self.rules:
            self.rules[nonTerminals] = []
            self.rules[nonTerminals].append(productions)
    def setStartSymbol(self,startSymbol):
        self.symbol = startSymbol


    def tokenize(inputString):
        tokenSpecification = [
        ("NUMBER", r"\d+"),
        ("PLUS", r"\+"),
        ("TIMES", r"\*"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),
        ("SKIP", r"[ \t]+"),
        ("MISMATCH", r"."),
        ]
        tokenRegex = "|".join(f"(?P<{title}>{pattern})" for title, pattern in tokenSpecification)
        tokens = []
        for match in re.finditer(tokenRegex,inputString):
            kind = match.lastGroup
            value = match.group()
            if kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                raise RuntimeError(f"Unexpected character: {value}")
            tokens.append((kind, value))
        return tokens

class FirstFollow:
    def __init__(self, grammar:Grammar):
        self.grammar = grammar
        self.first = {nonTerminal: set() for nonTerminal in grammar.rules}
        self.follow = {nonTerminal: set() for nonTerminal in grammar.rules}
    def computeFirst(self):
        for nonTerminal in self.grammar.rules:
            self.first[nonTerminal] = self.firstOf(nonTerminal)
    def firstOf(self,symbol):
        if symbol not in self.grammar.rules:
            return {symbol}
        firstSet = set()
        for production in self.grammar.rules[symbol]:
            for prodSymbol in production:
                subFirst = self.firstOf(prodSymbol)
                firstSet.update(subFirst - {"ε"})
                if "ε" not in subFirst:
                    break
            else:
                subFirst.add("ε")
        return firstSet

    def computeFollow(self):
        self.follow[self.grammar.symbol].add("ε")
        while True:
            updated = True
            for nonTerminals, productions in self.grammar.rules.items():
                for production in productions:
                    for i, symbol in enumerate(production):
                        if symbol in self.grammar.rules:
                            rest = production[i + 1:]
                            restFirst = self.computeFirstOfString(rest)
                            beforeUpdate = len(self.follow[symbol])
                            self.follow[symbol].update(restFirst - "ε")
                            if "ε" in restFirst:
                                self.follow[symbol].update(self.follow[nonTerminals])
                            if len(self.follow[symbol]) > beforeUpdate:
                                updated = True
            if not updated:
                break


    def computeFirstOfString(self, symbols):
        result = set()
        for symbol in symbols:
            subFirst = self.firstOf(symbol)
            result.update(subFirst - {"ε"})
            if "ε" not in subFirst:
                return result
        result.add("ε")
        return result
    


class ParsingTable:
    def __init__(self,grammar: Grammar) :
        self.grammar = grammar
        self.actionTable ={}
        self.gotoTable = {}
        self.states = []
        self.transitions = {}

    def constructTable(self):
        augmentedStart = f"{self.grammar.start_symbol}'"
        self.grammar.addRules(augmentedStart, [self.grammar.symbol])
        self.grammar.setStartSymbol(augmentedStart)

        startItem = (augmentedStart, ["." + self.grammar.symbol], "$")
        initialState = self.closure([startItem])
        self.states.append(initialState)

        self.buildStates()

        for i, state in enumerate(self.states):
            self.actionTable[i]= {}
            self.gotoTable[i] = {}

            for symbol in self.transitions[i]:
                targetState = self.transitions[i][symbol]
                if symbol in self.grammar.rules:
                    self.gotoTable[i][symbol] = targetState
                else:
                     self.gotoTable[i][symbol] = ("shift", targetState)
            for item in state:
                head, body, lookahead = item
                if "." in body and body[-1] == ".":
                    if head == augmentedStart:
                        self.actionTable[i]["$"] = ("accept", None)
                    else:
                        productionIndex = self.grammar.rules[head].index(body[:-1])
                        self.actionTable[i][lookahead] = ("reduce", (head, productionIndex))
    def closure(self, items):
        closureSet = set(items)
        while True:
            newItem =set()
            for body, lookahead in closureSet:
                dotPosition = body.index('.')
                if dotPosition < len(body) -1:
                    nextSymbol = body[dotPosition + 1]
                    if nextSymbol in self.grammar.rules:
                        for production in self.grammar.rules[nextSymbol]:
                            for la in self.firstOfString(body[dotPosition + 2 : ] + [lookahead]):
                                newItem = (nextSymbol, ["." + production], la)
                                if newItem not in closureSet:
                                    closureSet.add(newItem)
            if not newItem:
                break
            closureSet.update(newItem)
        return closureSet
    
    def firstOfString(self, symbols):
        firstSet = set()
        for symbol in symbols:
            subFirst = self.firstOf(symbol)
            firstSet.update(subFirst - {"ε"})
            if "ε" not in subFirst:
                break
            else:
                firstSet.add("ε")
        return firstSet

    def buildStates(self):
        for i, state in enumerate(self.states):
            self.transitions[i] = {}
            symbols = {body[body.index(".") + 1] for _, body, _ in state if "." in body[:-1]}
            for symbol in symbols:
                newItems = set()
                for head, body, lookahead in state:
                    dotPosition = body.index('.')
                    if dotPosition <  len(body) -1 and body[dotPosition + 1]== symbol:
                        newItem = (head, body[:dotPosition] + [symbol, "."]  + body[dotPosition + 2:], lookahead)
                        newItems.add(newItem)
            closureSet = self.closure(newItems)
            if closureSet not in self.states:
                self.states.append(closureSet)
            self.transitions[i][symbol] = self.states.index(closureSet)



class LR1Parser:
    def __init__(self, grammar, parsing_table):
        self.grammar = grammar
        self.parsing_table = parsing_table

    def parse(self, tokens):
        stack = [0]
        index = 0
        while True:
            state = stack[-1]
            token = tokens[index][0] if index < len(tokens) else "$"
            
            if token in self.parsing_table.action_table[state]:
                action = self.parsing_table.action_table[state][token]
                if action[0] == "shift":
                    stack.append(action[1])
                    index += 1
                elif action[0] == "reduce":
                    production = self.grammar.rules[action[1]]
                    for _ in range(len(production)):
                        stack.pop()
                    goto_state = self.parsing_table.goto_table[stack[-1]][action[1]]
                    stack.append(goto_state)
                elif action[0] == "accept":
                    print("Input successfully parsed!")
                    return
            else:
                print("Syntax Error!")
                return










