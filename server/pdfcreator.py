#!/usr/bin/env python
import uuid

import pdfkit
from fastapi import HTTPException


def create_pdf(report: str):
	# Define path to wkhtmltopdf.exe
	#path_to_wkhtmltopdf = r'/usr/bin/wkhtmltopdf'

	# Point pdfkit configuration to wkhtmltopdf.exe
	config = pdfkit.configuration(encoding="utf-8")

	# Convert HTML file to PDF
	name = f"{uuid.uuid4().hex}.pdf"
	if pdfkit.from_string(report, output_path=name, configuration=config):#, configuration=config):
		return name
	print("cant generate pdf ??? ")
	raise HTTPException(status_code=400, detail="Cant generate pdf??")
