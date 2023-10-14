import csv
import json
import sys

sys.path.append( '  ' )
from getfront import sub_inToPreExp,inToPreExp


each_exp = ""
qua = ['number0','number1','number2','number3','number4','number5','number6','number7','number8','number9','number10','number11','number12','number13','number14']
op = ['/','*','-','+']

num2le = {0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h',8:'i',9:'j'}
le2num = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7,'i':8,'j':9}

class Stack(object):#用列表实现栈
    def __init__(self):	#实例化栈
        self.list = []
    def isEmpty(self):#判断栈空
        return self.list == []
    def push(self, item):#入栈
        self.list.append(item)
    def pop(self):#出栈
        return self.list.pop()
    def top(self):#返回顶部元素
        return self.list[len(self.list)-1]
    def size(self):#返回栈大小
        return len(self.list)

# 前缀表达式求值
def pretomid(list):
    s = Stack()
    op = []
    for par in list:
        if par in "+-*/":#遇到运算符则入栈
            s.push(par)
        else:   #为数字时分两种情况：
            if s.top() in '+-*/':#栈顶为运算符
                s.push(par)#数字入栈
            else:#当前栈顶为数字
                while (not s.isEmpty()) and (not s.top() in '+-*/'):#若栈不空，且当前栈顶为数字，则循环计算
                    shu = s.pop()#运算符前的数字出栈
                    fu = s.pop()#运算符出栈
                    if len(op)!=0 and op[-1] in ['+','-'] and fu in ['*','/']:
                        par = shu + fu +'(' + par + ')'
                    else:
                        par = shu + fu + par
                    op.append(fu)

                s.push(str(par))#算式入栈
    return s.pop()#返回最终算式

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def __init__(self):
        self.exp = []

    def buildTree(self, preorder, inorder):

        if not preorder:
            return None

        root = TreeNode(preorder[0])
        left_inorder = inorder[: inorder.index(root.val)]
        right_inorder = inorder[inorder.index(root.val) + 1:]

        l_left = len(left_inorder)
        left_preorder = preorder[1:l_left + 1]
        right_preorder = preorder[l_left + 1:]

        root.left = self.buildTree(left_preorder, left_inorder)
        root.right = self.buildTree(right_preorder, right_inorder)

        return root

    def print_tree(self, root):
        if root.left != None:
            if root.left.val[0] in ['-','+'] and root.val[0] in ['*','/']:
                self.exp.append('(')
                self.print_tree(root.left)
                self.exp.append(')')
            else:
                self.print_tree(root.left)


        self.exp .append(root.val)
        if root.right != None:
            if root.right.val[0] in ['-', '+'] and root.val[0] in ['*', '/']:
                self.exp.append('(')
                self.print_tree(root.right)
                self.exp.append(')')
            else:
                self.print_tree(root.right)

def get_middle_exp(inputString):
    '''将输入的字符串转化为包含操作数和操作符的列表'''
    inputString = inputString.replace('(','').replace(')','')
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

sub_exp = []
def get_Tree_exp(Tree):
    if Tree.val[0] in op:
        s = Solution()
        s.print_tree(Tree)
        want_exp = s.exp
        for i,each in enumerate(want_exp):
            if each[0] in '/*-+':
                want_exp[i] = each[0]
        sub_exp.append(''.join(want_exp))
    else:
        return
    if Tree.left != None:
        get_Tree_exp(Tree.left)
    if Tree.right != None:
        get_Tree_exp(Tree.right)

def get_subexp(exp):
    #传入表达式得到所有子式
    a = get_middle_exp(exp)

    b = sub_inToPreExp(exp)

    Tree = Solution().buildTree(preorder=b, inorder=a)
    get_Tree_exp(Tree)

    return sub_exp[1:]

def choose_two_exp(quas):
    #任意两个变量组成的子式
    exp_set = []
    for i in range(len(quas)):
        for j in range(len(quas[i:])):
            for each in op:
                exp_set.append(quas[i] + each + quas[i+j])
                if quas[i]!=quas[i+j]:
                    exp_set.append(quas[i+j] + each + quas[i])
    return exp_set


#相同单位的处理
def sub_same_unit(same_unit):

    Len = len(same_unit)
    i = 0
    while i<Len-1:
        j = i+1
        while j<Len:
            same_unit.append(same_unit[i] + ['+'] + same_unit[j])
            same_unit.append(same_unit[i] + ['-'] + same_unit[j])
            same_unit.append(same_unit[j] + ['-'] + same_unit[i])
            same_unit.append(same_unit[i] + ['/'] + same_unit[j])
            same_unit.append(same_unit[j] + ['/'] + same_unit[i])
            j+=1
        i+=1
    return same_unit


