'''
Created on 26.05.2017

@author: mirandaa
'''
from simStitcherGUI import SimStitcherFrame
import wx
from lib.simStitching.simStitcher import simStitcher
import os

class mySimStitcherFrame(SimStitcherFrame):
    def __init__(self,parent):
        super(mySimStitcherFrame, self).__init__(parent)
    
    def browseClicked( self, event ):
#         doCompare = self.m_checkBox1.GetValue()
#         simStitcher(filepath, doCompare)
        wildcard = "mzXML (*.mzXML)|*.mzxml;*MZXML"
        dlg = wx.FileDialog(self, message="Select your files",defaultDir=os.getcwd(),defaultFile="*.mzXML", wildcard=wildcard, style=wx.OPEN|wx.MULTIPLE)
 
        if dlg.ShowModal() == wx.ID_OK:
            self.path, file = os.path.split(dlg.GetPath())
            self.fileNames = dlg.GetFilenames()
                  
            self.m_textCtrl1.SetValue(str(self.path).replace('\\\\', '\\')+' '+ str(len(self.fileNames))+' files')
            self.m_button2.Enable(True)
            self.m_gauge1.SetValue(0)
    

    def clickStart( self, event ):
        self.run_all()
    
    def checkCompare( self, event ):
        self.m_radioBtn3.Enable(self.m_checkBox1.GetValue())
        self.m_radioBtn4.Enable(self.m_checkBox1.GetValue())
    
    def radioDefault( self, event ):
        self.RadioCustom(event)
    
    def RadioCustom( self, event ):
        self.m_textCtrl_a.Enable(self.m_radioBtn4.GetValue())
        self.m_textCtrl_b.Enable(self.m_radioBtn4.GetValue())


    def get_a(self):
        if self.m_radioBtn3.GetValue(): return None # its default
        try:
            return float(self.m_textCtrl_a.GetValue())
        except ValueError:
            dlg = wx.MessageDialog(self, 'There was a problem with value a {} \n it will not be used'.format(self.m_textCtrl_a.GetValue()), 'Warning', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
            raise ValueError('text must be a float')
    
    def get_b(self):
        if self.m_radioBtn3.GetValue(): return None # its default
        try:
            return float(self.m_textCtrl_b.GetValue())
        except ValueError:
            dlg = wx.MessageDialog(self, 'There was a problem with value b {} \n it will not be used'.format(self.m_textCtrl_b.GetValue()), 'Warning', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
            raise ValueError('text must be a float')
    
    def run_all(self):
#         self.path
#         self.fileNames
        gaugeStep = 100.0/(len(self.fileNames)+1)
        doCompare = self.m_checkBox1.GetValue()
        
        for onefile in self.fileNames:
            filepath = str(self.path+'\\'+onefile)
            self.m_gauge1.SetValue(self.m_gauge1.GetValue() + gaugeStep)
            try:
                simStitcher(filepath, doCompare, a=self.get_a(),b=self.get_b(), loglevel = int(self.m_slider1.GetValue()))
                self.m_gauge1.SetValue(self.m_gauge1.GetValue() + gaugeStep)
            except :
                dlg = wx.MessageDialog(self, 'There was a problem processing the file {}'.format(onefile), 'Warning', wx.OK | wx.ICON_WARNING)
                dlg.ShowModal()
                dlg.Destroy()
                self.m_gauge1.SetValue(self.m_gauge1.GetValue() - gaugeStep)
        raise SystemExit
            
    
def main():
    app = wx.App(False)
    frame = mySimStitcherFrame(None)
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()