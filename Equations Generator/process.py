import json
from exp2Tree import inToPreExp
from exp_process import middle2Final






if __name__ == '__main__':

    json_data = json.load(open('Unbias_train.json', encoding='utf-8'), strict=False)
    new_data = []
    for each in json_data:
        new_each = {}
        new_each['id'] = each['id']
        new_each['text'] = each['text']

        new_each['annotations'] = []
        for each_qa in each['annotations']:
            new_each_qa = {}
            new_each_qa['Q'] = each_qa['Q']
            new_each_qa['A'] = inToPreExp(each_qa['A'])
            new_each['annotations'].append(new_each_qa)
        new_data.append(new_each)


with open('Unbias_train_front.json', 'w', encoding='utf-8') as file_obj:
  json.dump(new_data, file_obj, ensure_ascii=False, indent=2)