'''
Created on 26.05.2017

@author: mirandaa
'''
from simStitcherGUI import SimStitcherFrame
import wx
from lib.simStitching.simStitcher import simStitcher

class mySimStitcherFrame(SimStitcherFrame):
    def __init__(self,parent):
        super(mySimStitcherFrame, self).__init__(parent)
    
    def filecChanged( self, event ):
        filepath  = self.m_filePicker1.GetPath()
        doCompare = self.m_checkBox1.GetValue()
        simStitcher(filepath, doCompare, self.callback)
    
    def callback(self, message):
        print(message)
        
    
def main():
    app = wx.App(False)
    frame = mySimStitcherFrame(None)
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()