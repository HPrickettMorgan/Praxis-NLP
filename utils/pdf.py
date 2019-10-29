from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

from mine_pdf import convert_pdf_to_txt

import glob
import os


def convert_pdf_to_txt(path):
    # from https://stackoverflow.com/a/26495057

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos,
            maxpages=maxpages,
            password=password,
            caching=caching,
            check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


def get_folder_pdf_text(folder, n=-1):
    """Obtains the text of PDFs in an entire folder.

    :folder: The folder to get the text from.
    :n: The number of PDFs to return (default: -1, all of them).

    :returns: The text of the folder as a dict, where the keys are the file
    names (stripped of path / extension) and the values are the file text.
    """
    text = {}
    for i, fname in enumerate(glob.iglob(os.path.join(folder, '*.pdf'))):
        print(fname)
        text[os.path.basename(fname).split('.')[0]] = \
            convert_pdf_to_txt(os.path.join(folder, fname))
        if i >= n-1 and n is not -1:
            break
    return text
