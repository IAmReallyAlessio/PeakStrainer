'''
Created on 04.05.2017

@author: mirandaa
'''
from msBinFilterGUI import MyFrame2
import wx
import os


class MyFrame(MyFrame2):
    
    def __init__(self, parent):
        super(MyFrame, self).__init__(parent)
        
   # Virtual event handlers, overide them in your derived class
    def clickedBrowse( self, event ):
        wildcard = "Thermo raw (*.raw)|*.raw;*RAW"
        dlg = wx.FileDialog(self, message="Select your files",defaultDir=os.getcwd(),defaultFile="*.raw", wildcard=wildcard, style=wx.OPEN|wx.MULTIPLE)

        if dlg.ShowModal() == wx.ID_OK:
                path, file = os.path.split(dlg.GetPath())
                fileNames = dlg.GetFilenames()
                 
                self.m_textCtrl1.SetValue(str(path).replace('\\\\', '\\')+' '+ str(len(fileNames))+' files')
                # ----
                self.m_buttonFinish.Enable(True)
    
    def radioBin( self, event ):
        self.m_staticText23.Enable(self.m_radioBtn1.GetValue())
#         ----
        self.m_staticText231 .Enable(self.m_radioBtn4.GetValue())
        self.m_staticText241 .Enable(self.m_radioBtn4.GetValue())
        self.m_textCtrl61    .Enable(self.m_radioBtn4.GetValue())
        self.m_staticText2511.Enable(self.m_radioBtn4.GetValue())
        self.m_textCtrl711   .Enable(self.m_radioBtn4.GetValue())
        self.m_staticText381 .Enable(self.m_radioBtn4.GetValue())
        self.m_checkBox11    .Enable(self.m_radioBtn4.GetValue())
        self.m_staticText251 .Enable(self.m_radioBtn4.GetValue())
        self.m_textCtrl71    .Enable(self.m_radioBtn4.GetValue())
        self.m_staticText38  .Enable(self.m_radioBtn4.GetValue())
        self.m_staticText2411.Enable(self.m_radioBtn4.GetValue())
        self.m_textCtrl611   .Enable(self.m_radioBtn4.GetValue())

    def radioPre( self, event ):
        self.m_staticText14 .Enable(self.m_radioBtn11.GetValue())
        self.m_spinCtrl2    .Enable(self.m_radioBtn11.GetValue())
        self.m_staticText15 .Enable(self.m_radioBtn11.GetValue())
        self.m_spinCtrl1    .Enable(self.m_radioBtn11.GetValue())       
        self.m_staticText22 .Enable(self.m_radioBtn11.GetValue())
    
def main():
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()