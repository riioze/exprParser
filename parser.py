


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

DOUBLE = {
    '+' : OP_PLUS,
    '-' : OP_MINUS,
    '*' : OP_MULT,
    '/' : OP_DIV
}

############   Class    ################


class part:
    def operate(self):
        assert False, 'not implemented yet'

class Number(part):
    def __init__(self,value):
        if '.' in value:
            self.value = float(value)
        else:
            self.value = int(value)
    def operate(self):
        return self.value
    def __repr__(self):
        return str(self.value)

class dOperator(part):
    def __init__(self,p1,p2,opFunc):
        self.p1 = p1
        self.p2 = p2
        self.opFunc = opFunc
    def operate(self):
        return self.opFunc(self.p1,self.p2)
    def __repr__(self):
        return f'op: {self.p1} {self.opFunc} {self.p2}'

############# Parser ###############

def split(string):
    nBuff = ''
    state = ''
    liste = []
    for c in string:
        if c in NUMBERS:
            nBuff+=c
            state = 'number'
        elif c in DOUBLE.keys():
            state = ''
            expBuff = c
        
        if state == '' and len(nBuff)>0:
            liste.append(nBuff)
            liste.append(expBuff)
            nBuff = ''
    if len(nBuff)>0:
        liste.append(nBuff)
    return liste


        

def parse(string):
    liste = split(string)
    Buff = []
    while '*' in liste:
        index = liste.index('*')
        liste[index] = dOperator(Number(liste[index-1]),Number(liste[index+1]),OP_MULT)
        liste.pop(index-1)
        liste.pop(index)
    return liste[0].operate()


