# import camelot
import numpy as np
import unidecode
import matplotlib.pyplot as plt
import pandas as pd
import re
import os
import sys
from PyPDF2 import PdfFileReader, PdfWriter, PdfReader
import urllib.request
from tabulate import tabulate
import pdfplumber
import re
import bs4 as bs
from utils import download_file, remove_headers

days = {'Lun': "Lunes", 'Mar': "Martes", 'Mie': "Miercoles", 'Jue': "Jueves" , 'Vie': "Viernes",'Sab':"Sabado", 'Dom': "Domingo"}
months = {'Ene': "Enero",'Feb':"Febrero",'Mar':"Marzo", 'May':"Mayo",'Abr':"Abril",'Jul':"Julio",'Jun':"Junio",'Ago':"Agosto"}
cursos = ['Ingeniería Informática','Ingeniería de Tecnologías de Telecomunicación',
        'Informática y Matemáticas', 'Ingeniería Informática y Administración y Dirección de Empresas']
siglas = ['GII','GIIT','GIIM','GIIADE']


domain = "https://etsiit.ugr.es"
html = domain + '/docencia/grados/calendario-examenes'
source = urllib.request.urlopen(html).read()
soup = bs.BeautifulSoup(source,'html.parser')
a_files = soup.find_all('div',{'class':'field__item'})
ul_files = a_files[3].find_all_next('ul')
li_files = ul_files[0].find_all('a',{'class':'file'})
to_add = [ ref.get('href') for ref in li_files]

dir_tree = os.listdir('./datos')
if len(dir_tree) == 0:
    nombres = []
    for i,a in enumerate(to_add):
        pdf_path = domain + a
        nombre = a[a.rfind('/')+1:]
        nombres.append(nombre)
        download_file(pdf_path, "./datos/{}".format(nombre))

for file in dir_tree:
    if '.pdf' in file:
        filename = "./datos/{}".format(file)
        print(file,filename)
        pdf = pdfplumber.open(filename)
        filtered_table = None
        first_index = None
        for i in range(0,len(pdf.pages)-2):
            page = pdf.pages[i]
            good_data = np.array(page.extract_table())
            index  = remove_headers(good_data)
            if not first_index:
                first_index = index

            for i in range(3,good_data.shape[0]):
                fila = good_data[i]
                fila = np.array([fil=='M' or fil=='T' for fil in fila])
                fila[:6] = False
                fecha = good_data[index,fila]
                fecha = fecha[0].split("\n")
                fecha = "{}, {} de {}".format(days[fecha[0]],fecha[1],months[fecha[2]])
                good_data[i,6] = fecha

            if filtered_table is not None :
                good_data = good_data[index+2:,:7]
                filtered_table = np.vstack((filtered_table,good_data))
            else:
                good_data = good_data[index+1:,:7]
                good_data[index-1,-1] = "Fecha"
                filtered_table = good_data

        df = pd.DataFrame(filtered_table[first_index:,:],columns=filtered_table[first_index-1,:])
        outname = "./datos/{}.csv".format(file[:file.rfind('.')])
        df.to_csv(outname,encoding='utf-8')
        print(tabulate(df,headers='keys',tablefmt='psql'))
