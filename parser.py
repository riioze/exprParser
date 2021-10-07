import re
from math import sqrt,cos,sin,tan

############   CONSTS   ###############

NUMBERS = '0123456789.'

############ op functions ##############

def OP_PLUS(p1,p2):
    return p1.operate()+p2.operate()
def OP_MINUS(p1,p2):
    return p1.operate()-p2.operate()
def OP_MULT(p1,p2):
    return p1.operate()*p2.operate()
def OP_DIV(p1,p2):
    return p1.operate()/p2.operate()
def OP_POW(p1,p2):
    return p1.operate()**p2.operate()
def OP_UNI_MINUS(p):
    return -p.operate()
def OP_SQRT(p):
    return sqrt(p.operate())
def OP_COS(p):
    return cos(p.operate())
def OP_SIN(p):
    return sin(p.operate())
def OP_TAN(p):
    return tan(p.operate())


DOUBLE = {
    '+' : OP_PLUS,
    '-' : OP_MINUS,
    '*' : OP_MULT,
    '/' : OP_DIV,
    '^' : OP_POW
}

SIMPLE = {
    '-' : OP_UNI_MINUS,
    'sqrt' : OP_SQRT,
    'cos' : OP_COS,
    'sin' : OP_SIN,
    'tan' : OP_TAN
}

VARIABLES = {
    
}
############   Class    ################


class part:
    """ global object for the parts"""
    def operate(self):
        assert False, 'not implemented yet'

class Number(part):
    """ objects containings the numbers"""
    def __init__(self,value):
        if '.' in value:
            self.value = float(value)
        else:
            self.value = int(value)
    def operate(self):
        return self.value
    def __repr__(self):
        return f' num: {self.value}'

class dOperator(part):
    """ object for the double operator containing the 2 parts"""
    def __init__(self,p1,p2,opFunc):
        self.p1 = p1
        self.p2 = p2
        self.opFunc = opFunc
    def operate(self):
        return self.opFunc(self.p1,self.p2)
    def __repr__(self):
        return f'op: {self.p1} {self.opFunc} {self.p2}'

class uOperator(part):
    """ object for the double operator containing the 2 parts"""
    def __init__(self,p,opFunc):
        self.p = p
        self.opFunc = opFunc
    def operate(self):
        return self.opFunc(self.p)
    def __repr__(self):
        return f'op: {self.opFunc} -> {self.p}'

class variable(part):
    def __init__(self,p):
        self.p = p
    def operate(self):
        return self.p.operate()
    def __repr__(self):
        return f'var: {self.p}'
tTypes = [Number,dOperator,uOperator,variable]
############# Parser ###############

def isToken(T):
    return type(T) in tTypes

def find_uni(liste):
    for x in range(len(liste)):
        if liste[x] in SIMPLE.keys():
            if isToken(liste[x+1]) and (x ==0 or not isToken(liste[x-1])):
                return x
    return -1

def find_variable(liste):
    for x in range(len(liste)):
        if liste[x] in VARIABLES.keys():
            return x
    return -1            

def split(string):
    """ splits the string in all sub parts"""
    regex = r'\d+|[\^\*\+\(\)/-=]|sqrt|cos|sin|tan|[^ ]'
    return re.findall(regex,string)


def token(liste):
    """ creates all the tokens"""
    
    #
    while find_variable(liste) != -1:
        index = find_variable(liste)
        liste[index] = VARIABLES[liste[index]]

    #execute parenthesis as sub parts using recursion
    while '(' in liste:
        pos1 = liste.index('(')+1
        pnum=1
        pos2 = pos1
        while pnum>0:
            if liste[pos2] == '(':
                pnum+=1
            elif liste[pos2] == ')':
                pnum-=1
            pos2+=1
        liste = liste[:pos1-1]+[token(liste[pos1:pos2-1])]+liste[pos2:]

    while find_uni(liste) != -1:
        uniPos = find_uni(liste)
        liste[uniPos] = uOperator(liste[uniPos+1],SIMPLE[liste[uniPos]])
        liste.pop(uniPos+1)

    while '^' in liste:
        index = liste.index('^')
        liste[index] = dOperator(liste[index-1],liste[index+1],OP_POW)
        liste.pop(index-1)
        liste.pop(index)

    # transforms the * and / into tokens
    while '*' in liste or '/' in liste:
        mindex,dindex = float('inf'),float('inf')
        if '*' in liste:
            mindex = liste.index('*')

        if '/' in liste:
            dindex = liste.index('/')
        if mindex>dindex:
            index = dindex
            liste[index] = dOperator(liste[index-1],liste[index+1],OP_DIV)
        else:
            index = mindex
            liste[index] = dOperator(liste[index-1],liste[index+1],OP_MULT)
        liste.pop(index-1)
        liste.pop(index)
    
    #transforms + and - into tokens
    while '+' in liste or '-' in liste:
        pindex,mindex = float('inf'),float('inf')
        if '+' in liste:
            pindex = liste.index('+')

        if '-' in liste:
            mindex = liste.index('-')
        if mindex>pindex:
            index = pindex
            liste[index] = dOperator(liste[index-1],liste[index+1],OP_PLUS)
        else:
            index = mindex
            liste[index] = dOperator(liste[index-1],liste[index+1],OP_MINUS)
        liste.pop(index-1)
        liste.pop(index)
    return liste[0]
        

def parse(string):
    """ parse the expression and return the result"""
    global VARIABLES
    liste = split(string)
    
    # convert num to tokens
    for x in range(len(liste)):
        if liste[x][0] in NUMBERS:
            liste[x] = Number(liste[x])
    


    if '=' in liste:
        index = liste.index('=')
        l,r = liste[:index],liste[index+1:]
        if '(' in l:
            pass
        else:
            VARIABLES[l[0]] = variable(token(r))

        return VARIABLES[l[0]].operate()
    
    





    return token(liste).operate()


