'''
Created on 26.05.2017

@author: mirandaa
'''
from simStitcherGUI import SimStitcherFrame
import wx

def main():
    app = wx.App(False)
    frame = SimStitcherFrame(None)
    frame.Show(True)
    app.MainLoop()

if __name__ == '__main__':
    main()