import sys

from lexer import Lexer
from parser import Parser
from evaluator import Evaluator

def main():
    # Check if the filename is provided
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename>")
        return

    # Read the source code from the file
    filename = sys.argv[1]

    with open(filename, 'r') as file:
        source_code = file.read()

    # Run the interpreter
    lexer = Lexer(source_code)
    parser = Parser(lexer.tokens)
    evaluator = Evaluator(parser.ast)

if __name__ == "__main__":
    try:
        main()
    except ZeroDivisionError as e:
        print(e)
    except ValueError as e:
        print(e)
    except OverflowError as e:
        print(f"Overflow error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
