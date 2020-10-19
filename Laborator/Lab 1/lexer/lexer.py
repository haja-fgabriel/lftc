#TODO implement lexer

if __name__ != "__main__":    
    from lexer.binary_tree import BinaryTree
    from lexer.errors import TokenizerException
    #from lexer.state_machine import StateMachine
import re
from colorama import *

class MockLexer:

    def __init__(self, atoms_table, sym_table):
        self.__atoms_table = atoms_table
        self.__sym_table = sym_table
    

    def get_all_tokens(self, code):
        result = []
        index = 0
        for line in code:
            index += 1

            tokens = line.split(' ')
            for token in tokens:
                data = self.__atoms_table.search(token)

                if data:
                    result += [(token, data[1])]
                else:
                    if re.match(r"([$_a-zA-Z]+[0-9]*)+", token): 
                        if len(token) > 8:
                            raise TokenizerExecption(f"Token '{token}' at line {index} has length greater than 8.")
                        result += [(token, 'ID')]
                    elif re.match(r"[-]?[0-9]*([.][0-9]+)?", token): 
                        result += [(token, 'constant')]
                    else:
                        raise TokenizerExecption(f"Invalid token '{token}' at line {index}.")
            
        for token in result:
            print(f"Token in file: '{token[0]}'\twith code {token[1]}")
        return tokens



class RegexLexer:

    def __init__(self, atoms_table, sym_table):
        self.__atoms_table = atoms_table
        self.__sym_table = sym_table
        self.__special_ids = {
            "id" : self.__atoms_table.search("id")[1],
            "int_const" : self.__atoms_table.search("int_const")[1],
            "float_const" : self.__atoms_table.search("float_const")[1]
        }


    def __get_next_token(self, code):
        matches = [
              ('keyword',       re.match(r"(while|break|continue|if|scan|print)", code) )
            , ('type',          re.match(r"(int|float|char)", code) )
            , ('opt_keyword',   re.match(r"(return|exit)", code) )
            , ('id',            re.match(r"([$_a-zA-Z][$_a-zA-Z0-9]*)", code) )
            , ('parantheses',   re.match(r"([)(])", code) )
            , ('separator',     re.match(r"([;,])", code) )
            , ('sign',          re.match(r"([=+\-*/%><]|==|>=|<=)", code) )
            , ('curly_brace',   re.match(r"([{}])", code) )
            , ('int_const',     re.match(r"([0-9]+)([^$_a-zA-Z0-9]+|$)", code) )
            , ('float_const',   re.match(r"([0-9]+[.][0-9]+)([^$_a-zA-Z0-9]+|$)", code) )
        ]
        _type, match_obj = max(matches, key = lambda t : 0 if t[1] is None else len(t[1].group(1)))
        return (_type, match_obj.group(1)) if match_obj is not None else ('invalid', None)


    def __tokenize(self, code):
        result = []
        code = code.strip()
        index = 1
        while code:
            tok_code = 0
            tok_type, token = self.__get_next_token(code)
            if token is None:
                raise TokenizerException(f"Invalid token {index}")
            if tok_type in ['id', 'int_const', 'float_const']:
                if tok_type == "id" and len(token) > 8:
                    raise TokenizerException(f"Length of token '{token}' too large")
                tok_val, id_code = self.__sym_table.add(token)
                # separate if statements for performance optimizations
                tok_code = self.__special_ids[tok_type]
                result += [(tok_type, token, tok_code, id_code)]
            else:
                tok_val, tok_code = self.__atoms_table.search(token)
                result += [('symbol', token, tok_code)]

            code = code[len(token):].strip()
            index += 1
            #print(f"[DEBUG] current code to tokenize: {code}")

        return result

    def get_all_tokens(self, code):
        result = []
        index = 1
        for line in code:
            try:
                result += self.__tokenize(line)
                index += 1
            except TokenizerException as te:
                raise TokenizerException(f"{te} at line {index}")
        return result

    def print_internal_form(self, code):
        print(Fore.YELLOW + "Tokens in code:")
        print("    Token      Atom value   SymTable value")
        for t in code:
            #print(t)
            if t[0] == 'symbol':
                print(Fore.GREEN + f"    {t[1]:10} {t[2]:<12} -")
            else:
                print(Fore.MAGENTA + f"    {t[1]:10} {t[2]:<12} {t[3]}")
    
    def print_current_sym_table(self):
        print(Fore.YELLOW + "Symbol table:")
        self.__sym_table.print_elems('Code of symbol', 'Symbol')

if __name__ == "__main__":
    r = RegexLexer(None, None)
    #print(r._RegexLexer__tokenize("scan(a,   b  , c )  ;   "))
    print(repr(r._RegexLexer__get_next_token("int a,b,c;")))
    print(repr(r._RegexLexer__get_next_token(",b,c);")))
    print(repr(r._RegexLexer__get_next_token("scan(a,b,c);")))
    print(repr(r._RegexLexer__get_next_token("return 0;")))
    print(repr(r._RegexLexer__get_next_token("if(0<9)")))
    print(repr(r._RegexLexer__get_next_token(";if(0<9)")))
    print(repr(r._RegexLexer__get_next_token("manu+maria)")))
    print(repr(r._RegexLexer__get_next_token("<9)")))
    print(repr(r._RegexLexer__get_next_token("0{ioana;}")))
    print(repr(r._RegexLexer__get_next_token("  ;xxx;")))
    print(repr(r._RegexLexer__get_next_token("0;  ;xxx;")))
    print(repr(r._RegexLexer__get_next_token("(x)x=x-1;")))
    print(repr(r._RegexLexer__get_next_token("return0;")))