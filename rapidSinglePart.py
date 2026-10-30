import wx
import wx.grid
#import rapidModel
import rapidModel2
import printLib
import conf

class singlePart(wx.Dialog):
    def __init__(self):
        # begin wxGlade: singlePart.__init__
        wx.Dialog.__init__(self, None, title="Single Part Management")
        self.SetSize((512, 435))
        self.txt_PartID = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
        self.txt_PartJob = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txt_PartWO = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txt_PartName = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txt_PartCabNo = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txt_PartCabName = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txt_PartMaterial = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txt_PartLength = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txt_PartWidth = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txt_PartThick = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txt_Edge = wx.TextCtrl(self, wx.ID_ANY, "")
        self.cb_Station = wx.ComboBox(self, wx.ID_ANY, choices=["Check Job", "Allocations", "Bay Drops", "Purchasing", "Waiting Receipt", "Create Nest", "Nesting", "Holzma", "Edging", "Hinging", "Reworks QA", "Rework Complete", "Dispatch"], style=wx.CB_DROPDOWN)
        self.cb_Tool = wx.ComboBox(self, wx.ID_ANY, choices=["Saw", "CNC"], style=wx.CB_DROPDOWN)
        self.txt_Bay = wx.TextCtrl(self, wx.ID_ANY, "")
        self.txt_Note = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.HSCROLL | wx.TE_BESTWRAP | wx.TE_LEFT | wx.TE_MULTILINE)
        self.btn_Edit = wx.Button(self, wx.ID_ANY, "Enable Edit")
        self.btn_New = wx.Button(self, wx.ID_ANY, "New Part")
        self.btn_Print = wx.Button(self, wx.ID_ANY, "Print Label")
        self.btn_Save = wx.Button(self, wx.ID_ANY, "Save")
        self.btn_Cancel = wx.Button(self, wx.ID_ANY, "Close")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_TEXT_ENTER, self.newPartID, self.txt_PartID)
        self.Bind(wx.EVT_BUTTON, self.enableEdit, self.btn_Edit)
        self.Bind(wx.EVT_BUTTON, self.newPart, self.btn_New)
        self.Bind(wx.EVT_BUTTON, self.printLabel, self.btn_Print)
        self.Bind(wx.EVT_BUTTON, self.savePart, self.btn_Save)
        self.Bind(wx.EVT_BUTTON, self.closePart, self.btn_Cancel)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: singlePart.__set_properties
        self.SetTitle("Single Part Management")
        self.txt_PartID.Enable(False)
        self.txt_PartJob.Enable(False)
        self.txt_PartWO.Enable(False)
        self.txt_PartName.Enable(False)
        self.txt_PartCabNo.Enable(False)
        self.txt_PartCabName.Enable(False)
        self.txt_PartMaterial.Enable(False)
        self.txt_PartLength.Enable(False)
        self.txt_PartWidth.Enable(False)
        self.txt_PartThick.Enable(False)
        self.txt_Edge.Enable(False)
        self.cb_Station.Enable(False)
        self.cb_Tool.Enable(False)
        self.txt_Bay.Enable(False)
        self.txt_Note.SetMinSize((200, 300))
        self.txt_Note.Enable(False)
        self.btn_Save.Enable(False)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: singlePart.__do_layout
        sizer_17 = wx.BoxSizer(wx.VERTICAL)
        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        sizer_18 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(0, 2, 2, 2)
        sizer_17.Add((10, 10), 0, 0, 0)
        sizer_14.Add((10, 10), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        lbl_Scanned = wx.StaticText(self, wx.ID_ANY, "Part")
        lbl_Scanned.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        grid_sizer_1.Add(lbl_Scanned, 0, 0, 0)
        label_35 = wx.StaticText(self, wx.ID_ANY, "ID")
        grid_sizer_1.Add(label_35, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.txt_PartID, 1, 0, 0)
        label_36 = wx.StaticText(self, wx.ID_ANY, "Job")
        grid_sizer_1.Add(label_36, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.txt_PartJob, 1, 0, 0)
        label_37 = wx.StaticText(self, wx.ID_ANY, "WO")
        grid_sizer_1.Add(label_37, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.txt_PartWO, 1, 0, 0)
        label_38 = wx.StaticText(self, wx.ID_ANY, "Part Name")
        grid_sizer_1.Add(label_38, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.txt_PartName, 1, 0, 0)
        label_39 = wx.StaticText(self, wx.ID_ANY, "Cab No")
        grid_sizer_1.Add(label_39, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.txt_PartCabNo, 1, 0, 0)
        label_40 = wx.StaticText(self, wx.ID_ANY, "Cab Name")
        grid_sizer_1.Add(label_40, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.txt_PartCabName, 1, 0, 0)
        label_41 = wx.StaticText(self, wx.ID_ANY, "Material")
        grid_sizer_1.Add(label_41, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.txt_PartMaterial, 1, 0, 0)
        label_42 = wx.StaticText(self, wx.ID_ANY, "Length")
        grid_sizer_1.Add(label_42, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.txt_PartLength, 1, 0, 0)
        label_43 = wx.StaticText(self, wx.ID_ANY, "Width")
        grid_sizer_1.Add(label_43, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.txt_PartWidth, 1, 0, 0)
        label_44 = wx.StaticText(self, wx.ID_ANY, "Thick")
        grid_sizer_1.Add(label_44, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.txt_PartThick, 1, 0, 0)
        label_45 = wx.StaticText(self, wx.ID_ANY, "Edge")
        grid_sizer_1.Add(label_45, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.txt_Edge, 1, 0, 0)
        label_47 = wx.StaticText(self, wx.ID_ANY, "Station")
        grid_sizer_1.Add(label_47, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.cb_Station, 0, 0, 0)
        label_48 = wx.StaticText(self, wx.ID_ANY, "Tool")
        grid_sizer_1.Add(label_48, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.cb_Tool, 0, 0, 0)
        label_49 = wx.StaticText(self, wx.ID_ANY, "Bay")
        grid_sizer_1.Add(label_49, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.txt_Bay, 1, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        grid_sizer_1.Add((0, 0), 0, 0, 0)
        sizer_14.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_14.Add((10, 10), 0, 0, 0)
        lbl_Note = wx.StaticText(self, wx.ID_ANY, "Note")
        lbl_Note.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        sizer_18.Add(lbl_Note, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
        sizer_18.Add(self.txt_Note, 100, 0, 0)
        sizer_18.Add((10, 10), 0, 0, 0)
        sizer_14.Add(sizer_18, 0, 0, 0)
        sizer_14.Add((10, 10), 0, 0, 0)
        sizer_15.Add(self.btn_Edit, 1, 0, 0)
        sizer_15.Add(self.btn_New, 1, 0, 0)
        sizer_15.Add(self.btn_Print, 1, 0, 0)
        sizer_15.Add(self.btn_Save, 1, 0, 0)
        sizer_15.Add(self.btn_Cancel, 1, 0, 0)
        sizer_15.Add((10, 10), 0, 0, 0)
        sizer_14.Add(sizer_15, 1, wx.EXPAND, 0)
        sizer_14.Add((10, 10), 0, 0, 0)
        sizer_17.Add(sizer_14, 0, 0, 0)
        sizer_17.Add((5, 10), 0, 0, 0)
        self.SetSizer(sizer_17)
        self.Layout()
        # end wxGlade

    def newPartID(self, event):  # wxGlade: singlePart.<event_handler>
        # They've entered a new ID, now let's try and see if it exists.
        try:
            tblPart = rapidModel2.getPart(self.txt_PartID.Value)
            wx.MessageBox(f'Unfortunately {self.txt_partID.Value} exists. Enter a new ID or close.')
        except:
            try:

                rapidModel2.makeRapidPart(self.txt_PartID.Value)
            except:
                wx.MessageBox(f'Failed to add {self.txt_partID.Value} please close.')
        event.Skip()

    def enableEdit(self, event):  # wxGlade: singlePart.<event_handler>
        tblPart = rapidModel2.getPart(self.txt_PartID.Value)
        if conf.config.get('PART SETTINGS', 'edit') == 'True' and len(tblPart) > 0:
            # Allow editing of all but PartID
            self.txt_PartID.Enable(False)
            self.txt_PartJob.Enable(True)
            self.txt_PartWO.Enable(True)
            self.txt_PartName.Enable(True)
            self.txt_PartCabNo.Enable(True)
            self.txt_PartCabName.Enable(True)
            self.txt_PartMaterial.Enable(True)
            self.txt_PartLength.Enable(True)
            self.txt_PartWidth.Enable(True)
            self.txt_PartThick.Enable(True)
            self.txt_Edge.Enable(True)
            self.cb_Station.Enable(True)
            self.cb_Tool.Enable(True)
            self.txt_Bay.Enable(True)
            self.txt_Note.Enable(True)
            # And buttons on the dialog box
            self.btn_Edit.Enable(False)
            self.btn_Save.Enable(True)
            self.btn_New.Enable(False)
        event.Skip()

    def newPart(self, event):  # wxGlade: singlePart.<event_handler>
        if conf.config.get('PART SETTINGS', 'new') == 'True':
            # And buttons on the dialog box
            self.btn_Edit.Enable(False)
            self.btn_Save.Enable(True)
            self.btn_New.Enable(False)

            self.txt_PartID.Value = ''
            self.txt_PartID.Enable(True)
            self.txt_PartID.SetFocus()
            self.txt_PartJob.Enable(True)
            self.txt_PartWO.Enable(True)
            self.txt_PartName.Enable(True)
            self.txt_PartCabNo.Enable(True)
            self.txt_PartCabName.Enable(True)
            self.txt_PartMaterial.Enable(True)
            self.txt_PartLength.Enable(True)
            if self.txt_PartLength.Value == '':
                self.txt_PartLength.Value = '0.0'
            self.txt_PartWidth.Enable(True)
            if self.txt_PartWidth.Value == '':
                self.txt_PartWidth.Value = '0.0'
            self.txt_PartThick.Enable(True)
            if self.txt_PartThick.Value == '':
                self.txt_PartThick.Value = '0.0'
            self.txt_Edge.Enable(True)
            self.txt_Bay.Enable(True)
            self.txt_Note.Enable(True)
            self.cb_Station.Enable(True)
            self.cb_Tool.Enable(True)

        event.Skip()

    def printLabel(self, event):  # wxGlade: singlePart.<event_handler>
        if self.txt_PartID.Value != "":
            tblPart = rapidModel2.getPart(self.txt_PartID.Value)
            if len(tblPart) > 0:
                printLib.printLabel(tblPart)
        event.Skip()

    def savePart(self, event):  # wxGlade: singlePart.<event_handler>
        if conf.config.get('PART SETTINGS', 'edit') == 'True' or conf.config.get('PART SETTINGS', 'new') == 'True':
            self.txt_PartID.Enable(False)
            self.txt_PartJob.Enable(False)
            self.txt_PartWO.Enable(False)
            self.txt_PartName.Enable(False)
            self.txt_PartCabNo.Enable(False)
            self.txt_PartCabName.Enable(False)
            self.txt_PartMaterial.Enable(False)
            self.txt_PartLength.Enable(False)
            self.txt_PartWidth.Enable(False)
            self.txt_PartThick.Enable(False)
            self.txt_Edge.Enable(False)
            self.cb_Station.Enable(False)
            self.cb_Tool.Enable(False)
            self.txt_Bay.Enable(False)
            self.txt_Note.Enable(False)
            # Buttons
            self.btn_Edit.Enable(True)
            self.btn_Save.Enable(False)
            self.btn_New.Enable(True)
            if self.txt_PartID.Value != "":
                rapidModel2.updateRapidPart( self.txt_PartID.Value,
                                            self.txt_PartJob.Value,
                                            self.txt_PartWO.Value,
                                            self.txt_PartName.Value,
                                            self.txt_PartCabNo.Value,
                                            self.txt_PartCabName.Value,
                                            self.txt_PartMaterial.Value,
                                            self.txt_PartLength.Value,
                                            self.txt_PartWidth.Value,
                                            self.txt_PartThick.Value,
                                            self.txt_Edge.Value,
                                            self.cb_Station.Selection,
                                            self.cb_Tool.Selection,
                                            self.txt_Bay.Value,
                                            self.txt_Note.Value)
            self.btn_Cancel.SetFocus()
        event.Skip()

    def closePart(self, event):  # wxGlade: singlePart.<event_handler>
        self.EndModal(0)
        event.Skip()

# end of class singlePart
