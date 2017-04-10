# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
# import wx.xrc
import wx.wizard
import time
from wx import MessageDialog
import sys
import subprocess
from _ast import If

###########################################################################
## Class MyWizard1
###########################################################################

class MyWizard1 ( wx.wizard.Wizard ):
    
    def __init__( self, parent ):
        wx.wizard.Wizard.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, bitmap = wx.NullBitmap, pos = wx.DefaultPosition, style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHintsSz( wx.Size( 540,420 ), wx.DefaultSize )
        self.m_pages = []
        
        
        self.m_wizPage2 = wx.wizard.WizardPageSimple( self  )
        self.add_page( self.m_wizPage2 )
        
        bSizer3 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText4 = wx.StaticText( self.m_wizPage2, wx.ID_ANY, u"MS Bin filter", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        self.m_staticText4.SetFont( wx.Font( 14, 74, 90, 92, False, "Arial" ) )
        
        bSizer3.Add( self.m_staticText4, 0, wx.ALL, 5 )
        
        self.m_staticline1 = wx.StaticLine( self.m_wizPage2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer3.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
        
        self.m_staticText2 = wx.StaticText( self.m_wizPage2, wx.ID_ANY, u"Select file", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        bSizer3.Add( self.m_staticText2, 0, wx.ALL, 5 )
        
        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_filePicker1 = wx.FilePickerCtrl( self.m_wizPage2, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST )
        bSizer4.Add( self.m_filePicker1, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer3.Add( bSizer4, 0, wx.EXPAND|wx.ALIGN_RIGHT, 5 )
        
        self.m_checkBox2 = wx.CheckBox( self.m_wizPage2, wx.ID_ANY, u"Generate CSV Files", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_checkBox2, 0, wx.ALL, 5 )
        
        self.m_checkBox9 = wx.CheckBox( self.m_wizPage2, wx.ID_ANY, u"Custom Settings", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer3.Add( self.m_checkBox9, 0, wx.ALL, 5 )
        
        
        
        self.m_wizPage2.SetSizer( bSizer3 )
        self.m_wizPage2.Layout()
        bSizer3.Fit( self.m_wizPage2 )
        self.m_wizPage3 = wx.wizard.WizardPageSimple( self  )
        self.add_page( self.m_wizPage3 )
        
        bSizer5 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText83 = wx.StaticText( self.m_wizPage3, wx.ID_ANY, u"Output Data", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText83.Wrap( -1 )
        self.m_staticText83.SetFont( wx.Font( 14, 74, 90, 92, False, "Arial" ) )
        
        bSizer5.Add( self.m_staticText83, 0, wx.ALL, 5 )
        
        
        bSizer5.AddSpacer( ( 0, 5), 0, wx.EXPAND, 0 )
        
        self.m_staticline23 = wx.StaticLine( self.m_wizPage3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer5.Add( self.m_staticline23, 0, wx.EXPAND |wx.ALL, 5 )
        
        self.m_staticText5 = wx.StaticText( self.m_wizPage3, wx.ID_ANY, u"Use Config File:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        bSizer5.Add( self.m_staticText5, 0, wx.ALL, 5 )
        
        self.m_filePicker2 = wx.FilePickerCtrl( self.m_wizPage3, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        bSizer5.Add( self.m_filePicker2, 0, wx.ALL|wx.EXPAND, 5 )
        
        self.m_staticline26 = wx.StaticLine( self.m_wizPage3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer5.Add( self.m_staticline26, 0, wx.EXPAND |wx.ALL, 5 )
        
        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText7 = wx.StaticText( self.m_wizPage3, wx.ID_ANY, u"Set Logging level", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        bSizer6.Add( self.m_staticText7, 0, wx.ALL, 5 )
        
        self.m_slider1 = wx.Slider( self.m_wizPage3, wx.ID_ANY, 1, 1, 5, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
        bSizer6.Add( self.m_slider1, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer5.Add( bSizer6, 0, wx.EXPAND, 5 )
        
        self.m_staticline27 = wx.StaticLine( self.m_wizPage3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer5.Add( self.m_staticline27, 0, wx.EXPAND |wx.ALL, 5 )
        
        self.m_staticText84 = wx.StaticText( self.m_wizPage3, wx.ID_ANY, u"Output directory", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText84.Wrap( -1 )
        bSizer5.Add( self.m_staticText84, 0, wx.ALL, 5 )
        
        self.m_dirPicker1 = wx.DirPickerCtrl( self.m_wizPage3, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
        bSizer5.Add( self.m_dirPicker1, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        self.m_wizPage3.SetSizer( bSizer5 )
        self.m_wizPage3.Layout()
        bSizer5.Fit( self.m_wizPage3 )
        self.m_wizPage4 = wx.wizard.WizardPageSimple( self  )
        self.add_page( self.m_wizPage4 )
        
        bSizer7 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText8 = wx.StaticText( self.m_wizPage4, wx.ID_ANY, u"Filter out Scans", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        self.m_staticText8.SetFont( wx.Font( 14, 74, 90, 92, False, "Arial" ) )
        
        bSizer7.Add( self.m_staticText8, 0, wx.ALL, 5 )
        
        
        bSizer7.AddSpacer( ( 0, 5), 0, wx.EXPAND, 0 )
        
        self.m_staticline2 = wx.StaticLine( self.m_wizPage4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer7.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )
        
        bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText9 = wx.StaticText( self.m_wizPage4, wx.ID_ANY, u"By Retention Time", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9.Wrap( -1 )
        bSizer21.Add( self.m_staticText9, 0, wx.ALL, 5 )
        
        
        bSizer21.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_checkBox41 = wx.CheckBox( self.m_wizPage4, wx.ID_ANY, u"select", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_checkBox41.SetFont( wx.Font( 8, 74, 93, 90, False, "Arial" ) )
        
        bSizer21.Add( self.m_checkBox41, 0, wx.ALL, 5 )
        
        
        bSizer7.Add( bSizer21, 0, wx.EXPAND, 5 )
        
        bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText10 = wx.StaticText( self.m_wizPage4, wx.ID_ANY, u"In Seconds from:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10.Wrap( -1 )
        bSizer8.Add( self.m_staticText10, 0, wx.ALL, 5 )
        
        self.m_textCtrl4 = wx.TextCtrl( self.m_wizPage4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_textCtrl4, 0, wx.ALL, 5 )
        
        self.m_staticText11 = wx.StaticText( self.m_wizPage4, wx.ID_ANY, u" to: ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )
        bSizer8.Add( self.m_staticText11, 0, wx.ALL, 5 )
        
        self.m_textCtrl5 = wx.TextCtrl( self.m_wizPage4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8.Add( self.m_textCtrl5, 0, wx.ALL, 5 )
        
        
        bSizer7.Add( bSizer8, 0, 0, 5 )
        
        self.m_staticline3 = wx.StaticLine( self.m_wizPage4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer7.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )
        
        bSizer211 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText93 = wx.StaticText( self.m_wizPage4, wx.ID_ANY, u"By Header Text", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText93.Wrap( -1 )
        bSizer211.Add( self.m_staticText93, 0, wx.ALL, 5 )
        
        
        bSizer211.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_checkBox411 = wx.CheckBox( self.m_wizPage4, wx.ID_ANY, u"select", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_checkBox411.SetFont( wx.Font( 8, 74, 93, 90, False, "Arial" ) )
        
        bSizer211.Add( self.m_checkBox411, 0, wx.ALL, 5 )
        
        
        bSizer7.Add( bSizer211, 1, wx.EXPAND, 5 )
        
        bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_textCtrl6 = wx.TextCtrl( self.m_wizPage4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.m_textCtrl6, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.m_checkBox4 = wx.CheckBox( self.m_wizPage4, wx.ID_ANY, u"Keep Scans (or discard)", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.m_checkBox4, 0, wx.ALL, 5 )
        
        
        bSizer7.Add( bSizer9, 0, wx.EXPAND, 5 )
        
        self.m_staticline4 = wx.StaticLine( self.m_wizPage4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer7.Add( self.m_staticline4, 0, wx.EXPAND|wx.ALL, 5 )
        
        bSizer2111 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText931 = wx.StaticText( self.m_wizPage4, wx.ID_ANY, u"By Scans Sample", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText931.Wrap( -1 )
        bSizer2111.Add( self.m_staticText931, 0, wx.ALL, 5 )
        
        
        bSizer2111.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_checkBox4111 = wx.CheckBox( self.m_wizPage4, wx.ID_ANY, u"select", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_checkBox4111.SetFont( wx.Font( 8, 74, 93, 90, False, "Arial" ) )
        
        bSizer2111.Add( self.m_checkBox4111, 0, wx.ALL, 5 )
        
        
        bSizer7.Add( bSizer2111, 1, wx.EXPAND, 5 )
        
        bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText15 = wx.StaticText( self.m_wizPage4, wx.ID_ANY, u"Select 1 out of every ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )
        bSizer10.Add( self.m_staticText15, 0, wx.ALL, 5 )
        
        self.m_textCtrl7 = wx.TextCtrl( self.m_wizPage4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer10.Add( self.m_textCtrl7, 0, wx.ALL, 5 )
        
        self.m_staticText16 = wx.StaticText( self.m_wizPage4, wx.ID_ANY, u"Scans", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText16.Wrap( -1 )
        bSizer10.Add( self.m_staticText16, 0, wx.ALL, 5 )
        
        
        bSizer7.Add( bSizer10, 1, wx.EXPAND, 5 )
        
        
        self.m_wizPage4.SetSizer( bSizer7 )
        self.m_wizPage4.Layout()
        bSizer7.Fit( self.m_wizPage4 )
        self.m_wizPage5 = wx.wizard.WizardPageSimple( self  )
        self.add_page( self.m_wizPage5 )
        
        bSizer71 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText81 = wx.StaticText( self.m_wizPage5, wx.ID_ANY, u"Prefilter Peaks", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText81.Wrap( -1 )
        self.m_staticText81.SetFont( wx.Font( 14, 74, 90, 92, False, "Arial" ) )
        
        bSizer71.Add( self.m_staticText81, 0, wx.ALL, 5 )
        
        
        bSizer71.AddSpacer( ( 0, 5), 0, wx.EXPAND, 0 )
        
        self.m_staticline21 = wx.StaticLine( self.m_wizPage5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer71.Add( self.m_staticline21, 0, wx.EXPAND |wx.ALL, 5 )
        
        bSizer21111 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText9311 = wx.StaticText( self.m_wizPage5, wx.ID_ANY, u"Group by Decimal Places", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9311.Wrap( -1 )
        bSizer21111.Add( self.m_staticText9311, 0, wx.ALL, 5 )
        
        
        bSizer21111.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_checkBox41111 = wx.CheckBox( self.m_wizPage5, wx.ID_ANY, u"select", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_checkBox41111.SetFont( wx.Font( 8, 74, 93, 90, False, "Arial" ) )
        
        bSizer21111.Add( self.m_checkBox41111, 0, wx.ALL, 5 )
        
        
        bSizer71.Add( bSizer21111, 0, wx.EXPAND, 5 )
        
        bSizer81 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText101 = wx.StaticText( self.m_wizPage5, wx.ID_ANY, u"Decimal Places", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText101.Wrap( -1 )
        bSizer81.Add( self.m_staticText101, 0, wx.ALL, 5 )
        
        self.m_textCtrl41 = wx.TextCtrl( self.m_wizPage5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer81.Add( self.m_textCtrl41, 0, wx.ALL, 5 )
        
        self.m_staticText111 = wx.StaticText( self.m_wizPage5, wx.ID_ANY, u"Min Group count", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText111.Wrap( -1 )
        bSizer81.Add( self.m_staticText111, 0, wx.ALL, 5 )
        
        self.m_textCtrl51 = wx.TextCtrl( self.m_wizPage5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer81.Add( self.m_textCtrl51, 0, wx.ALL, 5 )
        
        
        bSizer71.Add( bSizer81, 0, 0, 5 )
        
        self.m_staticline31 = wx.StaticLine( self.m_wizPage5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer71.Add( self.m_staticline31, 0, wx.EXPAND |wx.ALL, 5 )
        
        bSizer21112 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText9312 = wx.StaticText( self.m_wizPage5, wx.ID_ANY, u"Repeat until:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText9312.Wrap( -1 )
        bSizer21112.Add( self.m_staticText9312, 0, wx.ALL, 5 )
        
        
        bSizer21112.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_checkBox41112 = wx.CheckBox( self.m_wizPage5, wx.ID_ANY, u"select", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_checkBox41112.SetFont( wx.Font( 8, 74, 93, 90, False, "Arial" ) )
        
        bSizer21112.Add( self.m_checkBox41112, 0, wx.ALL, 5 )
        
        
        bSizer71.Add( bSizer21112, 0, wx.EXPAND, 5 )
        
        bSizer811 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText1011 = wx.StaticText( self.m_wizPage5, wx.ID_ANY, u"Peak count is", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1011.Wrap( -1 )
        bSizer811.Add( self.m_staticText1011, 0, wx.ALL, 5 )
        
        self.m_textCtrl411 = wx.TextCtrl( self.m_wizPage5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer811.Add( self.m_textCtrl411, 0, wx.ALL, 5 )
        
        self.m_staticText1111 = wx.StaticText( self.m_wizPage5, wx.ID_ANY, u"percent of original, ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1111.Wrap( -1 )
        bSizer811.Add( self.m_staticText1111, 0, wx.ALL, 5 )
        
        
        bSizer71.Add( bSizer811, 0, wx.EXPAND, 5 )
        
        bSizer8111 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText10111 = wx.StaticText( self.m_wizPage5, wx.ID_ANY, u"With at least ", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText10111.Wrap( -1 )
        bSizer8111.Add( self.m_staticText10111, 0, wx.ALL, 5 )
        
        self.m_textCtrl4111 = wx.TextCtrl( self.m_wizPage5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer8111.Add( self.m_textCtrl4111, 0, wx.ALL, 5 )
        
        self.m_staticText11111 = wx.StaticText( self.m_wizPage5, wx.ID_ANY, u"peaks", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11111.Wrap( -1 )
        bSizer8111.Add( self.m_staticText11111, 0, wx.ALL, 5 )
        
        
        bSizer71.Add( bSizer8111, 0, wx.EXPAND, 5 )
        
        
        self.m_wizPage5.SetSizer( bSizer71 )
        self.m_wizPage5.Layout()
        bSizer71.Fit( self.m_wizPage5 )
        self.m_wizPage6 = wx.wizard.WizardPageSimple( self  )
        self.add_page( self.m_wizPage6 )
        
        bSizer72 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText82 = wx.StaticText( self.m_wizPage6, wx.ID_ANY, u"Generate Bins", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText82.Wrap( -1 )
        self.m_staticText82.SetFont( wx.Font( 14, 74, 90, 92, False, "Arial" ) )
        
        bSizer72.Add( self.m_staticText82, 0, wx.ALL, 5 )
        
        
        bSizer72.AddSpacer( ( 0, 5), 0, wx.EXPAND, 0 )
        
        self.m_staticline22 = wx.StaticLine( self.m_wizPage6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer72.Add( self.m_staticline22, 0, wx.EXPAND |wx.ALL, 5 )
        
        bSizer211121 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText93121 = wx.StaticText( self.m_wizPage6, wx.ID_ANY, u"By Peak Mass", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText93121.Wrap( -1 )
        bSizer211121.Add( self.m_staticText93121, 0, wx.ALL, 5 )
        
        
        bSizer211121.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_checkBox411121 = wx.CheckBox( self.m_wizPage6, wx.ID_ANY, u"select", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_checkBox411121.SetFont( wx.Font( 8, 74, 93, 90, False, "Arial" ) )
        
        bSizer211121.Add( self.m_checkBox411121, 0, wx.ALL, 5 )
        
        
        bSizer72.Add( bSizer211121, 1, wx.EXPAND, 5 )
        
        bSizer82 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText102 = wx.StaticText( self.m_wizPage6, wx.ID_ANY, u"Number of decimal Places", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText102.Wrap( -1 )
        bSizer82.Add( self.m_staticText102, 0, wx.ALL, 5 )
        
        self.m_textCtrl42 = wx.TextCtrl( self.m_wizPage6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer82.Add( self.m_textCtrl42, 0, wx.ALL, 5 )
        
        self.m_staticText112 = wx.StaticText( self.m_wizPage6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText112.Wrap( -1 )
        bSizer82.Add( self.m_staticText112, 0, wx.ALL, 5 )
        
        
        bSizer72.Add( bSizer82, 0, 0, 5 )
        
        self.m_staticline32 = wx.StaticLine( self.m_wizPage6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer72.Add( self.m_staticline32, 0, wx.EXPAND |wx.ALL, 5 )
        
        bSizer211122 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText93122 = wx.StaticText( self.m_wizPage6, wx.ID_ANY, u"By Peak Resolution", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText93122.Wrap( -1 )
        bSizer211122.Add( self.m_staticText93122, 0, wx.ALL, 5 )
        
        
        bSizer211122.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_checkBox411122 = wx.CheckBox( self.m_wizPage6, wx.ID_ANY, u"select", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_checkBox411122.SetFont( wx.Font( 8, 74, 93, 90, False, "Arial" ) )
        
        bSizer211122.Add( self.m_checkBox411122, 0, wx.ALL, 5 )
        
        
        bSizer72.Add( bSizer211122, 1, wx.EXPAND, 5 )
        
        bSizer91 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText62 = wx.StaticText( self.m_wizPage6, wx.ID_ANY, u"Number of decimal places", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText62.Wrap( -1 )
        bSizer91.Add( self.m_staticText62, 0, wx.ALL, 5 )
        
        self.m_textCtrl61 = wx.TextCtrl( self.m_wizPage6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer91.Add( self.m_textCtrl61, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer72.Add( bSizer91, 0, wx.EXPAND, 5 )
        
        self.m_staticline41 = wx.StaticLine( self.m_wizPage6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer72.Add( self.m_staticline41, 0, wx.EXPAND|wx.ALL, 5 )
        
        bSizer211123 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText93123 = wx.StaticText( self.m_wizPage6, wx.ID_ANY, u"By Resolution Trend Line", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText93123.Wrap( -1 )
        bSizer211123.Add( self.m_staticText93123, 0, wx.ALL, 5 )
        
        
        bSizer211123.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_checkBox411123 = wx.CheckBox( self.m_wizPage6, wx.ID_ANY, u"select", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_checkBox411123.SetFont( wx.Font( 8, 74, 93, 90, False, "Arial" ) )
        
        bSizer211123.Add( self.m_checkBox411123, 0, wx.ALL, 5 )
        
        
        bSizer72.Add( bSizer211123, 1, wx.EXPAND, 5 )
        
        bSizer101 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText151 = wx.StaticText( self.m_wizPage6, wx.ID_ANY, u"Number of decimal places", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText151.Wrap( -1 )
        bSizer101.Add( self.m_staticText151, 0, wx.ALL, 5 )
        
        self.m_textCtrl71 = wx.TextCtrl( self.m_wizPage6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer101.Add( self.m_textCtrl71, 0, wx.ALL, 5 )
        
        
        bSizer72.Add( bSizer101, 1, wx.EXPAND, 5 )
        
        
        self.m_wizPage6.SetSizer( bSizer72 )
        self.m_wizPage6.Layout()
        bSizer72.Fit( self.m_wizPage6 )
        self.m_wizPage7 = wx.wizard.WizardPageSimple( self  )
        self.add_page( self.m_wizPage7 )
        
        bSizer721 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText821 = wx.StaticText( self.m_wizPage7, wx.ID_ANY, u"Peak Sorting", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText821.Wrap( -1 )
        self.m_staticText821.SetFont( wx.Font( 14, 74, 90, 92, False, "Arial" ) )
        
        bSizer721.Add( self.m_staticText821, 0, wx.ALL, 5 )
        
        
        bSizer721.AddSpacer( ( 0, 5), 0, wx.EXPAND, 0 )
        
        self.m_staticline221 = wx.StaticLine( self.m_wizPage7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer721.Add( self.m_staticline221, 0, wx.EXPAND |wx.ALL, 5 )
        
        bSizer2111211 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText931211 = wx.StaticText( self.m_wizPage7, wx.ID_ANY, u"In First Matching Bin", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText931211.Wrap( -1 )
        bSizer2111211.Add( self.m_staticText931211, 0, wx.ALL, 5 )
        
        
        bSizer2111211.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_checkBox4111211 = wx.CheckBox( self.m_wizPage7, wx.ID_ANY, u"select", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_checkBox4111211.SetFont( wx.Font( 8, 74, 93, 90, False, "Arial" ) )
        
        bSizer2111211.Add( self.m_checkBox4111211, 0, wx.ALL, 5 )
        
        
        bSizer721.Add( bSizer2111211, 1, wx.EXPAND, 5 )
        
        self.m_staticline321 = wx.StaticLine( self.m_wizPage7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer721.Add( self.m_staticline321, 0, wx.EXPAND |wx.ALL, 5 )
        
        bSizer2111212 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText931212 = wx.StaticText( self.m_wizPage7, wx.ID_ANY, u"Sort Close Bin", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText931212.Wrap( -1 )
        bSizer2111212.Add( self.m_staticText931212, 0, wx.ALL, 5 )
        
        
        bSizer2111212.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_checkBox4111212 = wx.CheckBox( self.m_wizPage7, wx.ID_ANY, u"select", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_checkBox4111212.SetFont( wx.Font( 8, 74, 93, 90, False, "Arial" ) )
        
        bSizer2111212.Add( self.m_checkBox4111212, 0, wx.ALL, 5 )
        
        
        bSizer721.Add( bSizer2111212, 1, wx.EXPAND, 5 )
        
        bSizer911 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText621 = wx.StaticText( self.m_wizPage7, wx.ID_ANY, u"Window Size", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText621.Wrap( -1 )
        bSizer911.Add( self.m_staticText621, 0, wx.ALL, 5 )
        
        self.m_textCtrl611 = wx.TextCtrl( self.m_wizPage7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer911.Add( self.m_textCtrl611, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer721.Add( bSizer911, 0, wx.EXPAND, 5 )
        
        self.m_staticline411 = wx.StaticLine( self.m_wizPage7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer721.Add( self.m_staticline411, 0, wx.EXPAND|wx.ALL, 5 )
        
        bSizer2111213 = wx.BoxSizer( wx.HORIZONTAL )
        
        self.m_staticText931213 = wx.StaticText( self.m_wizPage7, wx.ID_ANY, u"Sort in Narrowest Bin", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText931213.Wrap( -1 )
        bSizer2111213.Add( self.m_staticText931213, 0, wx.ALL, 5 )
        
        
        bSizer2111213.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_checkBox4111213 = wx.CheckBox( self.m_wizPage7, wx.ID_ANY, u"select", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.m_checkBox4111213.SetFont( wx.Font( 8, 74, 93, 90, False, "Arial" ) )
        
        bSizer2111213.Add( self.m_checkBox4111213, 0, wx.ALL, 5 )
        
        
        bSizer721.Add( bSizer2111213, 1, wx.EXPAND, 5 )
        
        
        self.m_wizPage7.SetSizer( bSizer721 )
        self.m_wizPage7.Layout()
        bSizer721.Fit( self.m_wizPage7 )
        
        
        self.m_wizPage8 = wx.wizard.WizardPageSimple( self  )
        self.add_page( self.m_wizPage8 )
        
        bSizer55 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText65 = wx.StaticText( self.m_wizPage8, wx.ID_ANY, u"Process File", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText65.Wrap( -1 )
        bSizer55.Add( self.m_staticText65, 0, wx.ALL, 5 )
        
        self.m_textCtrl18_sysout = wx.TextCtrl( self.m_wizPage8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_DONTWRAP|wx.TE_MULTILINE|wx.TE_READONLY )
        bSizer55.Add( self.m_textCtrl18_sysout, 1, wx.ALL|wx.EXPAND, 5 )
        
        self.m_gauge1_progress = wx.Gauge( self.m_wizPage8, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.m_gauge1_progress.SetValue( 0 ) 
        bSizer55.Add( self.m_gauge1_progress, 0, wx.ALL|wx.EXPAND, 5 )
        
        
        self.m_wizPage8.SetSizer( bSizer55 )
        self.m_wizPage8.Layout()
        bSizer55.Fit( self.m_wizPage8 )
        self.m_wizPage9 = wx.wizard.WizardPageSimple( self  )
        self.add_page( self.m_wizPage9 )
        
        bSizer56 = wx.BoxSizer( wx.VERTICAL )
        
        self.m_staticText8211 = wx.StaticText( self.m_wizPage9, wx.ID_ANY, u"Finish", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8211.Wrap( -1 )
        self.m_staticText8211.SetFont( wx.Font( 14, 74, 90, 92, False, "Arial" ) )
        
        bSizer56.Add( self.m_staticText8211, 0, wx.ALL, 5 )
        
        
        bSizer56.AddSpacer( ( 0, 0), 0, wx.EXPAND, 5 )
        
        self.m_checkBox22_open_dir = wx.CheckBox( self.m_wizPage9, wx.ID_ANY, u"Open Directory", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_checkBox22_open_dir.SetValue(True) 
        bSizer56.Add( self.m_checkBox22_open_dir, 1, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 5 )
        
        
        self.m_wizPage9.SetSizer( bSizer56 )
        self.m_wizPage9.Layout()
        bSizer56.Fit( self.m_wizPage9 )
        self.Centre( wx.BOTH )
        
        self.setCustomPageOrder()
        
        # Connect Events
        self.Bind( wx.wizard.EVT_WIZARD_FINISHED, self.wizardFinished )
        self.Bind( wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.pageChanging )
        self.m_filePicker1.Bind( wx.EVT_FILEPICKER_CHANGED, self.fileSelected )
        self.m_checkBox9.Bind( wx.EVT_CHECKBOX, self.enable_m_filePicker3configfile )
        
        
        
    def add_page(self, page):
        if self.m_pages:
            previous_page = self.m_pages[-1]
            page.SetPrev(previous_page)
            previous_page.SetNext(page)
        self.m_pages.append(page)
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def wizardFinished( self, event ):
        if self.m_checkBox22_open_dir.IsChecked():
            if self.m_dirPicker1.GetTextCtrlValue():
                subprocess.call("explorer /select,'"+self.m_dirPicker1.GetTextCtrlValue()+"'", shell=True)
            else:
                subprocess.call("explorer .", shell=True)
    

    def buildComand(self):
        command = []
        command.append(sys.executable) # not sure why, but it works
        command.append("msbf.py")
        command.append(self.m_filePicker1.TextCtrlValue)
        
        if self.m_checkBox2.IsChecked():
            command.append('--csv')
        
        if self.m_filePicker2.TextCtrlValue:
            command.append('-c')
            command.append(self.m_filePicker2.TextCtrlValue)
        
        vees = '-'
        for i in range(self.m_slider1.Value): vees = vees + 'v' 
        command.append(vees)
        
        #Filter out Scans
#         if not(not self.m_checkBox41 and not self.m_checkBox411 and not self.m_checkBox4111):
#             d = MessageDialog(self, 'please go back and correct the entries', 'THERE WAS AN ERROR' , wx.OK | wx.ICON_INFORMATION)
#             d.ShowModal()
#             d.Destroy()
#                     
        if self.m_checkBox41.IsChecked() or self.m_textCtrl4.GetValue():
            command.append('--filterRetentionTime')
            command.append(self.m_textCtrl4.GetValue())
            command.append(self.m_textCtrl5.GetValue())
            
        if  self.m_checkBox411.IsChecked() or self.m_textCtrl6.GetValue():
            command.append('--filterText')
            command.append(self.m_textCtrl6.GetValue())
            if self.m_checkBox4.IsChecked() and self.m_textCtrl6.GetValue():
                command.append('True')
            if not self.m_checkBox4.IsChecked() and self.m_textCtrl6.GetValue():
                command.append('False')
        
        if self.m_checkBox4111.IsChecked() or self.m_textCtrl7.GetValue():
            command.append('--filterSamples')
            command.append(self.m_textCtrl7.GetValue())
        
        #Prefilter Peaks
        if self.m_checkBox41111.IsChecked() or self.m_textCtrl41.GetValue():
            command.append('--prefilter')
            command.append(self.m_textCtrl41.GetValue())
            command.append(self.m_textCtrl51.GetValue())
        
        if self.m_checkBox41112.IsChecked() or self.m_textCtrl411.GetValue():
            command.append('--preliminaryReductionFilter')
            command.append(self.m_textCtrl411.GetValue())
            command.append(self.m_textCtrl4111.GetValue())
        
        #Generate Bins
        if self.m_checkBox411121.IsChecked() or self.m_textCtrl42.GetValue():
            command.append('--binsDecimal')
            command.append(self.m_textCtrl42.GetValue())
        if self.m_checkBox411122.IsChecked() or self.m_textCtrl61.GetValue():
            command.append('--binsResolution')
            command.append(self.m_textCtrl61.GetValue())
        if self.m_checkBox411123.IsChecked() or self.m_textCtrl71.GetValue():
            command.append('--binsTheoResolution')
            command.append(self.m_textCtrl71.GetValue())
        
        #Peak Sorting
        if self.m_checkBox4111211.IsChecked():
            command.append('--inFirstBin')
        if self.m_checkBox4111212.IsChecked() or self.m_textCtrl611.GetValue():
            command.append('--inWindowBin')
            command.append(self.m_textCtrl611.GetValue())
        if self.m_checkBox4111213.IsChecked():
            command.append('--inNarrowBin')
            
#         this one must be last because its positional
        if self.m_dirPicker1.TextCtrlValue:
            command.append(self.m_dirPicker1.TextCtrlValue)
        
            
        
        return command
    
    def streamTopage6_OK(self):
        self.m_textCtrl18_sysout.AppendText("Staring command..."+ "\n")
        command = self.buildComand()
        self.m_textCtrl18_sysout.AppendText(' '.join(command))
        self.m_textCtrl18_sysout.AppendText("\n")
        self.m_textCtrl18_sysout.AppendText("Please wait this may take some time"+ "\n")
        
        theproc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = theproc.communicate()
        self.m_textCtrl18_sysout.AppendText(out)
        self.m_textCtrl18_sysout.AppendText('------------------------\n')
        
        if theproc.returncode != 0:
            d = MessageDialog(self, 'please go back and correct the entries', 'THERE WAS AN ERROR' , wx.OK | wx.ICON_INFORMATION)
            d.ShowModal()
            d.Destroy()
        
        return theproc.returncode == 0
        
    
    def pageChanging( self, event ):
        if (event.GetPage() == self.m_pages[6] and event.GetDirection()):
            isOK = self.streamTopage6_OK()
            if isOK:
                event.Allow()
            else:
                event.Veto()
    
    def fileSelected( self, event ):
        event.Skip()
        
        
    def enable_m_filePicker3configfile( self, event ):
        if(not event.Checked()):
            thispage = self.m_pages[0]
            semilastpage = self.m_pages[-2]
            thispage.SetNext(semilastpage)
            semilastpage.SetPrev(thispage)
        else:
            thispage = self.m_pages[0]
            thispage.SetNext(self.m_pages[1])
    
    def setCustomPageOrder(self):
        
        thispage = self.m_pages[0]
        semilastpage = self.m_pages[-2]
        thispage.SetNext(semilastpage)
        semilastpage.SetPrev(thispage)
    
def main():
     wizard = MyWizard1(None)
     wizard.FitToPage(wizard.m_pages[3])
     wizard.RunWizard(wizard.m_pages[0])
     wizard.Destroy()

if __name__ == '__main__':
    app = wx.App(False)
    main()
    app.MainLoop()