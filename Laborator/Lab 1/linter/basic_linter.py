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

    def lint(self, code):
        # TODO add additional linting procedures
        return self.__remove_comments(code)

