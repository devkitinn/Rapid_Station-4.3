#!/usr/bin/env python
import wx
import wx.grid
#import rapidModel
import rapidModel2
import printLib
import conf
from stationEnum import Station

from reportlab.graphics.barcode import *
from reportlab.platypus import *
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import cm
from reportlab.graphics.barcode import common, code128, code39, code93, usps, usps4s, ecc200datamatrix
from reportlab.pdfgen import canvas

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class jobFrame(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: dialogFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.BORDER_SIMPLE | wx.DEFAULT_FRAME_STYLE
        wx.Dialog.__init__(self, None, title="Job Part Management", style=wx.BORDER_SIMPLE | wx.DEFAULT_FRAME_STYLE)
        self.SetSize((1024, 768))
        self.txtJobName = wx.TextCtrl(self, wx.ID_ANY, "")
        self.cbAddR = wx.CheckBox(self, wx.ID_ANY, "Prepend R to ID's")
        self.grid_1 = wx.grid.Grid(self, wx.ID_ANY, size=(1, 1))
        self.btnAddSelected = wx.Button(self, wx.ID_ANY, "Add Selected to")
        self.cbSelectTargetStation = wx.ComboBox(self, wx.ID_ANY, choices=["Allocations", "Bay Drops", "Purchasing", "Receiving", "Create Nest", "Nesting", "Holzma", "Edging", "Hinging", "Reworks QA", "Rework Complete", "Dispatch"], style=wx.CB_DROPDOWN)
        self.btnCancel = wx.Button(self, wx.ID_ANY, "Cancel")
        self.btnPrint = wx.Button(self, wx.ID_ANY, "Print")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.saveJob, self.btnAddSelected)
        self.Bind(wx.EVT_BUTTON, self.closeJob, self.btnCancel)
        self.Bind(wx.EVT_BUTTON, self.printJob, self.btnPrint)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: jobFrame.__set_properties
        self.SetTitle("Job in Rapid")
        self.cbAddR.Hide()
        self.cbAddR.SetValue(1)
        self.txtJobName.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "Segoe UI"))
        self.grid_1.CreateGrid(10, 10)
        self.grid_1.SetColLabelValue(0, "Part ID")
        self.grid_1.SetColLabelValue(1, "Work Order")
        self.grid_1.SetColLabelValue(2, "Name")
        self.grid_1.SetColLabelValue(3, "Cab No")
        self.grid_1.SetColLabelValue(4, "Cab Name")
        self.grid_1.SetColLabelValue(5, "Material")
        self.grid_1.SetColLabelValue(6, "Length")
        self.grid_1.SetColLabelValue(7, "Width")
        self.grid_1.SetColLabelValue(8, "Thickness")
        self.grid_1.SetColLabelValue(9, "Edge")
        self.cbSelectTargetStation.SetSelection(0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: jobFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.txtJobName, 0, 0, 0)
        sizer_1.Add(self.cbAddR, 0, 0, 0)
        sizer_1.Add(self.grid_1, 100, wx.EXPAND, 0)
        sizer_2.Add((20, 20), 0, 0, 0)
        sizer_3.Add(self.btnAddSelected, 0, 0, 0)
        sizer_3.Add((20, 20), 0, 0, 0)
        sizer_3.Add(self.cbSelectTargetStation, 0, 0, 0)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)
        sizer_2.Add((20, 20), 0, 0, 0)
        static_line_1 = wx.StaticLine(self, wx.ID_ANY, style=wx.LI_VERTICAL)
        sizer_2.Add(static_line_1, 0, wx.EXPAND, 0)
        sizer_2.Add((20, 20), 0, 0, 0)
        sizer_4.Add(self.btnCancel, 0, 0, 0)
        sizer_4.Add((20, 20), 0, 0, 0)
        sizer_4.Add(self.btnPrint, 0, 0, 0)
        sizer_2.Add(sizer_4, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_2.Add((20, 20), 0, 0, 0)
        sizer_1.Add(sizer_2, 1, 0, 0)
        self.SetSizer(sizer_1)
        self.grid_1.AutoSize()
        self.Layout()
        # end wxGlade


    def saveJob(self, event):  # wxGlade: singlePart.<event_handler>
        # Get parts selected and update them in the database with selected station id.
        lst = self.grid_1.GetSelectedRows()
        for i in range(0, len(lst)):
            partID = self.grid_1.GetCellValue(lst[i],0)
            jobName = self.txtJobName.GetValue()
            wOrder = self.grid_1.GetCellValue(lst[i],1)
            pName = self.grid_1.GetCellValue(lst[i], 2)
            cabNum = self.grid_1.GetCellValue(lst[i], 3)
            cabName = self.grid_1.GetCellValue(lst[i], 4)
            material = self.grid_1.GetCellValue(lst[i], 5)
            length = self.grid_1.GetCellValue(lst[i], 6)
            width = self.grid_1.GetCellValue(lst[i], 7)
            thick = self.grid_1.GetCellValue(lst[i], 8)
            banding = self.grid_1.GetCellValue(lst[i], 9)
            station = self.cbSelectTargetStation.GetSelection() + 1
            if self.cbAddR.GetValue() == True:
                rapidModel2.addRapidMulti(partID, jobName, wOrder, pName, cabNum, cabName, material, length, width, thick, banding, station)
            else:
                rapidModel2.makeRapidMulti(partID, jobName, wOrder, pName, cabNum, cabName, material, length, width, thick, banding, station)

        self.EndModal(0)
        event.Skip()

    def printJob(self, event):  # wxGlade: singlePart.<event_handler>
        jobName = self.txtJobName.GetValue()
        try:
            jobDate = rapidModel2.getJobInstallDate(jobName)[0][1]
        except:
            jobDate = ""
        if jobName == '':
            wx.MessageBox('Please enter a job.')
        else:
            printLib.resetPrinting(f"Job RAPID Parts for {jobName}")
            im = printLib.Image("ki_logo.ico",width=30,height=30)
            im.hAlign = 'LEFT'
            para = printLib.Paragraph(f"{jobName} RAPID Parts       (Install Due: {jobDate})", printLib.HeaderStyle)
            #tblData = [[im, para],]
            tblData = [[para],]
            #t = printLib.Table(tblData, colWidths=(40, None))
            t = printLib.Table(tblData, colWidths=(None))
            printLib.Elements.append(t)
            tblParts = rapidModel2.getJobRapidParts(jobName)
            for i in range(0, len(tblParts)):
                tblParts[i] = list(tblParts[i])
                #if tblParts[i][9] == None:
                #    tblParts[i][9] = '0'
                if tblParts[i][9] == None:
                    tblParts[i][9] = 0
                if tblParts[i][9] < 0:
                    tblParts[i][9] = 'Unknown'
                else:
                    tblParts[i][9] = self.getLocation(int(tblParts[i][9]))

                #del tblParts[i][10]     # Now remove the scanned status column
                for j in range(1, len(tblParts[i])):
                    tblParts[i][j] = printLib.Paragraph(str(tblParts[i][j]), printLib.tableStyle)
                tblParts[i][0] = printLib.code128.Code128(tblParts[i][0])
            tblParts.insert(0, ["Barcode", "ID", "Part Name", "Cab\nNo", "Cab Name", "Material", "L", "W", "Edging", "Location"])
            printLib.printTable(tblParts, (None, 3 * cm, None, None, 3 * cm, None, 2 * cm, 2 * cm, 2 * cm, 3 * cm))
            printLib.goPrintLandscape()
        event.Skip()

    def closeJob(self, event):  # wxGlade: singlePart.<event_handler>
        self.EndModal(0)
        event.Skip()

    def getLocation(self, locationID):
        if locationID == 0:
            locationText = "Not Cut"
        elif locationID == Station.ALLOCATIONS:
            locationText = "Allocations"
        elif locationID == Station.BAY_DROPS:
            locationText = "Bay Drops"
        elif locationID == Station.PURCHASING:
            locationText = "Purchasing"
        elif locationID == Station.RECEIVING:
            locationText = "Waiting <br/>Receipt"
        elif locationID == Station.CREATE_NEST:
            locationText = "Create Nest"
        elif locationID == Station.NESTING:
            locationText = "Nesting"
        elif locationID == Station.HOLZMA:
            locationText = "Holzma"
        elif locationID == Station.EDGING:
            locationText = "Edging"
        elif locationID == Station.HINGING:
            locationText = "Hinging"
        elif locationID == Station.REWORKS_QA:
            locationText = "Reworks <br/>QA"
        elif locationID == Station.REWORK_COMPLETE:
            locationText = "Rework <br/>Complete"
        elif locationID == Station.DISPATCH:
            locationText = "Dispatch"
        elif locationID == Station.RAPID_COMPLETE:
            locationText = "Rapid <br/>Complete"
        elif locationID == Station.TROLLEY_SPECIALS:
            locationText = "Specials <br/>Trolley"
        elif locationID == Station.TROLLEY_CUTDOWN:
            locationText = "Cutdown <br/>Trolley"
        elif locationID == Station.TROLLEY_JOB:
            locationText = "Job <br/>Trolley"
        else:
            locationText = "Unknown"
        return locationText

# end of class jobFrame
