#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx

class SimpleMenu(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(500, 500))
        menubar = wx.MenuBar()
        archivo = wx.Menu()
        archivo.Append(-1, 'Salir', 'Salir de la Aplicación')
        menubar.Append(archivo, '&Archivo')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=1)
        self.Centre()
        self.Show(True)
        
    def OnQuit(self, event):
        self.Close()
def main():
    app = wx.App()
    SimpleMenu(None,-1,"balanza")
    app.MainLoop()

if __name__ == '__main__':
    main()

