
# !/usr/bin/env python
# -*- coding: UTF-8 -*-
import wx
import conf
import rapidModel2
import printLib
from reportlab.lib.units import cm

class RapidEnterFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        kwargs["style"] = kwargs.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        super().__init__(*args, **kwargs)
        conf.get_conf()
        divs = ", ".join(conf.get_allowed_divisions())
        self.SetTitle(f"R.A.P.I.D. — Enter & Print (Divisions: {divs})")
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Controls (simplified UI to align with division-aware data)
        self.txtJob = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.btnPrintJobRapids = wx.Button(panel, label="Print Job RAPIDs")
        self.comboWorkstations = wx.ComboBox(panel, choices=[
            "Allocations", "Push In", "Purchasing", "Receiving",
            "Create Nest", "Nesting", "Holzma", "Edging",
            "Waiting for Edge Tape", "Reworks QA", "Rework Complete",
            "Dispatch"
        ])
        self.btnPrintWorkstation = wx.Button(panel, label="Print Workstation List")
        self.gridPreview = wx.grid.Grid(panel)
        self.gridPreview.CreateGrid(0, 10)

        sizer.Add(wx.StaticText(panel, label="Job"))
        sizer.Add(self.txtJob, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.btnPrintJobRapids, 0, wx.ALL, 5)
        sizer.Add(wx.StaticText(panel, label="Workstation"))
        sizer.Add(self.comboWorkstations, 0, wx.EXPAND|wx.ALL, 5)
        sizer.Add(self.btnPrintWorkstation, 0, wx.ALL, 5)
        sizer.Add(self.gridPreview, 1, wx.EXPAND|wx.ALL, 5)
        panel.SetSizer(sizer)
        self.SetSize((800, 600))

        # Events
        self.Bind(wx.EVT_BUTTON, self.onPrintJobRapids, self.btnPrintJobRapids)
        self.Bind(wx.EVT_BUTTON, self.onPrintWorkstation, self.btnPrintWorkstation)
        self.Bind(wx.EVT_TEXT_ENTER, self.onPrintJobRapids, self.txtJob)

    def onPrintJobRapids(self, event):
        jobName = self.txtJob.GetValue()
        if not jobName:
            wx.MessageBox("Please enter a job name")
            return
        # Division-aware via rapidModel2
        tblParts = rapidModel2.getJobRapids(jobName)
        printLib.resetPrinting(f"RAPID Parts for Job {jobName}")
        para = printLib.Paragraph(f"RAPID Parts for Job {jobName}", printLib.HeaderStyle)
        t = printLib.Table([[para]], colWidths=(None))
        printLib.Elements.append(t)
        # Build table for PDF
        for i in range(len(tblParts)):
            row = list(tblParts[i])
            for j in range(len(row)):
                row[j] = printLib.Paragraph(str(row[j]), printLib.tableStyle)
            tblParts[i] = row
        tblParts.insert(0, ["ID", "WO", "Part Name", "Cab No", "Cab Name", "Material", "L", "W", "Thickness", "Edge"]) 
        printLib.printTable(tblParts, (None, 3*cm, 3*cm, None, 3*cm, 3*cm, 2*cm, 2*cm, 2*cm, 2*cm))
        printLib.goPrintLandscape()

    def onPrintWorkstation(self, event):
        idx = self.comboWorkstations.GetSelection()
        if idx == wx.NOT_FOUND:
            wx.MessageBox("Please choose a workstation")
            return
        mapping = [1,2,3,4,5,6,7,8,9,10,11,12]
        lid = mapping[idx]
        rapidLocation = self.getLocation(lid)
        tblParts = rapidModel2.getLocationRapidParts(lid)  # division-aware
        printLib.resetPrinting(f"RAPID Parts for {rapidLocation}")
        para = printLib.Paragraph(f"RAPID Parts for {rapidLocation}", printLib.HeaderStyle)
        t = printLib.Table([[para]], colWidths=(None))
        printLib.Elements.append(t)
        for i in range(len(tblParts)):
            tblParts[i] = list(tblParts[i])
            for j in range(1, len(tblParts[i])):
                tblParts[i][j] = printLib.Paragraph(str(tblParts[i][j]), printLib.tableStyle)
            try:
                tblParts[i][0] = printLib.code128.Code128(tblParts[i][0])
            except Exception:
                pass
        tblParts.insert(0, ["Barcode", "Job", "ID", "Part Name", "Cab No", "Cab Name", "Material", "L", "W", "Edging"])
        printLib.printTable(tblParts, (None, 3 * cm, 3 * cm, 3 * cm, None, 3 * cm, 3 * cm, 2 * cm, 2 * cm, 2 * cm))
        printLib.goPrintLandscape()

    def getLocation(self, locationID):
        return {
            1: "Allocations", 2: "Push In", 3: "Purchasing", 4: "Receiving",
            5: "Create Nest", 6: "Nesting", 7: "Holzma", 8: "Edging",
            9: "Waiting for Edge Tape", 10: "Reworks QA", 11: "Rework Complete",
            12: "Dispatch"
        }.get(locationID, "Check Job")

class MyApp(wx.App):
    def OnInit(self):
        conf.get_conf()
        divs = ", ".join(conf.get_allowed_divisions())
        frame = RapidEnterFrame(None, title=f"R.A.P.I.D. — Enter & Print (Divisions: {divs})")
        self.SetTopWindow(frame)
        frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
