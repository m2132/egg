"""Parser for the `Egg` language"""

import re
from collections import namedtuple

Atom = namedtuple('Atom', ['type', 'value'])
Apply = namedtuple('Apply', ['type', 'operator', 'args'])

class ParseError(BaseException):
    """Parse Error class"""

    def __init__(self, code, error="Can't parse:"):
        super().__init__(f"{error}\n{code}")


def parse_expression(code):
    """Parses an expression"""

    code = code.lstrip()

    if match := re.match(r'0|[1-9]\d*', code): # integer
        return Atom('value', int(match.group())), code[len(match.group()):]

    if match := re.match(r"'([^']*?)'", code): # str
        return Atom('value', match.groups()[0]), code[len(match.group()):]

    if match := re.match(r'(@?[^\s(),#"\']+)\(', code): # apply
        args, tail = parse_args(code[len(match.groups()[0]):])
        return Apply('apply', match.groups()[0], args), tail

    if match := re.match(r'[^\s(),#"\']+', code): # variable
        return Atom('name', match.group()), code[len(match.group()):]

    raise ParseError(code)


def parse_args(code):
    """Parses an `apply`'s arguments"""
    code = code.lstrip()

    if not code.startswith('('):
        raise ParseError(code)

    code = code[1:]
    arguments = []
    while not code.startswith(')'):
        node, code = parse_expression(code)
        arguments.append(node)
        code = re.sub(r'^\s*,?\s*', '', code)

    return arguments, code[1:]


def parse(code):
    """Parse an egg code"""
    absract_syntax_tree, tail = parse_expression(code)

    if tail.lstrip() != '':
        raise ParseError(tail, error='Unexpected text at end of program')

    return absract_syntax_tree
