import re
import json



op = '/*-+^()'


def process_eq(eq):
    eq = list(eq)
    eq_len = len(eq)
    i = 0
    while i < eq_len-1:
        if eq[i] in op:
            if eq[i-1]!=' ' and eq[i][0]!= ' ':
                eq[i] = ' '+eq[i]
            if eq[i + 1] != ' ' and eq[i][-1]!= ' ':
                eq[i] = eq[i]+' '
        i += 1
    return ''.join(eq)




def extract_last_sentence(text):
    # 用句号分割文本成句子列表
    sentences = text.split('．')
    if sentences[-1] == '':
        sentences = sentences[:-1]

    last_sen = sentences[-1]
    last_sen_list = last_sen.split('，')

    question = last_sen_list[-1]


    # 重新构建前面的句子
    if len(last_sen_list)!=1:
        remaining_text = '，'.join(last_sen_list[:-1])
    else:
        remaining_text = last_sen_list[-1]

    if len(sentences)!=1:
        remaining_text = '．'.join(sentences[:-1]) + remaining_text
    else:
        remaining_text = remaining_text

    return remaining_text, question



def process_data(text, equ):
    # 输入的文本


    sce,question = extract_last_sentence(text)
    equ = ' '+equ.replace('**','^')+' '

    # print(sce)
    # print(q)

    # 定义正则表达式
    pattern = r'\d+(?:\.\d+)?%?|\(\d+\/\d+\)'

    # 使用正则表达式找到匹配的数字
    matches = re.finditer(pattern, sce)

    # 创建一个字典来存储数字到符号的映射
    number_to_symbol = {}
    symbol_counter = 0



    # 遍历匹配的数字
    symbol_text = sce  # 创建一个副本用于替换
    for match in matches:
        value = match.group()  # 获取匹配的字符串值
        # start_index = match.start()  # 获取起始索引
        # end_index = match.end()  # 获取结束索引
        #
        # print(f"找到数字：{value}")
        # print(f"起始索引：{start_index}")
        # print(f"结束索引：{end_index}")


        if value not in number_to_symbol.keys():
            symbol = f" number{symbol_counter} "
            number_to_symbol[value] = symbol
            symbol_counter += 1


    # 定义一个函数，用于将匹配的数字替换为字典中的对应值
    def replace_number(match):
        number = match.group(0)
        return number_to_symbol.get(number, number)


    # 使用正则表达式进行替换
    result = re.sub(pattern, replace_number, sce)
    equ_re = re.sub(pattern, replace_number, equ)


    for each_key in number_to_symbol.keys():
        value =  number_to_symbol[each_key]
        number_to_symbol[each_key] = value[1:-1]
    equ_re= process_eq(equ_re).strip()
    #print(number_to_symbol)
    return question, result , equ_re, number_to_symbol

"""
data format
{"question": "一个超市购进5吨大米，5天卖出2000千克，还剩多少千克？", "answer": "x=(5*1000)-2000=3000"}
"""

if __name__ == '__main__':
    data = []
    index  = 0
    with open('data.json', 'r') as file:
        for line in file:
            line = eval(line)
            each_dic = {}
            each_dic['index'] = str(index)
            each_dic['problem'] = line['question']
            each_dic['equation'] = line['answer'].split('=')[1]
            each_dic['answer'] = line['answer'].split('=')[-1]
            each_dic['question'],each_dic['problem_sym'],each_dic['equ_sym'],each_dic['num2sym'] = \
                process_data(each_dic['problem'], each_dic['equation'])
            data.append(each_dic)
            index += 1

    with open('data_process.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)




