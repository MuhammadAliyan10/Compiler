# LR(0) Parsing Theory

## Introduction to LR(0) Parsing

LR(0) is a type of **bottom-up** deterministic parser used for syntax analysis in compilers. It stands for **Left-to-right**, **Rightmost derivation**, and **0 lookahead**.

- **Left-to-right**: The parser processes the input string from left to right.
- **Rightmost derivation**: The parser uses a rightmost derivation in reverse (i.e., reducing the rightmost non-terminal).
- **0 lookahead**: The parser makes parsing decisions based solely on the current input symbol and the current state, without any lookahead (i.e., it only looks at the current symbol and does not look ahead at the next one).

### Key Concepts of LR(0) Parsing

1. **States and Items**:

   - The parser maintains a set of **states**, each of which corresponds to a set of **items**.
   - An **item** represents a production rule with a dot (`•`) indicating the current position in the rule.

     Example:
     For the production `A -> a A`, an item might be:

     ```
     A -> • a A
     ```

     This indicates that the parser is currently at the beginning of the production `A -> a A` and is looking to process an `a`.

2. **Closure**:

   - **Closure** is a process that computes all the possible items that can be derived from a given set of items. This is necessary because the parser needs to account for all potential derivations that can follow a particular state.

   - For example, if you have the item `A -> • a A` and `A` is a non-terminal, the closure operation adds more items based on the rules for `A` (e.g., `A -> • b`), essentially expanding the possible derivations.

3. **Goto**:

   - **Goto** is an operation that computes the state resulting from shifting a symbol (either terminal or non-terminal) after processing the current input symbol.

   - For example, given a set of items representing a state, the `goto` operation computes the next state after shifting the input symbol, expanding the items in that state.

4. **Action and Goto Tables**:

   - An **action table** contains actions to be performed at each state, depending on the next input symbol.
   - The **goto table** describes state transitions based on the non-terminals. When a non-terminal is encountered, the `goto` table determines which state to transition to.

   These tables guide the parser in deciding whether to **shift**, **reduce**, or **accept** the input string.

### Example Grammar

Consider the following simple context-free grammar (CFG):

Where:

- `S` is the start symbol.
- `A` is a non-terminal that can be replaced by either `a A` or `b`.
- `a` and `b` are terminal symbols (the actual symbols in the input).

### Step-by-Step Explanation of LR(0) Parsing

1. **Start with the initial state**:
   The parsing process begins with the **start symbol** and its corresponding rule. We construct the initial item set, which for this grammar would be:

2. **Apply Closure**:
   We apply the **closure operation** to this set of items. In this case, the closure operation doesn't add any new items because the symbols after the dot are already terminals or there are no more non-terminals that need expanding.

3. **Shift and Reduce**:
   The parser proceeds by **shifting** symbols onto the stack or **reducing** the stack using production rules:

- **Shift**: Move to the next state by shifting the next symbol onto the stack.
- **Reduce**: Apply a reduction rule when a complete right-hand side of a production is matched on the stack.

For example:

- If the input symbol is `a`, and the current state has the item `A -> • a A`, the parser will shift and add the symbol `a` to the stack.
- If the input symbol is `b`, and the current state has the item `A -> • b`, the parser will reduce the stack using the rule `A -> b`.

4. **Construct the Canonical Collection**:
   The **canonical collection** of sets of items is constructed by repeatedly applying the **closure** and **goto** operations to generate all possible states the parser might encounter during the parsing process. Each state corresponds to a particular configuration of the grammar rules and input symbols.

The states represent various points in the parsing process and are used to decide the next parsing action.

Example canonical states for this grammar:

- **State 0**: `{S' -> • S, S -> • A, A -> • a A, A -> • b}`
- **State 1**: `{A -> b • }` (A complete reduction)
- **State 2**: `{S' -> S • }` (Parsing is complete)

5. **Final Parsing Decision**:
   The parser continues shifting and reducing until it either:

- **Accepts**: If the input string is valid according to the grammar.
- **Rejects**: If an invalid state is encountered or no valid transitions exist for the input string.

### Example Parsing Sequence

Given the input string `a a b`, the LR(0) parser would proceed as follows:

- **Initial state**: `{S' -> • S, S -> • A, A -> • a A, A -> • b}`
- The parser would shift `a` onto the stack and move to a new state.
- The parser would then shift the second `a` onto the stack and continue.
- Finally, when it encounters `b`, the parser reduces using the rule `A -> b`, and the input string is successfully parsed.

### Action and Goto Tables

In LR(0), the **action table** tells the parser what to do when it encounters a terminal symbol, while the **goto table** determines the next state for non-terminal symbols. The parser uses these tables to decide:

- **Shift**: Move to the next state.
- **Reduce**: Apply a reduction rule.
- **Accept**: If the input string is successfully parsed.
- **Error**: If no valid action can be taken.

### Advantages of LR(0)

- **Deterministic**: LR(0) parsers are deterministic and efficient because they do not require backtracking.
- **Simple to implement**: The LR(0) parsing algorithm is relatively straightforward and is the foundation for more complex LR parsers (like LR(1)).

### Limitations of LR(0)

- **Limited power**: LR(0) can only handle a limited set of grammars, and it may not work for more complex grammars that require more lookahead or ambiguity resolution.
- **Inability to handle all grammars**: Some context-free grammars that are ambiguous or involve conflicts may not be parseable with LR(0) parsers.

## Conclusion

LR(0) parsing is an important technique in compiler design for constructing efficient parsers. While it is limited in the types of grammars it can handle, it forms the foundation for more powerful parsers like LR(1) and LALR(1). Understanding the theory behind LR(0) parsing is crucial for anyone looking to delve deeper into compiler construction or formal language processing.

---

This markdown file focuses on explaining the theory behind LR(0) parsing, the grammar example, and the parsing process step-by-step. It's structured to provide a solid understanding of the underlying concepts, which can then be applied to more complex scenarios.
