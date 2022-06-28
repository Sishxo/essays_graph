from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFTextExtractionNotAllowed, PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.converter import PDFPageAggregator
import re
import os


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
                        #print(result)
                        #print(i,element.index)
                        if i == 0 and element.index == 0:
                            f.write(result)
                        if flag == 1:
                            f.write(result+'\n')
                            flag = 0
                            break
                        if re.search('Abstract', result):
                            flag = 1


if __name__ == '__main__':
    g=os.walk("essays")
    for path,dir_list,file_list in g:
        for file_name in file_list:
            parsePDF(os.path.join(path,file_name),"abstract.txt")
            print(file_name+" extract done.")
    '''parsePDF("./essays/A Pixel-Level Meta-Learner for Weakly Supervised Few-Shot Semantic Segmentation.pdf",
             "test.txt")'''
