# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame2
###########################################################################

class MyFrame2 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 750,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_MENU ) )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"MS Bin Filter", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		self.m_staticText1.SetFont( wx.Font( 14, 74, 90, 92, False, "Arial" ) )
		
		bSizer2.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer2.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_panel1.SetSizer( bSizer2 )
		self.m_panel1.Layout()
		bSizer2.Fit( self.m_panel1 )
		bSizer3.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )
		
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel3 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText3 = wx.StaticText( self.m_panel3, wx.ID_ANY, u"Select Files:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer6.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl1 = wx.TextCtrl( self.m_panel3, wx.ID_ANY, u"No files Selected...", wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		self.m_textCtrl1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		
		bSizer6.Add( self.m_textCtrl1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_buttonBrowse = wx.Button( self.m_panel3, wx.ID_ANY, u"Browse", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_buttonBrowse, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer5.Add( bSizer6, 0, wx.EXPAND, 5 )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox1 = wx.CheckBox( self.m_panel3, wx.ID_ANY, u"Open Results Directory", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_checkBox1, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer6, 0, 0, 5 )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox2 = wx.CheckBox( self.m_panel3, wx.ID_ANY, u"Open Spectra reorder", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_checkBox2, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer7, 0, 0, 5 )
		
		
		self.m_panel3.SetSizer( bSizer5 )
		self.m_panel3.Layout()
		bSizer5.Fit( self.m_panel3 )
		self.m_notebook1.AddPage( self.m_panel3, u"General", True )
		self.m_panel4 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox8 = wx.CheckBox( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_checkBox8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText31 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"CSV output directory:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText31.Wrap( -1 )
		bSizer10.Add( self.m_staticText31, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_dirPicker1 = wx.DirPickerCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
		bSizer10.Add( self.m_dirPicker1, 1, wx.ALL, 5 )
		
		
		bSizer9.Add( bSizer10, 0, wx.EXPAND, 5 )
		
		self.m_staticline5 = wx.StaticLine( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer9.Add( self.m_staticline5, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox9 = wx.CheckBox( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer11.Add( self.m_checkBox9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText4 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Set log Level:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer11.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText16 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"low", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		bSizer11.Add( self.m_staticText16, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_slider1 = wx.Slider( self.m_panel4, wx.ID_ANY, 1, 1, 5, wx.DefaultPosition, wx.DefaultSize, wx.SL_AUTOTICKS|wx.SL_HORIZONTAL )
		bSizer11.Add( self.m_slider1, 1, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText17 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"high", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		bSizer11.Add( self.m_staticText17, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer9.Add( bSizer11, 0, wx.EXPAND, 5 )
		
		self.m_staticline6 = wx.StaticLine( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer9.Add( self.m_staticline6, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox10 = wx.CheckBox( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_checkBox10, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Use Config file:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer12.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_filePicker2 = wx.FilePickerCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, u"Select a config.ini", u"*.ini", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
		bSizer12.Add( self.m_filePicker2, 1, wx.ALL, 5 )
		
		
		bSizer9.Add( bSizer12, 0, wx.EXPAND, 5 )
		
		
		self.m_panel4.SetSizer( bSizer9 )
		self.m_panel4.Layout()
		bSizer9.Fit( self.m_panel4 )
		self.m_notebook1.AddPage( self.m_panel4, u"Output", False )
		self.m_panel5 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer19 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText7 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"Discard Scans", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		self.m_staticText7.SetFont( wx.Font( 10, 74, 90, 92, False, "Arial" ) )
		
		bSizer19.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.m_staticline9 = wx.StaticLine( self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer19.Add( self.m_staticline9, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox5 = wx.CheckBox( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.m_checkBox5, 0, wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"By Retention Time, from: ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		bSizer21.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl2 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.m_textCtrl2, 0, wx.ALL, 5 )
		
		self.m_staticText9 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"to", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		bSizer21.Add( self.m_staticText9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl3 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.m_textCtrl3, 0, wx.ALL, 5 )
		
		self.m_staticText10 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"in seconds", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		bSizer21.Add( self.m_staticText10, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer19.Add( bSizer21, 0, wx.EXPAND, 5 )
		
		self.m_staticline11 = wx.StaticLine( self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer19.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer23 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox6 = wx.CheckBox( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer23.Add( self.m_checkBox6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText11 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"By Header (filterline) text:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		bSizer23.Add( self.m_staticText11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl4 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer23.Add( self.m_textCtrl4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		m_radioBox1Choices = [ u"including", u"excluding" ]
		self.m_radioBox1 = wx.RadioBox( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, m_radioBox1Choices, 1, wx.RA_SPECIFY_ROWS )
		self.m_radioBox1.SetSelection( 0 )
		bSizer23.Add( self.m_radioBox1, 0, wx.ALL, 5 )
		
		
		bSizer19.Add( bSizer23, 0, wx.EXPAND, 5 )
		
		self.m_staticline12 = wx.StaticLine( self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer19.Add( self.m_staticline12, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer24 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox7 = wx.CheckBox( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer24.Add( self.m_checkBox7, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_staticText12 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"By Sampling, only use 1 out of every", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		bSizer24.Add( self.m_staticText12, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl5 = wx.TextCtrl( self.m_panel5, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer24.Add( self.m_textCtrl5, 0, wx.ALL, 5 )
		
		self.m_staticText13 = wx.StaticText( self.m_panel5, wx.ID_ANY, u"scans", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		bSizer24.Add( self.m_staticText13, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer19.Add( bSizer24, 0, wx.EXPAND, 5 )
		
		
		self.m_panel5.SetSizer( bSizer19 )
		self.m_panel5.Layout()
		bSizer19.Fit( self.m_panel5 )
		self.m_notebook1.AddPage( self.m_panel5, u"Scan Selection", False )
		self.m_panel6 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer25 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline15 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer25.Add( self.m_staticline15, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer43 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_radioBtn10 = wx.RadioButton( self.m_panel6, wx.ID_ANY, u"Use Default", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioBtn10.SetValue( True ) 
		self.m_radioBtn10.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		
		bSizer43.Add( self.m_radioBtn10, 0, wx.ALL, 5 )
		
		
		bSizer25.Add( bSizer43, 0, wx.EXPAND, 5 )
		
		self.m_staticline181 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer25.Add( self.m_staticline181, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtn11 = wx.RadioButton( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer26.Add( self.m_radioBtn11, 0, wx.ALL, 5 )
		
		self.m_staticText14 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Group to decimal place", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		self.m_staticText14.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		
		bSizer26.Add( self.m_staticText14, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_spinCtrl2 = wx.SpinCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 10, 4 )
		bSizer26.Add( self.m_spinCtrl2, 0, wx.ALL, 5 )
		
		self.m_staticText15 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"discard groups with", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		self.m_staticText15.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		
		bSizer26.Add( self.m_staticText15, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_spinCtrl1 = wx.SpinCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 10, 2 )
		bSizer26.Add( self.m_spinCtrl1, 0, wx.ALL, 5 )
		
		self.m_staticText22 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"or less", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText22.Wrap( -1 )
		self.m_staticText22.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		
		bSizer26.Add( self.m_staticText22, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer25.Add( bSizer26, 0, wx.EXPAND, 5 )
		
		self.m_staticline13 = wx.StaticLine( self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer25.Add( self.m_staticline13, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer29 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer28 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox4 = wx.CheckBox( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer28.Add( self.m_checkBox4, 0, wx.ALL, 5 )
		
		self.m_staticText18 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"Repeat until peak count of the group is ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		bSizer28.Add( self.m_staticText18, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_spinCtrl3 = wx.SpinCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 100, 10 )
		bSizer28.Add( self.m_spinCtrl3, 0, wx.ALL, 5 )
		
		self.m_staticText21 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"percent of the original,", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		bSizer28.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer29.Add( bSizer28, 0, wx.EXPAND, 5 )
		
		bSizer30 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText19 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"with a minimum of ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		bSizer30.Add( self.m_staticText19, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_spinCtrl4 = wx.SpinCtrl( self.m_panel6, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 100, 0 )
		bSizer30.Add( self.m_spinCtrl4, 0, wx.ALL, 5 )
		
		self.m_staticText20 = wx.StaticText( self.m_panel6, wx.ID_ANY, u"peaks", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		bSizer30.Add( self.m_staticText20, 0, wx.ALL, 5 )
		
		
		bSizer29.Add( bSizer30, 0, wx.EXPAND, 5 )
		
		
		bSizer25.Add( bSizer29, 0, wx.EXPAND, 5 )
		
		
		self.m_panel6.SetSizer( bSizer25 )
		self.m_panel6.Layout()
		bSizer25.Fit( self.m_panel6 )
		self.m_notebook1.AddPage( self.m_panel6, u"Prefilter Peaks", False )
		self.m_panel7 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer34 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer42 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtn9 = wx.RadioButton( self.m_panel7, wx.ID_ANY, u"Use Default", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioBtn9.SetValue( True ) 
		self.m_radioBtn9.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		
		bSizer42.Add( self.m_radioBtn9, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer34.Add( bSizer42, 1, wx.EXPAND, 5 )
		
		bSizer31 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline16 = wx.StaticLine( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer31.Add( self.m_staticline16, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer32 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtn1 = wx.RadioButton( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer32.Add( self.m_radioBtn1, 0, wx.ALL, 5 )
		
		self.m_staticText23 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"By Resolution based on quadratic function r = a *m/z ^ -b,", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText23.Wrap( -1 )
		self.m_staticText23.SetFont( wx.Font( 9, 74, 90, 90, False, "Arial" ) )
		
		bSizer32.Add( self.m_staticText23, 0, wx.ALL, 5 )
		
		
		bSizer31.Add( bSizer32, 0, wx.EXPAND, 5 )
		
		bSizer33 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText24 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"where a =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText24.Wrap( -1 )
		self.m_staticText24.SetFont( wx.Font( 9, 74, 90, 90, False, "Arial" ) )
		
		bSizer33.Add( self.m_staticText24, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl6 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer33.Add( self.m_textCtrl6, 0, wx.ALL, 5 )
		
		self.m_staticText25 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"and b =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText25.Wrap( -1 )
		self.m_staticText25.SetFont( wx.Font( 9, 74, 90, 90, False, "Arial" ) )
		
		bSizer33.Add( self.m_staticText25, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl7 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer33.Add( self.m_textCtrl7, 0, wx.ALL, 5 )
		
		
		bSizer31.Add( bSizer33, 0, wx.EXPAND, 5 )
		
		self.m_staticline18 = wx.StaticLine( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer31.Add( self.m_staticline18, 0, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer34.Add( bSizer31, 0, wx.EXPAND, 5 )
		
		bSizer36 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtn2 = wx.RadioButton( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer36.Add( self.m_radioBtn2, 0, wx.ALL, 5 )
		
		self.m_staticText26 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"By measured resolution, up to", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText26.Wrap( -1 )
		bSizer36.Add( self.m_staticText26, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_spinCtrl5 = wx.SpinCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 10, 4 )
		bSizer36.Add( self.m_spinCtrl5, 0, wx.ALL, 5 )
		
		self.m_staticText27 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"decimal places", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText27.Wrap( -1 )
		bSizer36.Add( self.m_staticText27, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer34.Add( bSizer36, 0, wx.EXPAND, 5 )
		
		self.m_staticline20 = wx.StaticLine( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer34.Add( self.m_staticline20, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer361 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtn3 = wx.RadioButton( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer361.Add( self.m_radioBtn3, 0, wx.ALL, 5 )
		
		self.m_staticText261 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"By peak m/z, up to", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText261.Wrap( -1 )
		bSizer361.Add( self.m_staticText261, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_spinCtrl51 = wx.SpinCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 10, 4 )
		bSizer361.Add( self.m_spinCtrl51, 0, wx.ALL, 5 )
		
		self.m_staticText271 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"decimal places", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText271.Wrap( -1 )
		bSizer361.Add( self.m_staticText271, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer34.Add( bSizer361, 0, wx.EXPAND, 5 )
		
		bSizer311 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline161 = wx.StaticLine( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer311.Add( self.m_staticline161, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer321 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtn4 = wx.RadioButton( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer321.Add( self.m_radioBtn4, 0, wx.ALL, 5 )
		
		self.m_staticText231 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"By Resolution based on quadratic function r = a *m/z ^ -b, seperate MS1 and MS2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText231.Wrap( -1 )
		self.m_staticText231.SetFont( wx.Font( 9, 74, 90, 90, False, "Arial" ) )
		
		bSizer321.Add( self.m_staticText231, 0, wx.ALL, 5 )
		
		
		bSizer311.Add( bSizer321, 0, wx.EXPAND, 5 )
		
		bSizer331 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText241 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"where a =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText241.Wrap( -1 )
		self.m_staticText241.SetFont( wx.Font( 9, 74, 90, 90, False, "Arial" ) )
		
		bSizer331.Add( self.m_staticText241, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl61 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer331.Add( self.m_textCtrl61, 0, wx.ALL, 5 )
		
		self.m_staticText251 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"and b =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText251.Wrap( -1 )
		self.m_staticText251.SetFont( wx.Font( 9, 74, 90, 90, False, "Arial" ) )
		
		bSizer331.Add( self.m_staticText251, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl71 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer331.Add( self.m_textCtrl71, 0, wx.ALL, 5 )
		
		self.m_staticText38 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"for MS1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText38.Wrap( -1 )
		bSizer331.Add( self.m_staticText38, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer311.Add( bSizer331, 0, wx.EXPAND, 5 )
		
		bSizer3311 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText2411 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"where a =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2411.Wrap( -1 )
		self.m_staticText2411.SetFont( wx.Font( 9, 74, 90, 90, False, "Arial" ) )
		
		bSizer3311.Add( self.m_staticText2411, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl611 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3311.Add( self.m_textCtrl611, 0, wx.ALL, 5 )
		
		self.m_staticText2511 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"and b =", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2511.Wrap( -1 )
		self.m_staticText2511.SetFont( wx.Font( 9, 74, 90, 90, False, "Arial" ) )
		
		bSizer3311.Add( self.m_staticText2511, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_textCtrl711 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3311.Add( self.m_textCtrl711, 0, wx.ALL, 5 )
		
		self.m_staticText381 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"for MS2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText381.Wrap( -1 )
		bSizer3311.Add( self.m_staticText381, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer311.Add( bSizer3311, 0, wx.EXPAND, 5 )
		
		
		bSizer34.Add( bSizer311, 0, wx.EXPAND, 5 )
		
		self.m_staticline162 = wx.StaticLine( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer34.Add( self.m_staticline162, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer38 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox11 = wx.CheckBox( self.m_panel7, wx.ID_ANY, u"Merge overlapping bins", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox11.SetValue(True) 
		bSizer38.Add( self.m_checkBox11, 0, wx.ALL, 5 )
		
		
		bSizer34.Add( bSizer38, 1, wx.EXPAND, 5 )
		
		
		self.m_panel7.SetSizer( bSizer34 )
		self.m_panel7.Layout()
		bSizer34.Fit( self.m_panel7 )
		self.m_notebook1.AddPage( self.m_panel7, u"Bin Type", False )
		self.m_panel8 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer312 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer40 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_radioBtn111 = wx.RadioButton( self.m_panel8, wx.ID_ANY, u"Use Default", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioBtn111.SetFont( wx.Font( 9, 74, 90, 92, False, "Arial" ) )
		
		bSizer40.Add( self.m_radioBtn111, 0, wx.ALL, 5 )
		
		
		bSizer312.Add( bSizer40, 0, wx.EXPAND, 5 )
		
		self.m_staticline131 = wx.StaticLine( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer312.Add( self.m_staticline131, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer322 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtn5 = wx.RadioButton( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer322.Add( self.m_radioBtn5, 0, wx.ALL, 5 )
		
		self.m_staticText36 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Sort peak in first available bin", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText36.Wrap( -1 )
		self.m_staticText36.SetFont( wx.Font( 9, 74, 90, 90, False, "Arial" ) )
		
		bSizer322.Add( self.m_staticText36, 0, wx.ALL, 5 )
		
		
		bSizer312.Add( bSizer322, 0, wx.EXPAND, 5 )
		
		self.m_staticline14 = wx.StaticLine( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer312.Add( self.m_staticline14, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer332 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtn6 = wx.RadioButton( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer332.Add( self.m_radioBtn6, 0, wx.ALL, 5 )
		
		self.m_staticText37 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Sort peak in narrowest available bin", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText37.Wrap( -1 )
		bSizer332.Add( self.m_staticText37, 0, wx.ALL, 5 )
		
		
		bSizer312.Add( bSizer332, 0, wx.EXPAND, 5 )
		
		self.m_staticline151 = wx.StaticLine( self.m_panel8, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer312.Add( self.m_staticline151, 0, wx.EXPAND |wx.ALL, 5 )
		
		bSizer341 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer312.Add( bSizer341, 1, wx.EXPAND, 5 )
		
		bSizer3321 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_radioBtn61 = wx.RadioButton( self.m_panel8, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3321.Add( self.m_radioBtn61, 0, wx.ALL, 5 )
		
		self.m_staticText371 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"Sort peak in narrowest available bin within sort window of", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText371.Wrap( -1 )
		bSizer3321.Add( self.m_staticText371, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_spinCtrl7 = wx.SpinCtrl( self.m_panel8, wx.ID_ANY, u"200", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 10, 1000, 0 )
		bSizer3321.Add( self.m_spinCtrl7, 0, wx.ALL, 5 )
		
		self.m_staticText40 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"peaks", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText40.Wrap( -1 )
		bSizer3321.Add( self.m_staticText40, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		
		bSizer312.Add( bSizer3321, 0, wx.EXPAND, 5 )
		
		
		self.m_panel8.SetSizer( bSizer312 )
		self.m_panel8.Layout()
		bSizer312.Fit( self.m_panel8 )
		self.m_notebook1.AddPage( self.m_panel8, u"Sort Peaks", False )
		self.m_panel9 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer39 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticline17 = wx.StaticLine( self.m_panel9, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer39.Add( self.m_staticline17, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText41 = wx.StaticText( self.m_panel9, wx.ID_ANY, u"Status Log:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText41.Wrap( -1 )
		bSizer39.Add( self.m_staticText41, 0, wx.ALL, 5 )
		
		self.m_textCtrl12 = wx.TextCtrl( self.m_panel9, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer39.Add( self.m_textCtrl12, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		self.m_panel9.SetSizer( bSizer39 )
		self.m_panel9.Layout()
		bSizer39.Fit( self.m_panel9 )
		self.m_notebook1.AddPage( self.m_panel9, u"Status", False )
		
		bSizer3.Add( self.m_notebook1, 9, wx.EXPAND |wx.ALL, 5 )
		
		self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_buttonFinish = wx.Button( self.m_panel2, wx.ID_ANY, u"Finish", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonFinish.Enable( False )
		
		bSizer4.Add( self.m_buttonFinish, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		
		self.m_panel2.SetSizer( bSizer4 )
		self.m_panel2.Layout()
		bSizer4.Fit( self.m_panel2 )
		bSizer3.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_buttonBrowse.Bind( wx.EVT_BUTTON, self.clickedBrowse )
		self.m_buttonFinish.Bind( wx.EVT_BUTTON, self.clickedFinish )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def clickedBrowse( self, event ):
		event.Skip()
	
	def clickedFinish( self, event ):
		event.Skip()
	

