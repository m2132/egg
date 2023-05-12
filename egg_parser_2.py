import re


def arguments(code):
    pass


def expr(code):
    code = code.lstrip()

    int_re = r"\d+"
    if match := re.match(int_re, code):
        match_value = match.group()
        node = { "type": 'int', "value": int(match_value) }
        tail = code[len(match_value):]
        return node, tail
    
    apply_re = r"([^\d\s'#()]+)\("
    if match := re.match(apply_re, code):
        match_groups = match.groups()
        operator = match_groups[0]
        tail = code[len(operator):]
        args, tail = arguments(tail)
        node = { "type": 'apply', 'operator': operator, 'args': args }
        return node, tail




def parse(code):
    return # tree of code

