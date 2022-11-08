from pprint import pprint
from queue import Empty
import nltk
nltk.download("stopwords")
nltk.download("punkt")
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from bs4 import BeautifulSoup
from difflib import SequenceMatcher

import requests
import time
import docx
import logging
import pprint

logger = logging.getLogger("mylogger")

result_dic = { 'href':[], 'score':[], 'exclude_urls':[]}

stopwords = stopwords.words('english')

exclude_urls = []


# Compare input text and result text and assign a score
# Cosine Similarity

def checkSimilarity(s1, s2):

    return SequenceMatcher(None, s1, s2).ratio()


# def checkSimilarity(s1, s2):

#     l1 = word_tokenize(s1)
#     l2 = word_tokenize(s2)

#     v1 = []; v2 = []

#     set1 = {w for w in l1 if not w in stopwords}
#     set2 = {w for w in l2 if not w in stopwords}

#     rvect = set1.union(set2)

#     for w in rvect:
#         if w in set1:
#             v1.append(1)
#         else:
#             v1.append(0)
        
#         if w in set2:
#             v2.append(1)
#         else:
#             v2.append(0)
    
#     score = 0

#     for i in range(len(rvect)):
#         score += v1[i]*v2[i]
#     div = float((sum(v1)*sum(v2))**0.5)

#     if div > 0:
#         score /= div
#     else:
#         score = 0
#     return score


def findScore(sentence_list, sentence_list_web):

    len1 = len(sentence_list)

    len2 = 0
    for i in sentence_list_web:
        len2 += len(i)
        
    f = 0
    for i in range(len1):
        if sentence_list_web[i] == []:
            f += 1
        else:
            for j in range(len(sentence_list_web[i])):
                f += checkSimilarity(sentence_list[i], sentence_list_web[i][j])
    
    f /= len2
    
    return f


# 3- Extract or scrap text from the search results

def extractor(resdict):

    slweb = []
    for i in resdict.keys():
        itm = resdict[i]['cards']
        slweb.append(itm)

    return slweb


# 2- Search the web with each sentence

def getResults(text):

    text = text.replace(" ","+")

    url = f'https://www.bing.com/search?q={text}&qs=n&form=QBRE&sp=-1&pq={text.lower()}"'
    # url = f'https://www.google.com/search?q="{text}&oq={text}&sourceid=chrome&ie=UTF-8"'

    header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'}
    
    page = requests.get(url, headers= header, allow_redirects=True)

    content = BeautifulSoup(page.content, 'html.parser')

    return content


def checkExcludeURLS(url):
    exclude_urls = result_dic['exclude_urls']
    status = False
    for u in exclude_urls:
        if u:
            if u in url:
                status = True
        
    return status


def processResults(content):
    res = {}
    res["headlines"] = []
    res["result-stats"] = []
    res["cards"] = []
    

    for i in content.find_all('h2'):
        entry = i.find('a')
        try:
            isExcluded = checkExcludeURLS( entry['href'] )
            if not isExcluded:
                try:
                    result_dic['href'].append(entry['href'])
                except:
                    pass
        except:
            pass
        lnk = None
        if len(str(entry)) >= 28:
            lnk = str(entry)[28:str(entry).index('" target')]
        res["headlines"].append((i.get_text(), lnk))

    for i in content.find_all('p'):
        res["cards"].append(i.get_text().replace("/strong&gt;","").replace("&lt;","").replace("strong&gt;",""))
    
    res["result-stats"]=[i.get_text() for i in content.find_all('span', attrs = {"class": "sb_count"})][0]

    return res


def webSearch(sentence_list):

    search_results = {}

    for i in range(len(sentence_list)):
        cnt = getResults(sentence_list[i])
        search_results[sentence_list[i]] = processResults(cnt)
        time.sleep(2)

    return search_results


# 1- Convert large text into smaller sentences

def generateSentences(text):

    text = '''{}'''.format(text)
    sentences = []
    sen0 = sent_tokenize(text)
    for i in sen0:
        sentences.append(i)
    
    return sentences


# Plagiarism driver

def driver(text):

    sentences = generateSentences(text)
    searches = webSearch(sentences)
    results = extractor(searches)
    score = findScore(sentences, results)
    
    result_dic['score'].append(score*100)


# Starter for different file types

def readPdf(file):
   
    class PdfConverter:

        def __init__(self, file_path,*args, **kwargs):
            self.file_path = file_path

        def convert_pdf_to_txt(self):
            rsrcmgr = PDFResourceManager()
            retstr = StringIO()
            codec = 'utf-8'
            laparams = LAParams()
            device = TextConverter(rsrcmgr, retstr, laparams=laparams)
            fp = open(self.file_path, 'rb')
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            password = ""
            maxpages = 0
            caching = True
            pagenos = set()
            for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
                interpreter.process_page(page)
            fp.close()
            device.close()
            str = retstr.getvalue()
            retstr.close()
            return str

        def save_convert_pdf_to_txt(self):
            content = self.convert_pdf_to_txt()
            txt_pdf = open('temp_pdf.txt', 'wb')
            txt_pdf.write(content.encode('utf-8'))
            txt_pdf.close()

    if __name__ == '__main__':

        pdfConverter = PdfConverter(file_path=file)
        pdfConverter.save_convert_pdf_to_txt()
        readTxt("temp_pdf.txt")


def readTxt(file):
    
    completedText=''
    with open(file,encoding='utf-8') as f:
        ls=f.readlines()
    for el in ls:
        completedText+=el
    driver(completedText)


def readDoc(file):

    doc = docx.Document(file)

    completedText=''
    for paragraph in doc.paragraphs[:2]:
        completedText+=(paragraph.text)

    driver(completedText) 


# Initiate the process

def init_plagiarism(file, urls):


    result_dic['exclude_urls'] = urls.split(',')

    if file.endswith('.pdf'):
        readPdf(file)
    elif file.endswith('.txt'):
        readTxt(file)
    elif file.endswith('.docx'):
        readDoc(file)    
    else:
        print("Assignment should be in PDF, TXT or DOCX file only.")     
    # pprint.pprint(result_dic)
    return result_dic
