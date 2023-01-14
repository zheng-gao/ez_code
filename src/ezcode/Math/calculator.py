import math


def validate_infix_brackets(infix: str):
    stack = list()
    for char in infix:
        if char == "(":
            stack.append(char)
        elif char == ")":
            if len(stack) == 0:
                return False
            else:
                stack.pop()
    return len(stack) == 0


def is_operator(char: str) -> bool:
    return char in ["+", "-", "*", "/", "^", "√", "!"]


def infix_notation_to_reverse_polish_notation(infix: str) -> list:
    """ Shunting-yard Algorithm by Dijkstra """

    def _parse_number(string: str):
        return float(string) if "." in string else int(string)

    def _operator_precedence(operator: str):
        if operator in ["+", "-"]:
            return 1
        elif operator in ["*", "/"]:
            return 2
        elif operator in ["^"]:
            return 3
        elif operator in ["√"]:
            return 4
        elif operator in ["!"]:
            return 5

    if not validate_infix_brackets(infix):
        raise ValueError(f"Invalid arithmetic expression: {infix}")
    infix.replace(" ", "")  # remove all the spaces
    operator_stack = list()
    rpn = list()
    operand = ""
    for i in range(len(infix)):
        char = infix[i]
        if char.isdigit() or char == ".":
            operand += char
            if i == len(infix) - 1:
                rpn.append(_parse_number(operand))
        else:
            if operand != "":
                rpn.append(_parse_number(operand))
                operand = ""
        if is_operator(char):
            # process unary operator
            if char == "-" and (i == 0 or infix[i - 1] == "(" or is_operator(infix[i - 1])):
                operand = char
            else:
                while len(operator_stack) > 0 and operator_stack[-1] != "(":
                    if _operator_precedence(operator_stack[-1]) >= _operator_precedence(char):
                        rpn.append(operator_stack.pop())
                    else:
                        break
                operator_stack.append(char)
        if char == "(":
            operator_stack.append(char)
        if char == ")":
            while len(operator_stack) > 0 and operator_stack[-1] != "(":
                rpn.append(operator_stack.pop())
            if len(operator_stack) > 0:
                operator_stack.pop()  # pop "("
    while len(operator_stack) > 0:
        rpn.append(operator_stack.pop())
    return rpn


def evaluate_reverse_polish_notation(tokens: list):
    operand_stack = list()
    for t in tokens:
        if is_operator(t):
            if t == "!":
                operand = operand_stack.pop()
                if isinstance(operand, int) and operand >= 0:
                    factorial = 1
                    for i in range(2, operand + 1):
                        factorial *= i
                    operand_stack.append(factorial)
                else:
                    raise ValueError(f"Invalid factorial operand: {operand}")
            elif t == "√":
                operand = operand_stack.pop()
                operand_stack.append(math.sqrt(operand))
            else:
                operand_right = operand_stack.pop()
                operand_left = operand_stack.pop()
                if t == "+":
                    operand_stack.append(operand_left + operand_right)
                elif t == "-":
                    operand_stack.append(operand_left - operand_right)
                elif t == "*":
                    operand_stack.append(operand_left * operand_right)
                elif t == "/":
                    operand_stack.append(operand_left / operand_right)
                elif t == "^":
                    operand_stack.append(math.pow(operand_left, operand_right))
        else:
            operand_stack.append(t)
    return operand_stack.pop()


def calculate(infix: str):
    return evaluate_reverse_polish_notation(infix_notation_to_reverse_polish_notation(infix))












