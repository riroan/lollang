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
    SWAP = auto()
    
    COMMENT = auto()
    CLOSE = auto() # loop out
    
    LT = auto() # <
    LE = auto() # <=
    GT = auto() # >
    GE = auto() # >=
    
class TYPE(Enum): # 자료형
    INT = auto()
    STR = auto()
    
class Operator:
    ONE = "ㅠ"
    ADD = "ㅜ"
    SUB = "ㅡ"
    MUL = "ㅓ"
    DIV = "ㅏ"
    INT_DIV = "ㅕ"
    REM = "ㅑ"
    op = ["+","-","*","/","//","%"]
    
    @staticmethod
    def getOp():
        return [Operator.ADD, Operator.SUB,Operator.MUL,Operator.DIV,Operator.INT_DIV,Operator.REM]

class Variable:
    def __init__(self):
        self.var = dict()
    
    def insert(self, name):
        try:
            self.var[name]
        except:
            self.var[name] = [f"var_{len(self.var)}", TYPE.INT]
    
    def get(self, name):
        try:
            return self.var[name][0]
        except:
            print(f">> Error : 그런 변수명이 없습니다. {name}")
            return False
    
    def getType(self, name):
        try:
            return self.var[name][1]
        except:
            print(f">> Error : 그런 변수명이 없습니다. {name}")
            return False
    
    def setType(self, name, newType):
        self.var[name][1] = newType


class Compiler:
    def __init__(self):
        self.codes = list()
        self.stack = list()
        self.out = list()
        
        self.valid = False
        self.indent = 0
        self.var = Variable()
        
    def getNewLine(self):
        return "\t"*self.indent
    
    def save(self, path = "a.py"):
        with open(path, "w") as file:
            for code in self.out:
                file.write(code+"\n")
    
    def checkComment(self, code):
        ix = code.find("잠만")
        if ix>=0:
            code = code[ix:]
        return code
    
    def getType(self, code):
        if "스왑좀" in code:
            return Keyword.SWAP
        if "캐리좀" in code:
            return Keyword.VAR_ASSIGN
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
        if "뭐함?" in code:
            return Keyword.CLOSE
        if "잠만" in code:
            return Keyword.COMMENT
        if "님" in code:
            return Keyword.VAR_DECLARE
    
    def removeDeclare(self, elements): # 선언과 동시에 입력, 대입시 "님" 제거
        return [element[:-1] if element[-1] == '님' else element for element in elements]
        
    def varCheck(self, elements):
        for element in elements:
            if element[-1] == "님":
                self.var.insert(element[:-1])
            elif not self.var.get(element):
                print(f">> Error : 그런 변수명이 없습니다. {element}")
                return False
        return True
    
    def varDeclare(self, code):
        out = self.getNewLine()
        code = code.replace(" ", "")
        name = code[:code.find("님")]
        self.var.insert(name)
        self.out.append(out + f"{self.var.get(name)} = 0")
        print(f"변수 {name}({self.var.get(name)}) 선언!!")
    
    def varInput(self, code):
        out = self.getNewLine()
        elements = code.split()[:-1]
        
        if not self.varCheck(elements):
            # 컴파일 에러
            print(">> 변수가 없는게 있습니다!!")
            pass
        elements = self.removeDeclare(elements)
        if len(elements) == 1:
            out += f"{self.var.get(elements[0])} = int(input())"
        else:
            out += f"{self.var.get(elements[0])}"
            for element in elements[1:]:
                out += f", {self.var.get(element)} = map(int, input().split())"
        self.out.append(out)
        print(f"변수 {elements}({[self.var.get(i) for i in elements]}) 입력!!")
    
    def varPrint(self, code):
        out = self.getNewLine()
        out += "print("
        elements = code.split()[:-1]
        if not self.varCheck(elements):
            # 컴파일 에러
            pass
        out+=f"{self.var.get(elements[0])}"
        if len(elements) == 1:
            out+=")"
        else:
            for element in elements[1:]:
                out+=f", {self.var.get(element)}"
            out+=")"
        self.out.append(out)
        print(f"변수 {elements}({[self.var.get(i) for i in elements]}) 출력!!")
    
    def varSwap(self, code):
        elements = code.split()[:-1]
        if not self.varCheck(elements):
            # 컴파일 에러
            pass
        for element in elements:
            out = self.getNewLine()
            var_type = self.var.getType(element)
            if var_type == TYPE.INT:
                out += f"{self.var.get(element)} = chr({self.var.get(element)})"
                self.var.setType(element, TYPE.STR)
            elif var_type == TYPE.STR:
                out += f"{self.var.get(element)} = ord({self.var.get(element)})"
                self.var.setType(element, TYPE.INT)
            else:
                print(">> 잘못된 타입입니다.")
            self.out.append(out)
            
    def makeAssignStmt(self, code, ix = 0):
        stmt = ""
        op = Operator.getOp()
        if ix == len(op):
            element = code
            l = len(element)
            if element[0] == Operator.ONE:
                if element.count(Operator.ONE) != l:
                    # 컴파일에러
                    print(">> 변수 대입이 잘못되었습니다.")
                    pass
                else:
                    stmt+=f"{l}"
            else:
                stmt+=f"{self.var.get(element)}"
            return stmt
            
        elements = code.split(op[ix])
        l = len(elements)
        for i, element in enumerate(elements):
            stmt += self.makeAssignStmt(element, ix+1)
            if i < l-1:
                stmt += Operator.op[ix]
        return stmt

    def varAssign(self, code):
        out = self.getNewLine()
        elements = code.split(" ")
        if not self.varCheck([elements[0]]):
            # 컴파일 에러
            pass
        variable = self.removeDeclare([elements[0]])[0]
        out += f"{self.var.get(variable)} = "
        out += self.makeAssignStmt(elements[-1])
        self.out.append(out)
    
    def compileLine(self, code):
        code = self.checkComment(code)
        if self.isEmptyLine(code):
            return
        TYPE = self.getType(code)
        if TYPE == Keyword.VAR_DECLARE:
            self.varDeclare(code)
        if TYPE == Keyword.VAR_ASSIGN:
            self.varAssign(code)
        if TYPE == Keyword.VAR_PRINT:
            self.varPrint(code)
        if TYPE == Keyword.VAR_INPUT:
            self.varInput(code)
        if TYPE == Keyword.SWAP: # 아스키를 숫자로 변환
            self.varSwap(code)
        
    
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
    
    def run(self, path = "a.py"):
        try:
            exec(open(path).read())
        except:
            print("소환사 한명이 게임을 종료했습니다.")
            print(">> 런타임 에러")


if __name__ == "__main__":
    compiler = Compiler()
    compiler.compileFile("main.lo")
    compiler.save()
    print(compiler.out)
    compiler.run()