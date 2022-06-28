from snownlp import SnowNLP
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import spacy
import pytextrank
import getAbstract
import pathlib


def get_en_keywords(text):
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")
    doc = nlp(text)

    '''for phrase in doc._.phrases[:5]:
        print(phrase.text)
        print(phrase.rank, phrase.count)
        print(phrase.chunks)'''
    return doc._.phrases


def get_zh_keywords(text):
    snlp = SnowNLP(text)
    print(snlp.keywords())
    print(snlp.summary())


def get_en_keywords_from_pdf(in_pdf_path, out_txt_path):
    getAbstract.parsePDF(in_pdf_path, out_txt_path)
    text = pathlib.Path(out_txt_path).read_text()
    temp=get_en_keywords(text)
    return temp


if __name__ == "__main__":
    '''temp=get_en_keywords_from_pdf("./essays/A Pixel-Level Meta-Learner for Weakly Supervised Few-Shot Semantic Segmentation.pdf",
                             "test.txt")
    for phrase in temp[:5]:
        print(phrase.text)
        with open("test2.txt","a",encoding="UTF-8") as f:
            for phrase in temp[:5]:
                f.write(phrase.text)
            f.write()'''
    with open("abstract.txt","r",encoding='UTF-8') as f:
        with open("keywords.txt","a",encoding="UTF-8") as f2:
            abstract=""
            line=f.readline()
            while line:
                if line == "\n":
                    keywords=get_en_keywords(abstract)
                    abstract=""
                    for phrase in keywords[:5]:
                        f2.write(phrase.text+"\n")
                        print(phrase.text)
                    f2.write("\n")
                    line=f.readline()
                    f2.write("[title]")
                    print("[title]")
                    f2.write(line)
                    print(line)
                line=f.readline()
                abstract = abstract+line

