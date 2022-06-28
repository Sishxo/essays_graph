# coding=utf-8
import json

from regex import P

def txtToJson():
    path = "E:\\Mywork\\txt2json\\keywords.txt" #txt文件地址
    with open(path,'r', encoding="utf-8") as file:
        seq = re.compile(":")
        result = []
        for line in file:
            lst = seq.split(line.strip())
            print(lst[0][1:6])
            if(lst[0][1:6] == "title"):
                print(lst[0])
            item = {
                "name":lst[0],
                "group": 1
            }
            result.append(item)
        print(type(result))
    with open('txtToJson.json', 'w') as dump_f:
        json.dump(result,dump_f)

def txtToJson1():
    path = "E:\\Mywork\\txt2json\\keywords.txt" #txt文件地址
    resultNodes = []
    resultEdges = []
    Vertex =[]
    count = -1
    with open(path,'r', encoding="utf-8") as file:
        for line in file.readlines():
            line_list = line.strip('\n').split('\n') 
            # print(line_list[0])
            if(line_list[0] != ''):
                count =  count + 1
                if(line_list[0][1:6] == "title"):
                    Vertex.append(count) #存储标题位置
                if(Vertex[-1] != count):
                    edges = {
                        "source": Vertex[-1],
                        "target": count,
                        "value": 2
                    }
                    resultEdges.append(edges)
                nodes = {
                    "name":line_list[0],
                    "group": 1
                }
                resultNodes.append(nodes)
                
    # print(Vertex)
    #标题连接规则
    for i in range(0,len(Vertex)-2):
        for k in range(i+1,i+2):
            edges = {
                "source": Vertex[i],
                "target": Vertex[k],
                "value": 20
            }
            print(edges)
            resultEdges.append(edges)
    # print(resultEdges)
      # print(resultEdges)
    with open('nodes.json', 'w') as dump_f:
        json.dump(resultNodes,dump_f)
    with open('edges.json', 'w') as dump_f:
        json.dump(resultEdges,dump_f)
    # print(len(Vertex))
if __name__ == '__main__':
    txtToJson1()