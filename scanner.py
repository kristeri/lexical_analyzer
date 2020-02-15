KEYWORDS = [
    "if", "else", "void", "int", "while", "break",
    "continue", "switch", "default", "case", "return"]
SYMBOLS = [";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "*", "=", "<", ">", "=="]
WHITESPACES = [" ", "\n", "\r", "\t", "\v", "\f" ]
ILLEGAL_CHARACTERS = ["!", '"', "#", "$", "%", "&", "'", "\\", "~", "@", "`", "/", "_", "|" ]
symbol_count = 0

def check(token, output_file):
    is_valid = False
    symbol_exists = False
    global symbol_count
    # NUM
    if token.isdigit():
        output_file.write("(NUM, " + token + ") ")
        is_valid = True
    # ID
    if token.isidentifier() and not token in KEYWORDS:
        output_file.write("(ID, " + token + ") ")
        symbol_table_read = open("symbol_table.txt", "r")
        with open("symbol_table.txt") as symbol_table_read:
            for line in symbol_table_read:
                line = line.strip()
                if token == line.split("\t")[1]:
                    symbol_exists = True
        if not symbol_exists:
            symbol_count += 1
            symbol_table = open("symbol_table.txt", "a")
            symbol_table.write(str(symbol_count) + ".\t" + token + "\n")
            is_valid = True
    # KEYWORD
    if token in KEYWORDS:
        output_file.write("(KEYWORD, " + token + ") ")
        is_valid = True
    # SYMBOL
    if token in SYMBOLS:
        output_file.write("(SYMBOL, " + token + ") ")
        is_valid = True
    # WHITESPACE
    if token in WHITESPACES:
        output_file.write("(WHITESPACE, " + token + ") ")
        is_valid = True
    return is_valid

def get_next_token():
    output = ""
    line_count = 0
    global symbol_count
    with open("input.txt") as input_file:
        output_file = open("tokens.txt", "w")
        lexical_errors = open("lexical_errors.txt", "w")
        symbol_table = open("symbol_table.txt", "w")
        for keyword in KEYWORDS:
            symbol_count += 1
            symbol_table.write(str(symbol_count) + ".\t" + keyword + "\n")
        symbol_table.close()
        for line in input_file:
            line_count += 1
            line = line.strip("\n")
            if not line.lstrip().startswith("//") and (not line.lstrip().startswith("/*") and not line.lstrip().endswith("*/")) and len(line.strip()) != 0:
                output_file.write(str(line_count) + ".\t")
                start = line.find("/*")
                end = line.find("*/")
                if start != -1 and end != -1:
                    line = line.replace(line[start:end + 2], "")
                tokens = line.split(" ")

                for token in tokens:
                    token = token.strip("\t")
                    for illegal_char in ILLEGAL_CHARACTERS:
                        if illegal_char in token:
                            split_error = token.split(illegal_char)
                            token = split_error[1]
                            lexical_errors.write(str(line_count) + ".\t" + "(" + split_error[0] + illegal_char + ", invalid input)\n")
                    if check(token, output_file) == True:
                        continue
                    else:
                        for char in token:
                            add_output = True
                            for symbol in SYMBOLS:
                                if len(output) > 0 and char == symbol:
                                    if output.isidentifier():
                                        output_file.write("(ID, " + output + ") ")
                                    if output.isdigit():
                                        output_file.write("(NUM, " + output + ") ")
                                    output_file.write("(SYMBOL, " + char + ") ")
                                    output = ""
                                    add_output = False
                                    break
                                if len(output) == 0 and char == symbol:
                                    output_file.write("(SYMBOL, " + char + ") ")
                                    output = ""
                                    add_output = False
                                    break
                            if add_output == True:
                                output += char
                            if any(item == output for item in KEYWORDS):
                                output_file.write("(KEYWORD, " + output + ") ")
                                output = ""

                output_file.write("\n")
    input_file.close()
    output_file.close()
    lexical_errors.close()
    symbol_table.close()
    return

get_next_token()
