from enum import Enum, auto

class Keyword(Enum):
    BLANK = auto()
    VAR_DECLARE = auto()
    VAR_ASSIGN = auto()
    VAR_PRINT = auto()
    VAR_INPUT = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    WHILE = auto()
    FUNCTION = auto()
    FOR = auto()
    
    COMMENT = auto()
    CLOSE = auto() # loop out
    
    LT = auto() # <
    LE = auto() # <=
    GT = auto() # >
    GE = auto() # >=

class Variable:
    def __init__(self):
        self.var = dict()
    
    def insert(self, name):
        try:
            self.var[name]
        except:
            self.var[name] = f"var_{len(self.var)}"
    
    def get(self, name):
        try:
            return self.var[name]
        except:
            print(">> Error : 그런 변수명이 없습니다.")
            return False


class Compiler:
    def __init__(self):
        self.codes = list()
        self.stack = list()
        self.out = list()
        
        self.valid = False
        self.indent = 0
        self.var = Variable()
    
    def save(self):
        with open("a.py", "w") as file:
            for code in self.out:
                file.write(code)
    
    def getType(self, code):
        if "갱좀" in code:
            return Keyword.VAR_PRINT
        if "리쉬좀" in code:
            return Keyword.VAR_INPUT
        if "저기" in code:
            return Keyword.IF
        if "아니" in code:
            return Keyword.FUNCTION
        if "님아" in code:
            return Keyword.FOR
        if "님" in code:
            return Keyword.VAR_DECLARE
        if "뭐함?" in code:
            return Keyword.CLOSE
        if "잠만" in code:
            return Keyword.COMMENT
    
    def varDeclare(self, code):
        code = code.replace(" ", "")
        name = code[:code.find("님")]
        self.var.insert(name)
        print(f"변수 {name}({self.var.get(name)}) 선언!!")
    
    def varInput(self, code):
        elements = code.split()[:-1]
        for element in elements:
            if not self.var.get(element):
                print(">> Error : 그런 변수명이 없습니다.")
                return
        if len(elements) == 1:
            out = f"{self.var.get(elements[0])} = input()"
        else:
            out = f"{self.var.get(elements[0])}"
            for element in elements[1:]:
                out += f", {self.var.get(element)} = map(str, input().split())"
        self.out.append(out)
        print(f"변수 {elements}({[self.var.get(i) for i in elements]}) 입력!!")
    
    def varPrint(self, code):
        pass
    
    def compileLine(self, code):
        if self.isEmptyLine(code):
            return
        TYPE = self.getType(code)
        if TYPE == Keyword.VAR_DECLARE:
            self.varDeclare(code)
        if TYPE == Keyword.VAR_PRINT:
            self.varPrint(code)
        if TYPE == Keyword.VAR_INPUT:
            self.varInput(code)
    
    def isEmptyLine(self, code):
        for i in code:
            if i != " ":
                return False
        return True
    
    def compile(self, codes):
        if codes[0] != "우리 잘해보죠" or codes[-1] != "팀차이 ㅈㅈ":
            print(">> Error : 코드형식을 확인하세요.")
            return
        codes = codes[1:-1]
        for code in codes:
            if self.isEmptyLine(code):
                continue
            self.compileLine(code)
    
    def compileFile(self, path):
        with open(path, "r", encoding="utf-8") as file:
            codelines = [i.rstrip() for i in file.readlines()]
            self.compile(codelines)


if __name__ == "__main__":
    compiler = Compiler()
    compiler.compileFile("main.lo")
    compiler.save()