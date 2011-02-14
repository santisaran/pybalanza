import wx
import sys, random
import gettext
_ = gettext.gettext

data=[]

class ListaFrame(wx.Frame):
    def __init__(self,data):
        wx.Frame.__init__(self, None, -1,
                          "wx.ListCtrl in wx.LC_REPORT mode",
                          size=(600,400), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        #self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        self.lista = wx.ListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.VSCROLL)
        bSizer1.Add(self.lista, 1, wx.ALL|wx.EXPAND, 5)
        
        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        
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
        self.m_menuItem1 = wx.MenuItem( self.m_menu1, wx.ID_ANY, _("Abrir"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.AppendItem( self.m_menuItem1 )
        
        self.m_menuItem2 = wx.MenuItem( self.m_menu1, wx.ID_ANY, _("Guardar"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.AppendItem( self.m_menuItem2 )
        
        self.m_menuItem3 = wx.MenuItem( self.m_menu1, wx.ID_ANY, _("Cerrar"), wx.EmptyString, wx.ITEM_NORMAL )
        self.m_menu1.AppendItem( self.m_menuItem3 )
        
        self.m_menubar1.Append( self.m_menu1, _("Lista") ) 
        
        self.SetMenuBar( self.m_menubar1 )
        
        
        # Add some columns
        for col, text in [[0,"ID"],[1,"peso"],[2,"timestamp"]]:
            self.lista.InsertColumn(col, text)

        # add the rows
        for item in data:
            index = self.lista.InsertStringItem(sys.maxint, str(item[0]))
            for col, text in enumerate(item[1:]):
                self.lista.SetStringItem(index, col+1, text)

        # set the width of the columns in various ways
        self.lista.SetColumnWidth(0, 50)
        self.lista.SetColumnWidth(1, 150)
        self.lista.SetColumnWidth(2, 150)
        #self.lista.SetColumnWidth(3, wx.LIST_AUTOSIZE_USEHEADER)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = ListaFrame(data)
    frame.Show()
    app.MainLoop()
    
