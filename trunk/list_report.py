import wx
import os, sys, random
import gettext
_ = gettext.gettext
wildcard = "Texto Separado por comas (*.cvs)|*.cvs|"     \
           "All files (*.*)|*.*"

data=[["0","1002","20110212121200"],["1","1002","20110212121201"],["2","1002","20110212121202"],
    ["3","1002","20110212121203"],["4","1002","20110212121204"]]
columnas = ["ID","Peso","TimeStamp"]
class ListaFrame(wx.Frame):
    def __init__(self,datos,columnas=columnas):
        wx.Frame.__init__(self, None, -1,
                          "wx.ListCtrl in wx.LC_REPORT mode",
                          size=(600,400), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        #self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        self.lista = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.VSCROLL)
        bSizer1.Add(self.lista, 1, wx.ALL|wx.EXPAND, 5)
			
        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.data = datos
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, "Unidad")
        self.m_staticText1.Wrap( -1 )
        bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
        bSizer1.Add( bSizer2, 0, wx.EXPAND, 0 )

        self.SetSizer( bSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        m_choice1Choices = [ "gr", "lb", "kg"]
        self.m_choice1 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0 )
        self.m_choice1.SetSelection( 0 )
        bSizer2.Add( self.m_choice1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 0 )


        self.m_menubar1 = wx.MenuBar( 0 )
        self.m_menu1 = wx.Menu()
        self.m_abrir = wx.MenuItem( self.m_menu1, wx.ID_ANY, _("Abrir"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.AppendItem( self.m_abrir )
        
        self.m_guardar = wx.MenuItem( self.m_menu1, wx.ID_ANY, _("Guardar"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.AppendItem( self.m_guardar )
        
        self.m_cerrar = wx.MenuItem( self.m_menu1, wx.ID_ANY, _("Cerrar"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.AppendItem( self.m_cerrar )
        self.m_menubar1.Append( self.m_menu1, _("Lista") ) 
        self.OnPoblar(columnas)
        self.SetMenuBar( self.m_menubar1 )
        self.Bind( wx.EVT_MENU, self.OnMenuAbrir, id = self.m_abrir.GetId() )
        self.Bind( wx.EVT_MENU, self.OnMenuGuardar, id = self.m_guardar.GetId() )
        self.Bind( wx.EVT_MENU, self.OnMenuCerrar, id = self.m_cerrar.GetId() )
        self.m_choice1.Bind( wx.EVT_CHOICE, self.OnChoiceUnidad )
    
    def OnPoblar(self,columnas):
        # Add some columns
        for col, text in enumerate(columnas):#[[0,"ID"],[1,"peso"],[2,"timestamp"]]:
            self.lista.InsertColumn(col, text)
        # add the rows
        for item in self.data:
            index = self.lista.InsertStringItem(sys.maxint, str(item[0]))
            for col, text in enumerate(item[1:]):
                self.lista.SetStringItem(index, col+1, text)

        # set the width of the columns in various ways
        self.lista.SetColumnWidth(0, 50)
        self.lista.SetColumnWidth(1, 150)
        self.lista.SetColumnWidth(2, 150)
        #self.lista.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)
     
    
    def OnChoiceUnidad(self,evt):
        """Cambia de unidad"""
        unidad = self.m_choice1.GetStringSelection()
        
        


    def OnMenuAbrir(self, evt):
        #self.log.WriteText("CWD: %s\n" % os.getcwd())
        """ Crea el dialogo para abrir un archivo. Se fuerza el directorio actual."""
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(), 
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
    
        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
    
            #self.log.WriteText('You selected %d files:' % len(paths))
    
            #for path in paths:
            #   self.log.WriteText('           %s\n' % path)
    
        # Compare this with the debug above; did we change working dirs?
        #self.log.WriteText("CWD: %s\n" % os.getcwd())
    
        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()
    
    def OnMenuGuardar(self, evt):
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=wildcard, style=wx.SAVE
            )

        # This sets the default filter that the user will initially see. Otherwise,
        # the first filter in the list will be used by default.
        dlg.SetFilterIndex(0)

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            #self.log.WriteText('You selected "%s"' % path)

            # Normally, at this point you would save your data using the file and path
            # data that the user provided to you, but since we didn't actually start
            # with any data to work with, that would be difficult.
            # 
            # The code to do so would be similar to this, assuming 'data' contains
            # the data you want to save:
            #
            # fp = file(path, 'w') # Create file anew
            # fp.write(data)
            # fp.close()
            #
            # You might want to add some error checking :-)
            #
 
        # Note that the current working dir didn't change. This is good since
        # that's the way we set it up.
        #self.log.WriteText("CWD: %s\n" % os.getcwd())

        # Destroy the dialog. Don't do this until you are done with it!
        # BAD things can happen otherwise!
        dlg.Destroy()
        
    def OnMenuCerrar(self,evt):
        self.Destroy()
        pass



if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = ListaFrame(data,columnas)
    frame.Show()
    app.MainLoop()
    
