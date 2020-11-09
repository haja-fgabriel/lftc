if __name__ != "__main__":    
    from lexer.binary_tree import BinaryTree
    from lexer.errors import TokenizerException
    #from lexer.state_machine import StateMachine
    from state_machine.state_machine import StateMachine
else:
    from mock_state_machine import StateMachine
import re
import json
from colorama import *
from utils.constants import *


class Lexer:
    def __init__(self, atoms_table, sym_table):
        self.__atoms_table__ = atoms_table
        self.__sym_table__ = sym_table
        self.__special_ids__ = {
            "id" : self.__atoms_table__.search("id")[1],
            "int_const" : self.__atoms_table__.search("int_const")[1],
            "float_const" : self.__atoms_table__.search("float_const")[1]
        }
    
    def __get_next_token__(self, code):
        raise NotImplementedError("Please implement this method in your class")

    def __tokenize__(self, code):
        result = []
        code = code.strip()
        index = 1
        while code:
            tok_code = 0
            tok_type, token = self.__get_next_token__(code)
            if token is None:
                raise TokenizerException(f"Invalid token {index}")
            if tok_type in ['id', 'int_const', 'float_const']:
                if tok_type == "id" and len(token) > 8:
                    raise TokenizerException(f"Length of token '{token}' too large")
                tok_val, id_code = self.__sym_table__.add_or_get(token)
                
                # separate if statements for performance optimizations
                # so that the atom code for IDs and constants won't be calculated everytime
                tok_code = self.__special_ids__[tok_type]
                result += [(tok_type, token, tok_code, id_code)]
            else:
                tok_val, tok_code = self.__atoms_table__.search(token)
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
                result += self.__tokenize__(line)
                index += 1
            except TokenizerException as te:
                raise TokenizerException(f"{te} at line {index}")
        return result

    def print_internal_form(self, code):
        print(Fore.YELLOW + "Tokens in code:")
        print("    Atom value   SymTable value")
        for t in code:
            #print(t)
            if t[0] == 'symbol':
                print(Fore.GREEN + f"    {t[2]:<12} -")
            else:
                print(Fore.MAGENTA + f"    {t[2]:<12} {t[3]}")
    
    def print_current_sym_table(self):
        print(Fore.YELLOW + "Symbol table:")
        self.__sym_table__.print_elems('Code of symbol', 'Symbol', color=Fore.MAGENTA)

class MockLexer(Lexer):
    def __init__(self, atoms_table, sym_table):
        super().__init__(atoms_table, sym_table)
    
    def get_all_tokens(self, code):
        result = []
        index = 0
        for line in code:
            index += 1

            tokens = line.split(' ')
            for token in tokens:
                data = self.__atoms_table__.search(token)

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


class RegexLexer(Lexer):
    def __init__(self, atoms_table, sym_table):
        super().__init__(atoms_table, sym_table)

    def __get_next_token__(self, code):
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



class StateMachineLexer(Lexer):
    def __init__(self, atoms_table, sym_table, config="config.json"):
        self.__config_file__ = config
        self.__state_machines__ = {}
        self.__prepare_state_machines()
        super().__init__(atoms_table, sym_table)
    
    def __prepare_state_machines(self):
        with open(self.__config_file__, "r") as f:
            config = json.load(f)
            base_path = config["base_path"]
            default_folder = config["state_machines"]["base_path"]
            max_len = config["state_machines"]["max_identifier_length"]
            for _type, filename in config["state_machines"]["filenames"].items():
                try:
                    ml = max_len if _type in ['id'] else MAX_SEQUENCE_LENGTH
                    self.__state_machines__[_type] = StateMachine.read_file(f"{base_path}\{default_folder}\{filename}", ml)
                    # print(_type + ' ' + filename)
                except Exception as e: pass

    def __get_next_token__(self, code):
        # TODO modify matching functions
        matches = [
              ('keyword',       self.__state_machines__['keyword'].get_longest_prefix(code) )
            , ('type',          self.__state_machines__['type'].get_longest_prefix(code) )
            , ('opt_keyword',   self.__state_machines__['opt_keyword'].get_longest_prefix(code) )
            , ('id',            self.__state_machines__['id'].get_longest_prefix(code) )
            , ('parantheses',   self.__state_machines__['parantheses'].get_longest_prefix(code) )
            , ('separator',     re.match(r"([;,])", code) )
            , ('sign',          self.__state_machines__['sign'].get_longest_prefix(code) )
            , ('curly_brace',   self.__state_machines__['curly_brace'].get_longest_prefix(code) )
            , ('int_const',     self.__state_machines__['int_const'].get_longest_prefix(code) )
            , ('float_const',   self.__state_machines__['float_const'].get_longest_prefix(code) )
        ]
        _type, what = max(matches, key=lambda t: 0 if t[1] is None else (len(t[1]) if type(t[1]) != re.Match else len(t[1].group(1))))
        return ('invalid', None) if what is  None else ((_type, what) if type(what) != re.Match else (_type, what.group(1)) ) 

if __name__ == "__main__":
    r = StateMachineLexer(None, None)
    #print(r._RegexLexer__tokenize("scan(a,   b  , c )  ;   "))
    print(repr(r._StateMachineLexer__get_next_token("int a,b,c;")))
    print(repr(r._StateMachineLexer__get_next_token(",b,c);")))
    print(repr(r._StateMachineLexer__get_next_token("scan(a,b,c);")))
    print(repr(r._StateMachineLexer__get_next_token("return 0;")))
    print(repr(r._StateMachineLexer__get_next_token("if(0<9)")))
    print(repr(r._StateMachineLexer__get_next_token(";if(0<9)")))
    print(repr(r._StateMachineLexer__get_next_token("manu+maria)")))
    print(repr(r._StateMachineLexer__get_next_token("<9)")))
    print(repr(r._StateMachineLexer__get_next_token("0{ioana;}")))
    print(repr(r._StateMachineLexer__get_next_token("  ;xxx;")))
    print(repr(r._StateMachineLexer__get_next_token("0;  ;xxx;")))
    print(repr(r._StateMachineLexer__get_next_token("(x)x=x-1;")))
    print(repr(r._StateMachineLexer__get_next_token("return0;")))