import wx
from wx import xrc
from math import hypot, sin, cos, pi

class Blusb(wx.App):

    def OnInit(self):
        self.res = xrc.XmlResource('balanza.xrc')
        self.frame = self.res.LoadFrame(None, 'MyFrame1')
        self.botonAceptar = xrc.XRCCTRL(self.frame, 'm_button1')
        self.frame.Bind(wx.EVT_BUTTON, self.OnBotonAceptar, self.botonAceptar)
        self.botonCancelar = xrc.XRCCTRL(self.frame, 'm_button2')
        self.frame.Bind(wx.EVT_BUTTON, self.salir, self.botonCancelar)
        self.panel = xrc.XRCCTRL(self.frame,'m_panel1')
        self.angle = pi
        self.subangle = (20*pi/180)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.frame.Show()
        return True
    def OnPaint(self, event):
        dc = wx.PaintDC(self.panel)
        size_x, size_y =  200, 200    #self.frame.GetClientSizeTuple()
        dc.SetDeviceOrigin(size_x/2, size_y/2)
        radius = hypot(size_x/4, size_y/4)
        x1 = radius*cos(self.angle)
        y1 = radius*sin(self.angle)
        x2 = (-radius/8)*cos(self.angle+self.subangle)
        y2 = (-radius/8)*sin(self.angle+self.subangle)
        x3 = (-radius/8)*cos(self.angle-self.subangle)
        y3 = (-radius/8)*sin(self.angle-self.subangle)
        dc.DrawCircle(0, 0, (radius+10))
        dc.DrawCircle(0, 0, (radius/10))
        dc.DrawPolygon(((x1,y1),(x2,y2),(x3,y3)))

        
    def OnBotonAceptar(self, event):
        wx.MessageBox('Bienvenido!')
        
    def salir(self, event):
        self.frame.Close()



if __name__ == '__main__':

    Bl = Blusb()
    Bl.MainLoop()
