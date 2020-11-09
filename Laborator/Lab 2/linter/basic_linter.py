from linter.ilinter import ILinter

class BasicLinter(ILinter):
    def __init__(self):
        pass

    def __remove_comments(self, code):
        result = []
        for line in code:
            try: line = line[:line.index('//')]
            except: pass
            if len(line.strip()) > 0:
                result += [line.strip()]

        return result
    
    def __remove_blank_lines(self, code):
        return [line for line in code if line.strip()]

    def lint(self, code):
        # TODO add additional linting procedures
        code = self.__remove_comments(code)
        return self.__remove_blank_lines(code)

