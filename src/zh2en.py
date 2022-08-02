import json

from google_trans_new import google_translator


def zh_to_en(json_path, dest_path):
    Nodes = []
    with open(json_path, 'r') as file:
        nodes_json = json.load(file)
        translator = google_translator(timeout=10)
        for i, nodes in enumerate(nodes_json):
            # print(nodes['name'])
            nodes['name'] = translator.translate(nodes['name'], 'zh-CN')
            nodes_json[i]['name']=nodes['name']
            print(nodes_json[i])
    with open(dest_path, 'w') as dump_f:
        json.dump(nodes_json, dump_f)


if __name__ == '__main__':
    zh_to_en("../data/json/nodes1.json", '../data/json/nodes1_zh.json')
