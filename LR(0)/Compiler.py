class Grammar:
    def __init__(self, rules):
        self.rules = rules
        self.terminals = set()
        self.nonTerminals = set(rules.keys())
        for prodList in rules.values():
            for prod in prodList:
                for symbol in prod:
                    if symbol not in self.nonTerminals:
                        self.terminals.add(symbol)


class Item:
    def __init__(self, lhs, rhs, dotPosition=0):
        self.lhs = lhs
        self.rhs = rhs
        self.dotPosition = dotPosition

    def isCompleted(self):
        return self.dotPosition == len(self.rhs)

    def __repr__(self):
        before_dot = " ".join(self.rhs[:self.dotPosition])
        after_dot = " ".join(self.rhs[self.dotPosition:])
        return f"{self.lhs} -> {before_dot} • {after_dot}"

    def __eq__(self, other):
        return (
            self.lhs == other.lhs
            and self.rhs == other.rhs
            and self.dotPosition == other.dotPosition
        )

    def __hash__(self):
        return hash((self.lhs, tuple(self.rhs), self.dotPosition))


def closure(items, grammar: Grammar):
    closureSet = set(items)
    while True:
        added = False
        for item in list(closureSet):
            if item.dotPosition < len(item.rhs):
                symbol = item.rhs[item.dotPosition]
                if symbol in grammar.nonTerminals:
                    for prod in grammar.rules[symbol]:
                        newItem = Item(symbol, prod, 0)
                        if newItem not in closureSet:
                            print(f"Adding new item to closure: {newItem}")
                            closureSet.add(newItem)
                            added = True
        if not added:
            break
    return closureSet


def goto(items, symbol, grammar):
    nextItems = {Item(item.lhs, item.rhs, item.dotPosition + 1) 
                 for item in items if item.dotPosition < len(item.rhs) and item.rhs[item.dotPosition] == symbol}
    return closure(nextItems, grammar)


def constructCanonicalCollection(grammar: Grammar):
    startItem = Item("S'", ["S"])
    startState = closure({startItem}, grammar)
    states = [startState]
    stateMapping = {frozenset(startState): 0}  
    transitions = {}
    
    while True:
        added = False
        for state in states:
            for symbol in grammar.terminals.union(grammar.nonTerminals):
                nextState = goto(state, symbol, grammar)
                if nextState and frozenset(nextState) not in stateMapping:
                    states.append(nextState)
                    stateMapping[frozenset(nextState)] = len(states) - 1
                    transitions[(states.index(state), symbol)] = len(states) - 1
                    added = True
        if not added:
            break
    
    return states, transitions


def constructParsingTable(states, transitions, grammar):
    action = {}
    gotoTable = {}
    for i, state in enumerate(states):
        for item in state:
            if item.isCompleted():
                if item.lhs == "S'":
                    action[i] = ("accept",)
                else:
                    action[i] = ("reduce", item.lhs, item.rhs)
            else:
                symbol = item.rhs[item.dotPosition]
                if symbol in grammar.terminals:
                    nextState = transitions.get((i, symbol))
                    if nextState is not None:
                        action[i] = ("shift", nextState)
                elif symbol in grammar.nonTerminals:
                    nextState = transitions.get((i, symbol))
                    if nextState is not None:
                        gotoTable[i] = nextState
    return action, gotoTable


def parse(inputString, action, gotoTable, grammar):
    stack = [0]
    inputTokens = inputString.split() + ["$"]
    index = 0
    while True:
        state = stack[-1]
        token = inputTokens[index]
        if state in action:
            act = action[state]
            if act[0] == "shift":
                stack.append(act[1])
                index += 1
            elif act[0] == "reduce":
                lhs, rhs = act[1], act[2]
                for _ in range(len(rhs)):
                    stack.pop()
                state = stack[-1]
                stack.append(gotoTable[state])
            elif act[0] == "accept":
                return True
        else:
            return False


rules = {
    "S": [["A"]],
    "A": [["a", "A"], ["b"]]
}


grammar = Grammar(rules)

states, transitions = constructCanonicalCollection(grammar)
print("\nCanonical States:")
for i, state in enumerate(states):
    print(f"State {i}:\n{state}")

print("\nTransitions:")
for key, value in transitions.items():
    print(f"From State {key[0]} on '{key[1]}': Go to State {value}")


action, gotoTable = constructParsingTable(states, transitions, grammar)
print("\nAction Table:")
print(action)
print("\nGoto Table:")
print(gotoTable)

inputString = "a a b"
result = parse(inputString, action, gotoTable, grammar)
print(f"\nParsing result for '{inputString}': {'Accepted' if result else 'Rejected'}")
