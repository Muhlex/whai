#!/usr/bin/env python 

import pdfkit

def create_pdf(url):
    #Define path to wkhtmltopdf.exe
    path_to_wkhtmltopdf = r'/usr/bin/wkhtmltopdf'

    #Define path to HTML file
    path_to_file = 'templates/sample.html'

    #Point pdfkit configuration to wkhtmltopdf.exe
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    #Convert HTML file to PDF
    pdfkit.from_url(url, output_path='sample.pdf', configuration=config)