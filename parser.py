from node import Node

# Used to parse the tokens generated by the lexer to create an AST
class Parser:
    def __init__(self, tokens):
        self.line = 1  # Current line number
        self.tokens = tokens
        self.length = len(tokens)
        self.index = 0
        self.ast = self.parse()

    # Length of tokens
    def parse(self):
        statements = []
        while self.index < self.length:
            if self.tokens[self.index][0] == "MAKE":
                self.index += 1
                statements.append(self.assignment())
            elif self.tokens[self.index][0] == "DISPLAY":
                self.index += 2
                statements.append(self.display())
            else:
                self.index += 1
        return Node("STATEMENTS", down=statements)

    # Parse assignment statements
    def assignment(self):
        var_name = self.tokens[self.index][1]
        self.index += 1  # Skip variable name
        self.index += 1  # Skip '='
        expr = self.add_sub();
        if self.tokens[self.index][0] != "SEMICOLON":
            # Raise an exception if the statement doesn't end with a semicolon
            raise SyntaxError("Expected ';' at the end of the statement, line: " + str(self.line))
        self.index += 1  # Skip ';'
        self.line += 1 # Increment line number
        return Node("ASSIGN", value=var_name, right=expr)

    # Parse display statements
    def display(self):
        var_name = self.tokens[self.index][1]
        self.index += 1  # Skip variable name
        if self.tokens[self.index + 1][0] != "SEMICOLON":
            # Raise an exception if the statement doesn't end with a semicolon
            raise SyntaxError("Expected ';' at the end of the statement")
        self.index += 1  # Skip ';'
        self.line += 1 # Increment line number
        return Node("DISPLAY", value=var_name)

    # Parse addition and subtraction
    def add_sub(self):
        node = self.mul_div()

        while self.index < self.length and self.tokens[self.index][0] in ["ADD", "SUB"]:
            if self.tokens[self.index][0] == "ADD":
                self.index += 1
                node = Node("ADD", left=node, right=self.mul_div())
            elif self.tokens[self.index][0] == "SUB":
                self.index += 1
                node = Node("SUB", left=node, right=self.mul_div())

        return node

    # Parse multiplication and division
    def mul_div(self):
        node = self.exp()

        while self.index < self.length and self.tokens[self.index][0] in ["MUL", "DIV"]:
            if self.tokens[self.index][0] == "MUL":
                self.index += 1
                node = Node("MUL", left=node, right=self.exp())
            elif self.tokens[self.index][0] == "DIV":
                self.index += 1
                node = Node("DIV", left=node, right=self.exp())

        return node

    # Parse exponentiation
    def exp(self):
        node = self.factor()

        while self.index < self.length and self.tokens[self.index][0] == "EXP":
            self.index += 1
            node = Node("EXP", left=node, right=self.factor())

        return node

    # Parse factors
    def factor(self):
        token_type, token_value = self.tokens[self.index]
        if token_type == "NEG":
            self.index += 1
            return Node(token_type, down=self.factor())
        elif token_type == "LPAR":
            self.index += 1
            node = self.add_sub()  # Change here to add_sub
            if self.index < self.length and self.tokens[self.index][0] == "RPAR":
                self.index += 1
                return node
        elif token_type == "NUM":
            self.index += 1
            return Node(token_type, value=float(token_value))
        elif token_type == "ID":
            self.index += 1
            return Node(token_type, value=token_value)