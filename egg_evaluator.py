"""Evaluator for the `Egg` language"""

import random

class EvaluationError(BaseException):
    """Evaluation Error class"""
    def __init__(self, error='Evaluation error'):
        super().__init__(error)


def if_keyword(condition, do_block, else_block, scope):
    """@if keyword defenition"""
    if evaluate(condition, scope):
        return evaluate(do_block, scope)
    return evaluate(else_block, scope)


def while_keyword(condition, block, scope):
    """@while keyword defenition"""
    value = None
    while evaluate(condition, scope):
        value = evaluate(block, scope)
    return value


def fun_keyword(*params, scope):
    """@fun keyword defenition"""
    if len(params) == 0:
        raise EvaluationError('A function must have a body')

    def function(*args):
        if len(args) != len(params) - 1:
            raise EvaluationError(f'Expected {len(params) - 1} arguments but got {len(params)}')

        inner_scope = { 'parent': scope }
        for arg, param in zip(args, params[:-1]):
            if param.type != 'name':
                raise EvaluationError(f'Function parameters must be of type `name` but got {param}')
            inner_scope[param.value] = arg

        return evaluate(params[-1], inner_scope)
    return function


def set_keyword(name, value, scope):
    """@set keyword defenition"""
    if name.type != 'name':
        raise EvaluationError('@set first argument must be a `name` node')

    value = evaluate(value, scope)

    _, var_scope = get_name(name.value, scope)
    if var_scope is not None:
        var_scope[name.value] = value
    else:
        scope[name.value] = value
    return value

keywords = {
    '@if': if_keyword,
    '@while': while_keyword,
    '@fun': fun_keyword,
    '@set': set_keyword,
}

builtins = {
    'log': print,
    'input': lambda: input(),
    'rand': random.randint,
    'do': lambda *args: args[-1],
    'parent': None,
    'str': str,
    'int': int,
    'true': True,
    'false': False,
    'nil': None,
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '/': lambda a, b: a // b,
    '*': lambda a, b: a * b,
    '>': lambda a, b: a > b,
    '%': lambda a, b: a % b,
    '>=': lambda a, b: a >= b,
    '==': lambda a, b: a == b,
    '!=': lambda a, b: a != b,
    '<=': lambda a, b: a <= b,
    '<': lambda a, b: a < b,
}


def get_name(name, scope):
    """Finds variable in scope"""
    if scope is None:
        return None, None

    if name in scope:
        return scope[name], scope

    return get_name(name, scope['parent'])


def evaluate(node, scope=None):
    """Main evaluate function"""
    scope = scope or { 'parent': builtins }

    if node.type == 'value':
        return node.value

    if node.type == 'name':
        var_value = get_name(node.value, scope)[0]
        if var_value is None:
            raise EvaluationError(f'Variable not defined {node.value}')
        return var_value

    if node.type == 'apply':
        if node.operator.startswith('@'):
            return keywords[node.operator](*node.args, scope=scope)

        args = [evaluate(arg, scope) for arg in node.args]
        function = get_name(node.operator, scope)[0]
        if function is None:
            raise EvaluationError(f'Function {node.operator} is not defined')
        return function(*args)

    raise EvaluationError(f'unknown node {node}')
