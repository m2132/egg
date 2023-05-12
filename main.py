CODE_PATH = r'.\\code.egg'

from egg_parser_2 import expr

# open the file and print its content

# file = open(CODE_PATH)
# print(file.read())
# file.close()


with open(CODE_PATH) as file:
    content = file.read()

    print(expr("log(3, 1, 343)"))


