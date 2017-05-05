'''
Created on 04.05.2017

@author: mirandaa
'''
from msBinFilterGUI import MyFrame2
import wx
from FileDialog import FileDialog
import os


class MyFrame(MyFrame2):
    
    def __init__(self, parent):
        super(MyFrame, self).__init__(parent)
        
   # Virtual event handlers, overide them in your derived class
    def clickedBrowse( self, event ):
        wildcard = "spectra (*.mzXML)|*.mzXML;*mzxml"
        dlg = wx.FileDialog(self, message="Select your files",defaultDir=os.getcwd(),defaultFile="*.mzXML", wildcard=wildcard, style=wx.OPEN|wx.MULTIPLE)

        if dlg.ShowModal() == wx.ID_OK:
                path, file = os.path.split(dlg.GetPath())
                fileNames = dlg.GetFilenames()
                 
                self.m_textCtrl1.SetValue(str(path).replace('\\\\', '\\')+' '+ str(len(fileNames))+' files')
                # ----
                self.m_buttonFinish.Enable(True)
    
    def clickedCustomize( self, event ):
        self.m_panel4.Enable(False)
        
                 
    
    
def main():
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()