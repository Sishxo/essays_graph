import re
import os

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFTextExtractionNotAllowed, PDFPage
from pdfminer.pdfparser import PDFParser


def is_contains_chinese(strs):
    for _char in strs:
        if '\u4e00' <= _char <= '\u9fa5':
            return True
    return False

def parsePDF(PDF_path, TXT_path):
    with open(PDF_path, 'rb') as fp:
        parser = PDFParser(fp)
        document = PDFDocument(parser)

        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        rs_manager = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rs_manager, laparams=laparams)
        interpreter = PDFPageInterpreter(rs_manager, device)

        flag = 0

        for i, page in enumerate(PDFPage.create_pages(document)):
            interpreter.process_page(page)
            layout = device.get_result()

            for element in layout:
                if isinstance(element, LTTextBoxHorizontal):
                    with open(TXT_path, 'a', encoding='UTF-8') as f:
                        result = element.get_text()
                        # print(result)
                        # print(i,element.index)
                        if i == 0 and element.index == 0:
                            f.write(result)
                        elif flag == 1:
                            f.write(result + '\n')
                            return 1
                        elif re.search('Abstract', result):
                            flag = 1


def getCVFPapers(PDF_path):
    with(open(PDF_path, 'rb')) as fp:
        parser = PDFParser(fp)
        document = PDFDocument(parser)

        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        rs_manager = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rs_manager, laparams=laparams)
        interpreter = PDFPageInterpreter(rs_manager, device)

        for i, page in enumerate(PDFPage.create_pages(document)):
            interpreter.process_page(page)
            layout = device.get_result()

            for element in layout:
                if isinstance(element, LTTextBoxHorizontal):
                    result = element.get_text()
                    if i == 0 and element.index == 0 and (re.search('NOTE TO USERS', result, re.IGNORECASE) or re.search('INFORMATION TO USERS', result, re.IGNORECASE) or is_contains_chinese(result) or re.search('Gradual', result, re.IGNORECASE)):
                        return 1
                    elif i == 0 and element.index == 1 and re.search('by', result, re.IGNORECASE):
                        return 2
                    elif i == 0 and re.search('Amanda Fiore', result, re.IGNORECASE):
                        return 3
                    elif i == 1 and element.index == 0 and re.search('UMI Number', result, re.IGNORECASE):
                        return 4
                    elif i == 1 and element.index ==1:
                        return 0


if __name__ == '__main__':
    g = os.walk("../data/essays")
    for path, dir_list, file_list in g:
        finish_num = 0
        file_num = len(file_list)
        for file_name in file_list:
            parsePDF(os.path.join(path, file_name), "../data/txt/abstract_test.txt")
            finish_num += 1
            print(file_name + " extract done.  " + str(finish_num) + " / " + str(file_num))
