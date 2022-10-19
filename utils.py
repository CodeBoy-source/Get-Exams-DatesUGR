import numpy as np
import urllib.request
import re
# pdf_path = "https://etsiit.ugr.es/sites/centros/etsiit/public/inline-files/Calendario-Examenes-21-22-GII.pdf"
def download_file(download_url, filename):
    response = urllib.request.urlopen(download_url)
    if filename.find('.pdf')==-1:
        filename += '.pdf'
    file = open(filename,'wb')
    file.write(response.read())
    file.close()

def remove_headers(good_data):
    pattern = "([a-zA-Z]+)\n([0-9]+)\n([a-zA-Z]+)"
    index = 1
    for i in range(0,good_data.shape[0]):
        # row = titles.iloc[[i]].to_numpy()[0]
        row = good_data[i,:]
        row[np.where(row==None)[0]] = ""
        # row = [val.find("\\") for val in row]
        res = [bool(re.search(pattern,val)) for val in row]
        if np.count_nonzero(res)>=1:
            index = i
            break

    return index

