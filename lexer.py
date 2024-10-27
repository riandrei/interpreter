# Used to tokenize the input expression
class Lexer:
    def __init__(self, expression):
        self.expression = expression
        self.tokens = self.tokenize()

    # Tokenize the input expression
    def tokenize(self):
        operators = {
            "(": "LPAR",
            ")": "RPAR",
            "^": "EXP",
            "*": "MUL",
            "/": "DIV",
            "+": "ADD",
            "-": "SUB",
            "=": "ASSIGN",
            ";": "SEMICOLON",
        }

        keywords = {
            "make": "MAKE",
            "display": "DISPLAY",
        }

        tokens = []
        i = 0
        length = len(self.expression)
        digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]

        # Iterate over the expression and tokenize it
        while i < length:
            curr = self.expression[i] # Current character
            if curr.isspace():
                i += 1
                continue
            if curr in operators:
                tokens.append((operators[curr], curr))
            elif curr.isalpha():
                identifier = curr
                while i + 1 < length and self.expression[i + 1].isalnum():
                    i += 1
                    identifier += self.expression[i]
                if identifier in keywords:
                    tokens.append((keywords[identifier], identifier))
                else:
                    tokens.append(("ID", identifier))
            elif curr in digits:
                num = curr
                while i + 1 < length and self.expression[i + 1] in digits:
                    i += 1
                    num += self.expression[i]
                tokens.append(("NUM", num))
            i += 1
        return tokens