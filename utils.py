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



# https://www.programcreek.com/python/?CodeExample=remove+accents
def remove_accents(raw_text):
    """Removes common accent characters.

    Our goal is to brute force login mechanisms, and I work primary with
    companies deploying Engligh-language systems. From my experience, user
    accounts tend to be created without special accented characters. This
    function tries to swap those out for standard Engligh alphabet.
    """

    raw_text = re.sub(u"[àáâãäå]", 'a', raw_text)
    raw_text = re.sub(u"[èéêë]", 'e', raw_text)
    raw_text = re.sub(u"[ìíîï]", 'i', raw_text)
    raw_text = re.sub(u"[òóôõö]", 'o', raw_text)
    raw_text = re.sub(u"[ùúûü]", 'u', raw_text)
    raw_text = re.sub(u"[ýÿ]", 'y', raw_text)
    raw_text = re.sub(u"[ß]", 'ss', raw_text)
    raw_text = re.sub(u"[ñ]", 'n', raw_text)
    return raw_text