def choose_from_unit(sentence, qua_list):
    exp_list = []

    unit_list = {}
    unit_list['else'] = []
    unit_list['times'] = []
    sentence_list = sentence.split(' ')
    # print(sentence_list)
    for each_num in qua_list:
        index = sentence_list.index(each_num)
        #如果一句话的最后不是数字（找不到单位）或者其数字对应的单位不是符号或者倍数
        if index != len(sentence_list)-1 and sentence_list[index+1][0] not in ',.?，。、？．: ：）)(（%倍+/*-':
            if sentence_list[index+1][0] not in unit_list.keys():
                unit_list[sentence_list[index+1][0]] = [[each_num]]
            else:
                unit_list[sentence_list[index+1][0]].append([each_num])
        elif sentence_list[index+1][0] in '%倍':
            unit_list['times'].append([each_num])
        else:
            unit_list['else'].append([each_num])

    for each_key in unit_list.keys():
        if each_key =='else' or each_key=='times':
            pass
        elif len(unit_list[each_key])>1:
            #相同单位表达式
            unit_list[each_key] = sub_same_unit(unit_list[each_key])



    #TODO
    # unit_list = {'else': [], 'times': [['number1']],'页': [['number0'], ['number2'], ['number0', '+', 'number2'], ['number0', '-', 'number2'],['number2', '-', 'number0'], ['number0', '/', 'number2'], ['number2', '/', 'number0']]}
    # print(unit_list)

    print(unit_list)

    dic_list = list(unit_list.keys())[1:]
    Len = len(dic_list)
    i = 0
    while i<Len-1:
        j = i+1
        while j<Len:
            for each_num in unit_list[dic_list[i]]:
                for each_num2 in unit_list[dic_list[j]]:
                    if len(each_num)!=1:
                        if '+' in each_num or '-' in each_num:
                            if len(each_num2)==1:
                                exp_list.append(each_num2[0] + '*' + '(' + ''.join(each_num) + ')')
                                exp_list.append(each_num2[0] + '/' + '(' + ''.join(each_num) + ')')
                                exp_list.append('(' + ''.join(each_num) + ')' + '/' + each_num2[0])
                        else:
                            continue

                    else:

                        if len(each_num2)==1:
                            exp_list.append(each_num[0] + '*' + each_num2[0])
                            exp_list.append(each_num[0] + '/' + each_num2[0])
                            exp_list.append(each_num2[0] + '/' + each_num[0])
                        else:
                            if '+'  in each_num2 or '-' in each_num2:
                                exp_list.append(each_num[0] + '*' + '(' + ''.join(each_num2) + ')')
                                exp_list.append(each_num[0] + '/' + '(' + ''.join(each_num2) + ')')
                                exp_list.append('(' + ''.join(each_num2) + ')' + '/' + each_num[0])
                            else:
                                continue
            j+=1
        i+=1

    for each_key in dic_list:
        for each_num in unit_list[each_key]:
            if len(each_num)!=1:
                exp_list.append(''.join(each_num))

    print(exp_list)

    #
    # print(unit_list)
    # print(exp_list)
    return exp_list



if __name__ == '__main__':
#E:\NLP\论文阅读\数学题求解\Robustness\UnbiasedMWP-master\process_data\nezha_data   得到前缀表达式

    new_data = []
    want_data = []
    json_data = json.load(open('train_src.json', encoding='utf-8'))
# json_data[0]: {'id': 'a2ff2d7dbe8c11eb95dd04d4c4250d10', 'original_text': '一箱蜜蜂一个月大约产6千克蜂蜜，蛋糕房现需要126千克蜂蜜，大约需要多少箱蜜蜂？',
#  'context': '一箱蜜蜂一个月大约产6千克蜂蜜，蛋糕房现需要126千克蜂蜜，', 'nums': '6 126', 'question': '大约需要多少箱蜜蜂？',
#  'output_infix': 'N1 / N0', 'output_prefix': '/ N1 N0', 'output_original': 'x=126/6', 'interpretation': {}}


    for i,each in enumerate(json_data):
        nums = each['nums'].split(' ')

        nums_dict = {}
        for j,each_num in enumerate(nums):
            nums_dict[each_num] = j
        num_sort = sorted(nums,key = lambda i:len(i),reverse=True)
        problem = each['context']
        for j,each_num in enumerate(num_sort):
            problem = problem.replace(each_num, ' temp_'+num2le[nums_dict[each_num]]+' ')

        for each_key in le2num.keys():
            problem = problem.replace('temp_'+each_key,'number'+str(le2num[each_key]))

        #将题干里面的数字换成了number0、number1的形式
        print(problem)


        Equation = each['output_infix'].replace('N','number').replace(' ','')
        #equation也得到相同形式 将数字换成number0 number1

        # exit()
        #
        # Equation = ''.join(each["target_template"])[2:].replace('temp_a', 'number0').replace('temp_b',
        #                                                                                      'number1').replace(
        #     'temp_c', 'number2').replace('temp_d', 'number3').replace('temp_e', 'number4').replace('temp_f',
        #                                                                                            'number5').replace(
        #     'temp_g', 'number6').replace('temp_e', 'number4').replace('temp_f', 'number5').replace('temp_g',
        #                                                                                            'number6').replace(
        #     'temp_e', 'number4').replace('temp_f', 'number5').replace('temp_g', 'number6').replace('temp_h',
        #                                                                                            'number7').replace(
        #     'temp_i', 'number8').replace('temp_j', 'number9').replace('temp_k', 'number10').replace('temp_l',
        #                                                                                             'number11').replace(
        #     'temp_m', 'number12').replace('PI', '3.14').replace('temp_n', 'number13').replace('temp_o', 'number14')
        # if '^' in Equation or '^' in row[-2]:
        #     continue
        # else:
        new_each = {}
        new_each['id'] = i
        new_each['text'] = problem
        exp = Equation
        qua_list = []
        A_set = []
        for each_qua in qua:
            if each_qua in problem:
                qua_list.append(each_qua)

        #按unit得到表达式
        sub_exp_uni = choose_from_unit(problem,qua_list)


        # sub_exp1 = choose_two_exp(qua_list)
        sub_exp = []

        #得到子表达式
        sub_exp2 = get_subexp(exp)

        A_set = sub_exp_uni + sub_exp2
        A_set = list(set(A_set))
        if len(A_set)!=0:
            new_each['annotations'] = []
            for each in A_set:
                new_each['annotations'].append({'Q':"", 'A':each})
            new_data.append(new_each)
        else:
            pass




    # with open('Unbias_train.json', 'w', encoding='utf-8') as file_obj:
    #   json.dump(new_data, file_obj, ensure_ascii=False, indent=2)