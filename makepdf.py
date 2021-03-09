import pandas as pd
from readpdf import create_api, redacted

import os
import glob
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_pdf import PdfPages
# import numpy as np

from fpdf import FPDF 


d = redacted()

def genTxt():
    fout = "txt/" + d['Invoice No'] + ".txt"
    fo = open(fout, "w")

    for k, v in d.items():
        fo.write(str(k) + ' >>> '+ str(v) + '\n\n')

    fo.close()

    files = glob.glob('bills/*.pdf', recursive=True)
    for f in files:
        os.remove(f)

def txt2pdf():
    pdf = FPDF()    
    
    # Add a page 
    pdf.add_page() 
    
    # set style and size of font  
    # that you want in the pdf 

    pdf.set_font("Arial", size = 15) 
    
    # open the text file in read mode 
    f = open("txt/" + d['Invoice No'] + ".txt", "r") 
    
    # insert the texts in pdf 
    for x in f: 
        pdf.cell(200, 10, txt = x, ln = 1, align = 'C') 
    
    # save the pdf with name .pdf 
    pdf.output("final/" + d['Invoice No'] + ".pdf") 

    files = glob.glob('txt/*.txt')
    for f in files:
        os.remove(f)

