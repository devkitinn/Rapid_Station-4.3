import wx
import sys
import tempfile
#import win32api
import wx.lib.sized_controls as sc
from wx.lib.pdfviewer import pdfViewer, pdfButtonPanel
#from PyPDF4 import PdfFileReader

from reportlab.graphics.barcode import *
from reportlab.platypus import *
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import cm
from reportlab.graphics.barcode import common, code128, code39, code93, usps, usps4s, ecc200datamatrix
from reportlab.pdfgen import canvas

Title = ""
Elements = []
PAGE_HEIGHT=defaultPageSize[1]
styles = getSampleStyleSheet()
tableStyle = styles["BodyText"]
tableStyle.wordWrap = 'CJK'
HeaderStyle = styles["Heading1"] # XXXX
ParaStyle = styles["Normal"]
PreStyle = styles["Code"]

def myPage1(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold',24)
    canvas.drawString(108, PAGE_HEIGHT-108, Title)
    canvas.setFont('Times-Roman',9)
    canvas.restoreState()

def myLaterPages(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Roman',9)
    canvas.drawString(cm * 2.54 , 0.75 * cm * 2.54, "Page %d %s" % (doc.page, pageinfo))
    canvas.restoreState()

def header(txt, style=HeaderStyle, klass=Paragraph, sep=0.3):
    s = Spacer(0.2* cm * 2.54, sep * cm * 2.54)
    Elements.append(s)
    para = klass(txt, style)
    Elements.append(para)

def p(txt):
    return header(txt, style=ParaStyle, sep=0.1)

def pre(txt):
    s = Spacer(0.1 * cm * 2.54, 0.1 * cm * 2.54)
    Elements.append(s)
    p = Preformatted(txt, PreStyle)
    Elements.append(p)

#def printTable(tableToPrint, colWidthsList = (None, 3 * cm, 3 * cm, None, cm, 3 * cm, None, 2 * cm, 2 * cm, 2 * cm)):
def printTable(tableToPrint, colWidthsList=(None, 3 * cm, 3 * cm, 3 * cm, None, 3 * cm, 3 * cm, 2 * cm, 2 * cm, 2 * cm)):
    s = Spacer(0.1 * cm * 2.54, 0.2 * cm * 2.54)
    Elements.append(s)
    tblStyle = TableStyle([('ALIGN', (0,0), (0, -1), 'LEFT'),
                           ('ALIGN', (4,1), (4, -1), 'RIGHT'),
                           ('ALIGN', (7,1), (8, -1), 'RIGHT'),
                           ('INNERGRID', (0,0), (-1, -1), 0.25, colors.black),
                           ('BOX', (0,0), (-1, -1), 0.25, colors.black),
                           ])


    t = Table(tableToPrint, colWidths= colWidthsList)
    t.setStyle(tblStyle)
    Elements.append(t)

def insertPageBreak():
    Elements.append(PageBreak())

def goPrintLandscape():
    pdfFileName = tempfile.mktemp(".pdf")
    doc = SimpleDocTemplate(pdfFileName, pagesize=landscape(A4), rightMargin=30, leftMargin = 30, topMargin = 42, bottomMargin=18)
    doc.pagesize = landscape(A4)
    doc.build(Elements)
    print(pdfFileName)
    pdfV = PDFViewer(None, size=(800, 600))
    pdfV.viewer.LoadFile(pdfFileName)
    pdfV.Show()

def resetPrinting(pageTitle):
    global Elements
    Elements = []
    global Title
    Title = pageTitle


def printLabel(tblPart):
    # offset
    # 0 = Part ID
    # 1 = Job
    # 3 = Part name
    # 5 = Cab name
    # 7 = Length
    # 8 = Width
    # 9 = Thickness
    #10 = Edge
    pdfFileName = tempfile.mktemp(".pdf")
    c = canvas.Canvas(pdfFileName, pagesize=(8*cm, 8*cm), bottomup=0)
    c.setFont("Helvetica", 12)
#    c.setStrokeColorRGB(0,0,0) # black
    lwt = f"{tblPart[0][7]} x {tblPart[0][8]} x {tblPart[0][9]}"
    c.drawString(0.5*cm, 0.5 * cm, lwt)                             # L x W x T
    c.drawString(0.5*cm, 1.0 * cm, tblPart[0][6])                   # Material
    c.setFont("Helvetica-Bold", 18)
    c.drawString(0.5*cm, 1.7 * cm, tblPart[0][1])                   # Job
    c.setFont("Helvetica", 12)
    c.drawString(0.5*cm, 2.2 * cm, tblPart[0][5])                   # Cab Name
    c.drawString(4.5*cm, 2.2 * cm, f"CAB#:{tblPart[0][4]}")         # Cab No
    c.drawString(0.5*cm, 2.7 * cm, tblPart[0][3])                   # Part Name
    barcode = code128.Code128(tblPart[0][0], barHeight=0.8*cm, barWidth=1)                        # Part ID
    barcode.drawOn(c, 0.1*cm, 2.8*cm)
    c.drawString(0.5*cm, 4.0 * cm, tblPart[0][10])                  # Edge
    c.rect(2*cm, 4.5*cm, 1.5*cm, 1.5*cm)
    if tblPart[0][18] is not None:
        c.drawString(0.5*cm, 6.5 * cm, tblPart[0][18])                   # Part comment
    c.drawString(0.5*cm, 7.5 * cm, tblPart[0][0])                   # Part ID
    #c.rotate(90)
    #barcode.drawOn(c, 2*cm, -7*cm)
    c.showPage()
    c.save()
    pdfV = PDFViewer(None, size=(800, 600))
    pdfV.viewer.LoadFile(pdfFileName)
    pdfV.viewer.CalculateDimensions()
    pdfV.Show()

class PDFViewer(sc.SizedFrame):
    def __init__(self, parent, **kwds):
        super(PDFViewer, self).__init__(parent, **kwds)

        paneCont = self.GetContentsPane()
        self.buttonpanel = pdfButtonPanel(paneCont, wx.NewId(),
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        self.buttonpanel.SetSizerProps(expand=True)
        self.viewer = pdfViewer(paneCont, wx.NewId(), wx.DefaultPosition,
                                wx.DefaultSize,
                                wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER)

        self.viewer.SetSizerProps(expand=True, proportion=1)

        # introduce buttonpanel and viewer to each other
        self.buttonpanel.viewer = self.viewer
        self.viewer.buttonpanel = self.buttonpanel


