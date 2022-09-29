# import camelot
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import re
import sys
from PyPDF2 import PdfFileReader, PdfWriter, PdfReader
import urllib.request
from tabulate import tabulate
import pdfplumber
import re
import bs4 as bs

domain = "https://etsiit.ugr.es"
html = domain + '/docencia/grados/calendario-examenes'
source = urllib.request.urlopen(html).read()
soup = bs.BeautifulSoup(source)
# print(soup.find_all('a'))
headers = soup.body.findAll('a',text=re.compile('.Informática.'))
to_add = headers[0].get('href')

pdf_path = domain + to_add
# pdf_path = "https://etsiit.ugr.es/sites/centros/etsiit/public/inline-files/Calendario-Examenes-21-22-GII.pdf"
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    file = open(filename + ".pdf", 'wb')
    file.write(response.read())
    file.close()

download_file(pdf_path, "./datos/calendar")

filename = './datos/calendar.pdf'

PDF=PdfReader(open(filename,'rb'))
for i,page in enumerate(PDF.pages):
    writer = PdfWriter()
    with open("./datos/page{}.pdf".format(i),"wb") as fp:
        writer.addPage(page)
        writer.write(fp)


test = "Jue\n13\nEne"
pattern = "([a-zA-Z]+)\n([0-9]+)\n([a-zA-Z]+)"
# print(test)
# print(re.match(pattern,test))

dir_tree = os.listdir('./datos')
dir_tree.sort()
ot = 0
for file in dir_tree:
    if 'page' in file:
        # bad_data = camelot.read_pdf('./datos/'+file)
        pdf = pdfplumber.open("./datos/"+file)
        page = pdf.pages[0]
        good_data = np.array(page.extract_table())
        # titles = bad_data[0].df
        index = 1
        for i in range(0,titles.shape[0]):
            # row = titles.iloc[[i]].to_numpy()[0]
            row = good_data[i,:]
            row[np.where(row==None)[0]] = ""
            # row = [val.find("\\") for val in row]
            res = [bool(re.search(pattern,val)) for val in row]
            if np.count_nonzero(res)>=1:
                print(row)
                print(res)
                index = i
                break

        print(index)
        # print(titles.iloc[[1]].to_numpy()[0])
        # print(len(good_data[3,3:]),good_data[3,3:])
        # print(len(titles.iloc[[1]].to_numpy()[0,3:]),titles.iloc[[1]].to_numpy()[0,3:])
        # df = pd.DataFrame(good_data[3:,3:],columns=titles.iloc[[index]].to_numpy()[0,3:])
        df = pd.DataFrame(good_data[3:,3:],columns=good_data[index,3:])
        # print(df)
        # df.drop(labels=[0,2],axis=0,inplace=True)
        print(file)
        print(tabulate(df,headers='keys',tablefmt='psql'))
        outname = './datos/tab{}.csv'.format(ot)
        ot += 1
        print(outname)
        df.to_csv(outname ,encoding='utf-8')
