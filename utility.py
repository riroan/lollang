class Utility:
    def getNumLeftParenthesis(self, code):
        for i, v in enumerate(code):
            if v!="ㄴ":
                return i
        raise ValueError
    
    def getNumRightParenthesis(self, code):
        for i, v in enumerate(code[::-1]):
            if v!="ㄹ":
                return i
        raise ValueError
    
    def isEmptyLine(self, code):
        for i in code:
            if i != " ":
                return False
        return True
    
    def removeDeclare(self, elements): # 선언과 동시에 입력, 대입시 "님" 제거
        return [element[:-1] if element[-1] == '님' else element for element in elements]