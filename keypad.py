#!/usr/bin/python3
import wx


class KeyPad(wx.Frame):
    def __init__(self) : #, style = wx.SYSTEM_MENU):
        wx.Frame.__init__(self, None, title="keypad")
        self.bn_size = (40, 40)
        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.input_ui(), 0, wx.EXPAND, 0)
        vbox.Add(self.keypad_ui(), 0, wx.ALL, 5)

        self.SetSizer(vbox)
        self.Fit()

    def input_ui(self):
        self.input = wx.TextCtrl(self)
        return self.input

    def keypad_ui(self):
        sizer = wx.GridSizer(4, 4, 10, 5)
        self.buttons = {
                'bn1' : { 'id': 1001, 'label': '1' },
                'bn2' : { 'id': 1002, 'label': '2' },
                'bn3' : { 'id': 1003, 'label': '3' },
                'bnO' : { 'id': 1012, 'label': 'OK' },
                'bn4' : { 'id': 1004, 'label': '4' },
                'bn5' : { 'id': 1005, 'label': '5' },
                'bn6' : { 'id': 1006, 'label': '6' },
                'bnB' : { 'id': 1014, 'label': '<x' },
                'bn7' : { 'id': 1007, 'label': '7' },
                'bn8' : { 'id': 1008, 'label': '8' },
                'bn9' : { 'id': 1009, 'label': '9' },
                'bnC' : { 'id': 1015, 'label': 'C' },
                'bnE' : { 'id': 1016, 'label': '' },
                'bn0' : { 'id': 1000, 'label': '0' },
                'bnP' : { 'id': 1011, 'label': '.' },
                'bnX' : { 'id': 1013, 'label': 'Close' },
                }

        for k in self.buttons.keys():
            bn = self.buttons[k]
            bn['obj'] = wx.Button(self, id=bn['id'], label=bn['label'], size=self.bn_size)

            sizer.Add(bn['obj'])
            bn['obj'].Bind(wx.EVT_BUTTON, self.OnButton)

        return sizer

    def OnButton(self, e):
        i=e.GetId()

        # Numbers
        if 1000 <= i <= 1011:
            self.input.AppendText( e.GetEventObject().GetLabel() )

        # OK
        elif i == 1012:
            # OK
            #self.Close()
            None

        # Close
        elif i == 1013:
            self.Close()

        # <x
        elif i == 1014:
            self.input.SetValue(self.input.GetValue()[:-1])

        # C
        elif i == 1015:
            self.input.SetValue('')

        # empty
        #elif i == 1016:
        #    print(self.input.GetValue()[:-1])
        #    print(e.GetEventObject().GetLabel())


if __name__ == "__main__":
    app = wx.App()
    m = KeyPad()
    m.Show()
    app.MainLoop()


