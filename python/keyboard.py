#!/usr/bin/python3
import wx
import time


class KeyBoard(wx.Frame):
    def __init__(self, text='') : #, style = wx.SYSTEM_MENU):
        wx.Frame.__init__(self, None, pos=(25,110), size=(430, 270), title="keypad")

        self.char_case = 'LO'
        self.shift = False
        self.symbols = False
        self.bn_downtime = 0
        self.bn_duration = 0

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
                [ 'bn_1', 'bn_2', 'bn_3', 'bn_4', 'bn_5', 'bn_6', 'bn_7', 'bn_8', 'bn_9',   'bn_0'   ],
                [ 'bn_q', 'bn_w', 'bn_e', 'bn_r', 'bn_t', 'bn_y', 'bn_u', 'bn_i', 'bn_o',   'bn_p'   ],
                [ '_SP' , 'bn_a', 'bn_s', 'bn_d', 'bn_f', 'bn_g', 'bn_h', 'bn_j', 'bn_k',   'bn_l'   ],
                [ 'CL'  , 'bn_z', 'bn_x', 'bn_c', 'bn_v', 'bn_b', 'bn_n', 'bn_m', 'BS' ],
                [ 'SH'  , 'SYM', 'Space', 'Close', 'OK']
        ]

        """
        LO : normal char
        SH : shift button pressed 
        SYM: symbols button pressed 
        """
        self.bn = {
                'bn_a': { 'LO': 'a', 'SH': 'A', 'SYM': '@' },
                'bn_b': { 'LO': 'b', 'SH': 'B', 'SYM': '.' },
                'bn_c': { 'LO': 'c', 'SH': 'C', 'SYM': '.' },
                'bn_d': { 'LO': 'd', 'SH': 'D', 'SYM': '.' },
                'bn_e': { 'LO': 'e', 'SH': 'E', 'SYM': '[' },
                'bn_f': { 'LO': 'f', 'SH': 'F', 'SYM': '.' },
                'bn_g': { 'LO': 'g', 'SH': 'G', 'SYM': '.' },
                'bn_h': { 'LO': 'h', 'SH': 'H', 'SYM': '.' },
                'bn_i': { 'LO': 'i', 'SH': 'I', 'SYM': '>' },
                'bn_j': { 'LO': 'j', 'SH': 'J', 'SYM': '.' },
                'bn_k': { 'LO': 'k', 'SH': 'K', 'SYM': '.' },
                'bn_l': { 'LO': 'l', 'SH': 'L', 'SYM': '.' },
                'bn_m': { 'LO': 'm', 'SH': 'M', 'SYM': '.' },
                'bn_n': { 'LO': 'n', 'SH': 'N', 'SYM': '.' },
                'bn_o': { 'LO': 'o', 'SH': 'O', 'SYM': '_' },
                'bn_p': { 'LO': 'p', 'SH': 'P', 'SYM': '-' },
                'bn_q': { 'LO': 'q', 'SH': 'Q', 'SYM': '\\'},
                'bn_r': { 'LO': 'r', 'SH': 'R', 'SYM': ']' },
                'bn_s': { 'LO': 's', 'SH': 'S', 'SYM': '#' },
                'bn_t': { 'LO': 't', 'SH': 'T', 'SYM': '{' },
                'bn_u': { 'LO': 'u', 'SH': 'U', 'SYM': '<' },
                'bn_v': { 'LO': 'v', 'SH': 'V', 'SYM': '.' },
                'bn_w': { 'LO': 'w', 'SH': 'W', 'SYM': '|' },
                'bn_x': { 'LO': 'x', 'SH': 'X', 'SYM': '.' },
                'bn_y': { 'LO': 'y', 'SH': 'Y', 'SYM': '}' },
                'bn_z': { 'LO': 'z', 'SH': 'Z', 'SYM': '.' },

                'bn_0': { 'LO': '0', 'SH': '0', 'SYM': '=' },
                'bn_1': { 'LO': '1', 'SH': '1', 'SYM': '!' },
                'bn_2': { 'LO': '2', 'SH': '2', 'SYM': '"' },
                'bn_3': { 'LO': '3', 'SH': '3', 'SYM': ''  },
                'bn_4': { 'LO': '4', 'SH': '4', 'SYM': '$' },
                'bn_5': { 'LO': '5', 'SH': '5', 'SYM': '%' },
                'bn_6': { 'LO': '6', 'SH': '6', 'SYM': '&' },
                'bn_7': { 'LO': '7', 'SH': '7', 'SYM': '/' },
                'bn_8': { 'LO': '8', 'SH': '8', 'SYM': '(' },
                'bn_9': { 'LO': '9', 'SH': '9', 'SYM': ')' },
        
                'SYM':   { 'LO': '=\<',     'SH': '=\<',    'SYM': 'abc'    },    # SYMBOLS
                'CL':    { 'LO': 'CapsLk',  'SH': 'CapsLk', 'SYM': 'CapsLk' },    # Caps Locks
                'SH':    { 'LO': 'Shift',   'SH': 'Shift',  'SYM': 'Shift'  },    # Shift
                'BS':    { 'LO': '<--',     'SH': '<--',    'SYM': '<--'    },    # Back Space
                'Space': { 'LO': '',        'SH': '',       'SYM': ''       },    # bar space
                'OK':    { 'LO': 'Enter',   'SH': 'Enter',  'SYM': 'Enter'  },
                'Close': { 'LO': 'Close',   'SH': 'Close',  'SYM': 'Close'  }
                #'C':     { 'LO': 'C',       'SH': 'C',      'SH': 'C'       },    # Clear
                }

    def keyboard_ui(self, keymap, ccase):
        vbox = wx.BoxSizer(wx.VERTICAL)
        for row in keymap:
            hbox = wx.BoxSizer(wx.HORIZONTAL)

            for k in row:

                # spacer
                if k == '_SP':
                    hbox.AddSpacer(self.bn_size[0] * 0.5)
                else:
                    # set bn size
                    if k == 'Space':
                        bn_size = (self.bn_size[0] * 4, self.bn_size[1])
                    elif k in ('CL', 'BS', 'SH', 'SYM', 'OK', 'Close'):
                        bn_size = (self.bn_size[0] * 1.5, self.bn_size[1])
                    else:
                        bn_size = self.bn_size

                    # create bn
                    self.bn[k]['obj'] = wx.Button(self, label=self.bn[k][ccase], size=bn_size)
                    hbox.Add( self.bn[k]['obj'] )

            vbox.Add(hbox)

        # Bind buttons
        for k in self.bn.keys():
            if k[0:3] == 'bn_':
                print(k)
                self.bn[k]['obj'].Bind(wx.EVT_BUTTON, self.OnButton)

        # if keep pressed BackSlash, clear input
        self.bn['BS']['obj'].Bind(wx.EVT_LEFT_DOWN, self.OnBackSpaceDown)
        self.bn['BS']['obj'].Bind(wx.EVT_LEFT_UP, self.OnBackSpaceUp)
        self.bn['BS']['obj'].Bind(wx.EVT_BUTTON, self.OnBackSpace)

        self.bn['OK']['obj'].Bind(wx.EVT_BUTTON, self.OnOk)
        self.bn['Close']['obj'].Bind(wx.EVT_BUTTON, self.OnClose)
        self.bn['SH']['obj'].Bind(wx.EVT_BUTTON, self.OnShift)
        self.bn['CL']['obj'].Bind(wx.EVT_BUTTON, self.OnCapsLk)
        self.bn['SYM']['obj'].Bind(wx.EVT_BUTTON, self.OnSymbols)
        #self.bn['C']['obj'].Bind(wx.EVT_BUTTON, self.OnClear)

        return vbox

    def OnButton(self, e):
        self.input.AppendText( e.GetEventObject().GetLabel() )
        if self.shift:
            self.shift = False
            self.change_layout('LO')

    def OnShift(self, e):
        print(e.GetTimestamp())
        self.shift = True
        self.change_layout('SH')

    def OnCapsLk(self, e):
        if self.char_case == 'LO':
            self.change_layout('CL')
        else:
            self.change_layout('LO')

    def OnSymbols(self, e):
        if self.symbols:
            self.change_layout('LO')
        else:
            self.change_layout('SYM')

    def OnBackSpaceDown(self, e):
        self.bn_downtime = time.time()
        e.Skip()

    def OnBackSpaceUp(self, e):
        bn_uptime = time.time()
        self.bn_duration = bn_uptime - self.bn_downtime 
        self.bn_downtime = 0
        e.Skip()

    def OnBackSpace(self, e):
        if self.bn_duration < 0.6:
            self.input.SetValue(self.input.GetValue()[:-1])
        else:
            self.input.SetValue('')

    def OnClear(self, e):
        self.input.SetValue('')

    def OnOk(self, e):
        None
        # put here your function #
        #self.Close()

    def OnClose(self, e):
        self.Close()

    def change_layout(self, ccase):
        if ccase == 'LO':
            self.char_case = 'LO'
            self.bn['CL']['obj'].SetBackgroundColour(self.color_default)
            self.symbols = False
            self.bn['SYM']['obj'].SetBackgroundColour(self.color_default)

        elif ccase == 'SH':
            self.symbols = False
            self.bn['SYM']['obj'].SetBackgroundColour(self.color_default)

        elif ccase == 'CL':
            ccase = 'SH'
            self.char_case = 'SH'
            self.bn['CL']['obj'].SetBackgroundColour(self.color_pushed)
            self.symbols = False
            self.bn['SYM']['obj'].SetBackgroundColour(self.color_default)

        elif ccase == 'SYM':
            self.char_case = 'LO'
            self.bn['CL']['obj'].SetBackgroundColour(self.color_default)
            self.symbols = True
            self.bn['SYM']['obj'].SetBackgroundColour(self.color_pushed)

        for i in self.bn:
            self.bn[i]['obj'].SetLabel(self.bn[i][ccase])


if __name__ == "__main__":
    app = wx.App()
    m = KeyBoard()
    m.Show()
    app.MainLoop()


    def change_layout(self, ccase):
        for i in self.bn:
            self.bn[i]['obj'].SetLabel(self.bn[i][ccase])


if __name__ == "__main__":
    app = wx.App()
    m = KeyBoard()
    m.Show()
    app.MainLoop()


