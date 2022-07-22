# coding=utf-8
import json
import difflib


def stringSimilarity(string1,string2):
    if difflib.SequenceMatcher(None,string1,string2).quick_ratio()>0.75:
        return 1
    else:
        return 0

def txtToJson():
    path = "../data/txt/keywords.txt"  # txt文件地址
    resultNodes = []
    resultEdges = []
    Vertex = []  # 存储标题
    count = -1  # 记录txt中行数
    with open(path, 'r', encoding="utf-8") as file:
        for line in file.readlines():
            line_list = line.strip('\n').split('\n')
            # print(line_list[0])
            if line_list[0] != '':
                count = count + 1  # 每读一行，计数器加一
                if line_list[0][1:6] == "title":
                    Vertex.append(count)  # 存储标题位置
                    nodes = {
                        "name": line_list[0],
                        "group": len(Vertex),
                        "title": 1
                    }
                elif line_list[0] == "[end]":
                    Vertex.append(count)
                else:
                    nodes = {
                        "name": line_list[0],
                        "count": 0

                    }
                if Vertex[-1] != count:  # 把关键词和标题连起来
                    edges = {
                        "source": Vertex[-1],
                        "target": count,
                        "value": 1
                    }
                    # print(edges)
                    resultEdges.append(edges)
                #print(nodes)
                resultNodes.append(nodes)


    # 标题连接规则
    for vertex_index, title_index in enumerate(Vertex[:-2]):
        # print("now",title_index)
        for keywords_index in range(title_index + 1, Vertex[vertex_index + 1]):
            title_name = resultNodes[title_index]["name"]
            title_group = resultNodes[title_index]["group"]
            keywords_json = resultNodes[keywords_index]
            keywords_name = keywords_json["name"]
            keywords_count = keywords_json["count"]
            for vertex_index_compare, title_index_compare in enumerate(Vertex[vertex_index+1:-1]):
                temp = Vertex[vertex_index+1:]
                for keywords_index_compare in range(title_index_compare + 1, temp[vertex_index_compare+1]):
                    local_same_count = 5
                    title_name_compare = resultNodes[title_index_compare]["name"]
                    keywords_json_compare = resultNodes[keywords_index_compare]
                    keywords_name_compare = keywords_json_compare["name"]
                    keywords_count_compare = keywords_json_compare["count"]
                    print(keywords_name + "::" + keywords_name_compare + "\n")
                    if stringSimilarity(keywords_name,keywords_name_compare):  # 遇到满足相似条件的关键词后，修改边长以及关键词所在nodes信息
                        # print(keywords_name,keywords_name_compare)
                        keywords_count = keywords_count + 1
                        keywords_count_compare = keywords_count_compare + 1
                        if local_same_count > 1:
                            local_same_count = local_same_count - 1
                        edges = {
                            "source": title_index,
                            "target": title_index_compare,
                            "value": local_same_count
                        }
                        nodes = {
                            "name": title_name_compare,
                            "group": title_group,
                            "title": 1
                        }
                        nodes_keywords = {
                            "name": keywords_name,
                            "count": keywords_count
                        }
                        nodes_keywords_compare = {
                            "name": keywords_name_compare,
                            "count": keywords_count_compare
                        }
                        print(edges)
                        resultNodes[title_index_compare] = nodes  # 根据聚类关系更新节点group
                        resultNodes[keywords_index] = nodes_keywords
                        resultNodes[keywords_index_compare] = nodes_keywords_compare
                        resultEdges.append(edges)  # 加入有相同关键词的文章连线

    '''for i in range(0,len(Vertex)-1):
        for k in range(i+1,i+2):
            edges = {
                "source": Vertex[i],
                "target": Vertex[k],
                "value": 20
            }
            print(edges)
            resultEdges.append(edges)'''
    # print(resultEdges)
    with open('../data/json/nodes.json', 'w') as dump_f:
        json.dump(resultNodes, dump_f)
    with open('../data/json/edges.json', 'w') as dump_f:
        json.dump(resultEdges, dump_f)
    # print(len(Vertex))


if __name__ == '__main__':
    txtToJson()
