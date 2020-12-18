import logging
import operator
import re

logger = logging.getLogger(__name__)


def tokenize(expression):
    i = 0
    tokens = []
    current_token = None

    while i < len(expression):
        c = expression[i]
        i += 1

        if c == ' ':
            continue

        elif c in ['+', '*', '(', ')']:
            if current_token is not None:
                tokens.append(current_token)
                current_token = None

            tokens.append(c)
        else:
            if current_token is None:
                current_token = ''

            current_token = current_token + c

    if current_token is not None:
        tokens.append(current_token)

    return tokens


def to_postfix(infix, use_advanced_precedence=False):
    stack = []
    postfix = []

    def has_bigger_priority(a, b):
        priorities = {
            '+': 1 if use_advanced_precedence else 2,
            '*': 2,
            '(': 10,
            ')': 10
        }

        return priorities[a] > priorities[b]

    for c in infix:
        # logger.info("---")
        # logger.info(f"Current token: {c}")
        # logger.info(f"Current stack: {stack}")
        # logger.info(f"Current res:   {postfix}")

        if c == ' ' or c is None:
            continue

        # Operand
        elif re.match(r'^\d+$', c):
            postfix.append(int(c))

        # Other
        else:
            if c == '(':
                stack.append(c)

            elif c == ')':
                oper = stack.pop()

                while oper != '(':
                    postfix.append(oper)
                    oper = stack.pop()

            else:
                while stack and not has_bigger_priority(stack[-1], c):
                    postfix.append(stack.pop())

                stack.append(c)

    while stack:
        postfix.append(stack.pop())

    return postfix


def evaluate_expression(expression, use_advanced_precedence=False):
    tokenized_expression = tokenize(expression)
    postfix_expression = to_postfix(tokenized_expression, use_advanced_precedence)

    logger.info(f"Expression (infix)    : {expression}")
    logger.info(f"Expression (tokenized): {tokenized_expression}")
    logger.info(f"Expression (postfix)  : {postfix_expression}")

    opfun = {'+': operator.add, '*': operator.mul}

    stack = []
    i = 0

    while i < len(postfix_expression):
        token = postfix_expression[i]
        i += 1

        if token in ['+', '*']:
            op1 = int(stack.pop())
            op2 = int(stack.pop())

            res = opfun[token](op1, op2)
            stack.append(res)

        else:
            stack.append(token)

    return stack.pop()
