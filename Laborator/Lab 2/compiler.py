class Compiler:
    def __init__(self, linter, lexer):
        self.__linter = linter
        self.__lexer = lexer

    def compile(self, code):
        code = self.__linter.lint(code)
        print(code)
        code = self.__lexer.get_all_tokens(code)
        self.__lexer.print_current_sym_table()
        self.__lexer.print_internal_form(code)
        
        #print(f"{Fore.YELLOW + 'Found tokens:'} {Fore.BLUE + str(code)}")