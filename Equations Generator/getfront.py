op = [')','(','+','-','*','/']

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def isEmpty(self):
        return self.items == []

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[-1]

    def __str__(self):
        return '{}←'.format(self.items)


def inputProcess(inputString):
    '''将输入的字符串转化为包含操作数和操作符的列表'''
    resList = []
    tmp = ''  # 用于保存多位的数字时的中间结果
    for ele in inputString:
        if  ele not in op: # 能处理小数点的情况
            tmp += str(ele)
        else:
            if tmp != '':
                resList.append(tmp)
                tmp = ''
            resList.append(ele)
    if tmp != '':
        resList.append(tmp)
    return resList

def sub_inputProcess(inputString):
    '''将输入的字符串转化为包含操作数和操作符的列表'''
    resList = []
    tmp = ''  # 用于保存多位的数字时的中间结果
    for ele in inputString:
        if  ele not in op: # 能处理小数点的情况
            tmp += str(ele)
        else:
            if tmp != '':
                resList.append(tmp)
                tmp = ''
            resList.append(ele)
    if tmp != '':
        resList.append(tmp)

    op_num = {'+':0,'-':0,'*':0,'/':0}
    for i,each in enumerate(resList):
        if each in '+*/-':
            resList[i] = each + str(op_num[each])
            op_num[each] += 1

    return resList

#
def inToPreExp(epxString):
    expList = inputProcess(epxString)
    s = Stack()
    optPriorityDict = {')': 0, '+': 1, '-': 1, '*': 2, '/': 2}  # 操作符优先级字典
    res = []  # 保存结果
    for ele in expList[::-1]:  # 逆序扫描列表
        if ele not in op:  # 1数字直接添加进结果字符串
            res.insert(0, ele)  # 为保证数字顺序,所有从左边插入进结果列表
        elif ele == ')':  # 2.右括号压栈
            s.push(ele)
        elif ele == '(':  # 3.左括号,连续出栈直到右括号,并追加到结果字符串
            top = s.pop()
            while top != ')':
                res.insert(0, top)
                top = s.pop()
        elif ele[0] in '+-*/':  # 4 操作符和栈顶元素比较优先级
            while (not s.isEmpty() and optPriorityDict[s.peek()] >= optPriorityDict[ele]):  # 当前栈顶元素的优先级大于等于扫描到的运算符
                res.insert(0, s.pop())  # 出栈并插入结果列表
            s.push(ele)  # 入栈

    while not s.isEmpty():
        res.insert(0, s.pop())

    return res

def sub_inToPreExp(epxString):
    expList = sub_inputProcess(epxString)
    s = Stack()
    optPriorityDict = {')': 0, '+': 1, '-': 1, '*': 2, '/': 2}  # 操作符优先级字典
    res = []  # 保存结果
    for ele in expList[::-1]:  # 逆序扫描列表
        if ele[0] not in op:  # 1数字直接添加进结果字符串
            res.insert(0, ele)  # 为保证数字顺序,所有从左边插入进结果列表
        elif ele == ')':  # 2.右括号压栈
            s.push(ele)
        elif ele == '(':  # 3.左括号,连续出栈直到右括号,并追加到结果字符串
            top = s.pop()
            while top != ')':
                res.insert(0, top)
                top = s.pop()
        elif ele[0] in '+-*/':  # 4 操作符和栈顶元素比较优先级
            while (not s.isEmpty() and optPriorityDict[s.peek()[0]] >= optPriorityDict[ele[0]]):  # 当前栈顶元素的优先级大于等于扫描到的运算符
                res.insert(0, s.pop())  # 出栈并插入结果列表
            s.push(ele)  # 入栈

    while not s.isEmpty():
        res.insert(0, s.pop())

    return res

