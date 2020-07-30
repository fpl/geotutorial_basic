#!/usr/bin/python3

# Create a pdf with a map image

import fpdf

# PDF constructor:
# Portrait, millimeter units, A4 page size
pdf=fpdf.FPDF("P", "mm", "A4")
# create a new page
pdf.add_page()
# Set font: arial, bold, size 20
pdf.set_font('Arial','B',20)
# Create a new cell: 160 x 25mm, text contents, no border, centered
pdf.cell(160,25,'Hancock County Boundary', border=0, align="C")
pdf.image("hancock.png",25,50,150,160)
pdf.output('map.pdf','F')
