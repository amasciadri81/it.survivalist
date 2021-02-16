#!/usr/bin/python3
import wx


class KeyPad(wx.Frame):
    def __init__(self) : #, style = wx.SYSTEM_MENU):
        wx.Frame.__init__(self, None, title="keypad")
        self.bn_size = (40, 40)

        self.input = wx.TextCtrl(self)
        self.init_ui()

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.input, 0, wx.EXPAND, 0)
        vbox.Add(self.keypad_ui(), 0, wx.ALL, 5)

        self.SetSizer(vbox)
        self.Fit()

    def keypad_ui(self):
        sizer = wx.GridSizer(4, 4, 10, 5)
        self.buttons = {
                # 1st line
                'bn1' : { 'id': 1001, 'label': '1' },
                'bn2' : { 'id': 1002, 'label': '2' },
                'bn3' : { 'id': 1003, 'label': '3' },
                'bnO' : { 'id': 1012, 'label': 'OK' },
                # 2nd line
                'bn4' : { 'id': 1004, 'label': '4' },
                'bn5' : { 'id': 1005, 'label': '5' },
                'bn6' : { 'id': 1006, 'label': '6' },
                'bnB' : { 'id': 1014, 'label': '<' },
                # 3th line
                'bn7' : { 'id': 1007, 'label': '7' },
                'bn8' : { 'id': 1008, 'label': '8' },
                'bn9' : { 'id': 1009, 'label': '9' },
                'bnC' : { 'id': 1015, 'label': 'C' },
                # 4th line
                'bnE' : { 'id': 1016, 'label': '' },
                'bn0' : { 'id': 1000, 'label': '0' },
                'bnP' : { 'id': 1011, 'label': '.' },
                'bnX' : { 'id': 1013, 'label': 'Close' },
                }

        # create buttons
        for k in self.buttons.keys():
            bn = self.buttons[k]
            bn['obj'] = wx.Button(self, id=bn['id'], label=bn['label'], size=self.bn_size)

            # add to sizer and bind
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
            None
            # put here your function #
            #self.Close()
        # Close
        elif i == 1013:
            self.Close()
        # < [remove last char]
        elif i == 1014:
            self.input.SetValue(self.input.GetValue()[:-1])
        # C [clear]
        elif i == 1015:
            self.input.SetValue('')
        # Empty
        #elif i == 1016:
        #    print(self.input.GetValue()[:-1])
        #    print(e.GetEventObject().GetLabel())


if __name__ == "__main__":
    app = wx.App()
    m = KeyPad()
    m.Show()
    app.MainLoop()


