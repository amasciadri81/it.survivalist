#!/usr/bin/python3
import wx


class KeyBoard(wx.Frame):
    def __init__(self, text='') : #, style = wx.SYSTEM_MENU):
        wx.Frame.__init__(self, None, pos=(25,110), size=(460, 240), title="keypad")

        self.char_case = '1'
        self.shift = False

        # graphic
        self.text_initial = text
        self.bn_size = (40, 40)
        self.color_default = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND)
        self.color_pushed  = 'LIGHT GREY'
        self.color_pushed  = 'yellow'

        # change with your TextCtrl
        self.input = wx.TextCtrl(self)

        # init ui
        self.characters()
        self.init_ui()

        print(self.GetSize())

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.input, 0, wx.EXPAND, 0)
        vbox.Add(self.keyboard_ui(self.keymap1, self.char_case), 0, wx.ALL, 5)
        self.SetSizer(vbox)

    def characters(self):

        # Matrix of keyboard
        self.keymap1 = [
                [ 'bn_1', 'bn_2', 'bn_3', 'bn_4', 'bn_5', 'bn_6', 'bn_7', 'bn_8', 'bn_9',   'bn_0'   , 'OK'    ],
                [ 'bn_q', 'bn_w', 'bn_e', 'bn_r', 'bn_t', 'bn_y', 'bn_u', 'bn_i', 'bn_o',   'bn_p'   , 'BS'    ],
                [ 'CL'  , 'bn_a', 'bn_s', 'bn_d', 'bn_f', 'bn_g', 'bn_h', 'bn_j', 'bn_k',   'bn_l'   , 'C'     ],
                [ 'SH'  , 'bn_z', 'bn_x', 'bn_c', 'bn_v', 'bn_b', 'bn_n', 'bn_m', 'bn_dot', 'bn_dash', 'Close' ]
        ]

        # buttons - 1: normal - 2: shift
        self.bn = {
                'bn_a': { '1': 'a', '2': 'A' },
                'bn_b': { '1': 'b', '2': 'B' },
                'bn_c': { '1': 'c', '2': 'C' },
                'bn_d': { '1': 'd', '2': 'D' },
                'bn_e': { '1': 'e', '2': 'E' },
                'bn_f': { '1': 'f', '2': 'F' },
                'bn_g': { '1': 'g', '2': 'G' },
                'bn_h': { '1': 'h', '2': 'H' },
                'bn_i': { '1': 'i', '2': 'I' },
                'bn_j': { '1': 'j', '2': 'J' },
                'bn_k': { '1': 'k', '2': 'K' },
                'bn_l': { '1': 'l', '2': 'L' },
                'bn_m': { '1': 'm', '2': 'M' },
                'bn_n': { '1': 'n', '2': 'N' },
                'bn_o': { '1': 'o', '2': 'O' },
                'bn_p': { '1': 'p', '2': 'P' },
                'bn_q': { '1': 'q', '2': 'Q' },
                'bn_r': { '1': 'r', '2': 'R' },
                'bn_s': { '1': 's', '2': 'S' },
                'bn_t': { '1': 't', '2': 'T' },
                'bn_u': { '1': 'u', '2': 'U' },
                'bn_v': { '1': 'v', '2': 'V' },
                'bn_w': { '1': 'w', '2': 'W' },
                'bn_x': { '1': 'x', '2': 'X' },
                'bn_y': { '1': 'y', '2': 'Y' },
                'bn_z': { '1': 'z', '2': 'Z' },

                'bn_0': { '1': '0', '2': '0' },
                'bn_1': { '1': '1', '2': '1' },
                'bn_2': { '1': '2', '2': '2' },
                'bn_3': { '1': '3', '2': '3' },
                'bn_4': { '1': '4', '2': '4' },
                'bn_5': { '1': '5', '2': '5' },
                'bn_6': { '1': '6', '2': '6' },
                'bn_7': { '1': '7', '2': '7' },
                'bn_8': { '1': '8', '2': '8' },
                'bn_9': { '1': '9', '2': '9' },
        
                'bn_dot':  { '1': '.', '2': ',' },
                'bn_dash': { '1': '-', '2': '_' },

                'SH': { '1': 'SH', '2': 'SH' },    # Shift
                'CL': { '1': 'CL', '2': 'CL' },    # Caps Locks
                'BS': { '1': '<',  '2': '<'  },    # Back Space
                'C':  { '1': 'C',  '2': 'C'  },    # Clear
                'OK': { '1': 'OK', '2': 'OK' },
                'Close': { '1': 'Close', '2': 'Close' },
                }

    def keyboard_ui(self, keymap, ccase):
        vbox = wx.BoxSizer(wx.VERTICAL)
        for row in keymap:
            hbox = wx.BoxSizer(wx.HORIZONTAL)
            for k in row:
                self.bn[k]['obj'] = wx.Button(self, label=self.bn[k][ccase], size=self.bn_size)
                hbox.Add( self.bn[k]['obj'] )
            vbox.Add(hbox)

        # Bind
        for k in self.bn.keys():
            if k[0:3] == 'bn_':
                self.bn[k]['obj'].Bind(wx.EVT_BUTTON, self.OnButton)

        self.bn['OK']['obj'].Bind(wx.EVT_BUTTON, self.OnOk)
        self.bn['Close']['obj'].Bind(wx.EVT_BUTTON, self.OnClose)
        self.bn['BS']['obj'].Bind(wx.EVT_BUTTON, self.OnBackSpace)
        self.bn['C']['obj'].Bind(wx.EVT_BUTTON, self.OnClear)
        self.bn['SH']['obj'].Bind(wx.EVT_BUTTON, self.OnShift)
        self.bn['CL']['obj'].Bind(wx.EVT_BUTTON, self.OnCapsLk)

        return vbox

    def OnButton(self, e):
        self.input.AppendText( e.GetEventObject().GetLabel() )
        if self.shift:
            self.shift = False
            self.change_layout('1')

    def OnShift(self, e):
        self.shift = True
        self.change_layout('2')

    def OnCapsLk(self, e):
        if self.char_case == '1':
            self.bn['CL']['obj'].SetBackgroundColour(self.color_pushed)
            self.char_case = '2'
            self.change_layout('2')
        else:
            self.bn['CL']['obj'].SetBackgroundColour(self.color_default)
            self.char_case = '1'
            self.change_layout('1')

    def OnBackSpace(self, e):
        self.input.SetValue(self.input.GetValue()[:-1])

    def OnClear(self, e):
        self.input.SetValue('')

    def OnOk(self, e):
        None
        # put here your function #
        #self.Close()

    def OnClose(self, e):
        self.Close()

    def change_layout(self, ccase):
        for i in self.bn:
            self.bn[i]['obj'].SetLabel(self.bn[i][ccase])


if __name__ == "__main__":
    app = wx.App()
    m = KeyBoard()
    m.Show()
    app.MainLoop()


