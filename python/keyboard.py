#!/usr/bin/python3
import wx


class KeyBoard(wx.Frame):
    def __init__(self, text='') : #, style = wx.SYSTEM_MENU):
        wx.Frame.__init__(self, None, pos=(25,110), title="keypad")

        self.char_case = '1'
        self.shift = False
        self.text_initial = text
        self.bn_size = (40, 40)
        self.color_default = wx.SystemSettings.GetColour(wx.SYS_COLOUR_BACKGROUND)
        self.color_pushed  = 'yellow'

        # change with your TextCtrl
        self.input = wx.TextCtrl(self)

        self.characters()
        self.init_ui()

    def characters(self):
        self.line1 = [ 'bn_1', 'bn_2', 'bn_3', 'bn_4', 'bn_5', 'bn_6', 'bn_7', 'bn_8', 'bn_9',   'bn_0'   , 'OK'   ]
        self.line2 = [ 'bn_q', 'bn_w', 'bn_e', 'bn_r', 'bn_t', 'bn_y', 'bn_u', 'bn_i', 'bn_o',   'bn_p'   , 'BS'   ]
        self.line3 = [ 'CL'  , 'bn_a', 'bn_s', 'bn_d', 'bn_f', 'bn_g', 'bn_h', 'bn_j', 'bn_k',   'bn_l'   , 'C'     ]
        self.line4 = [ 'SH'  , 'bn_z', 'bn_x', 'bn_c', 'bn_v', 'bn_b', 'bn_n', 'bn_m', 'bn_dot', 'bn_dash', 'close' ]

        self.bn_letters = {
                'bn_a': { '1': 'a', '2': 'A'},
                'bn_b': { '1': 'b', '2': 'B'},
                'bn_c': { '1': 'c', '2': 'C'},
                'bn_d': { '1': 'd', '2': 'D'},
                'bn_e': { '1': 'e', '2': 'E'},
                'bn_f': { '1': 'f', '2': 'F'},
                'bn_g': { '1': 'g', '2': 'G'},
                'bn_h': { '1': 'h', '2': 'H'},
                'bn_i': { '1': 'i', '2': 'I'},
                'bn_j': { '1': 'j', '2': 'J'},
                'bn_k': { '1': 'k', '2': 'K'},
                'bn_l': { '1': 'l', '2': 'L'},
                'bn_m': { '1': 'm', '2': 'M'},
                'bn_n': { '1': 'n', '2': 'N'},
                'bn_o': { '1': 'o', '2': 'O'},
                'bn_p': { '1': 'p', '2': 'P'},
                'bn_q': { '1': 'q', '2': 'Q'},
                'bn_r': { '1': 'r', '2': 'R'},
                'bn_s': { '1': 's', '2': 'S'},
                'bn_t': { '1': 't', '2': 'T'},
                'bn_u': { '1': 'u', '2': 'U'},
                'bn_v': { '1': 'v', '2': 'V'},
                'bn_w': { '1': 'w', '2': 'W'},
                'bn_x': { '1': 'x', '2': 'X'},
                'bn_y': { '1': 'y', '2': 'Y'},
                'bn_z': { '1': 'z', '2': 'Z'},
                'bn_dot':  { '1': '.', '2': ','},
                'bn_dash': { '1': '-', '2': '_'}
                }

        self.bn_numbers = {
                'bn_0': { '1': '0', '2': '0'},
                'bn_1': { '1': '1', '2': '1'},
                'bn_2': { '1': '2', '2': '2'},
                'bn_3': { '1': '3', '2': '3'},
                'bn_4': { '1': '4', '2': '4'},
                'bn_5': { '1': '5', '2': '5'},
                'bn_6': { '1': '6', '2': '6'},
                'bn_7': { '1': '7', '2': '7'},
                'bn_8': { '1': '8', '2': '8'},
                'bn_9': { '1': '9', '2': '9'}
                }
        
        self.bn_sc = {
                'CL': { '1': 'CL'},
                'SH': { '1': 'SH'},
                'OK': { '1': 'OK'},
                'C':  { '1': 'C'},
                'BS': { '1': '<'},
                'Close': { '1': 'Close'},
                }

    def init_ui(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.input, 0, wx.EXPAND, 0)
        vbox.Add(self.keyboard_ui(self.char_case), 0, wx.ALL, 5)

        self.SetSizer(vbox)

    def keyboard_ui(self, ccase):
        vbox = wx.BoxSizer(wx.VERTICAL)

        # LINE 1
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        for i in 'bn_1', 'bn_2', 'bn_3', 'bn_4', 'bn_5', 'bn_6', 'bn_7', 'bn_8', 'bn_9', 'bn_0':
            self.bn_numbers[i]['obj'] = wx.Button(self, label=self.bn_numbers[i][ccase], size=self.bn_size)
            box1.Add( self.bn_numbers[i]['obj'] )
        self.bn_sc['OK']['obj'] = wx.Button(self, label=self.bn_sc['OK'][ccase], size=self.bn_size)
        box1.Add( self.bn_sc['OK']['obj'] )

        # LINE 2
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        for i in 'bn_q', 'bn_w', 'bn_e', 'bn_r', 'bn_t', 'bn_y', 'bn_u', 'bn_i', 'bn_o', 'bn_p':
            self.bn_letters[i]['obj'] = wx.Button(self, label=self.bn_letters[i][ccase], size=self.bn_size)
            box2.Add( self.bn_letters[i]['obj'] )
        self.bn_sc['BS']['obj'] = wx.Button(self, label=self.bn_sc['BS'][ccase], size=self.bn_size)
        box2.Add( self.bn_sc['BS']['obj'] )

        # LINE 3
        box3 = wx.BoxSizer(wx.HORIZONTAL)
        self.bn_sc['CL']['obj'] = wx.Button(self, label=self.bn_sc['CL'][ccase], size=self.bn_size)
        box3.Add( self.bn_sc['CL']['obj'] )
        for i in 'bn_a','bn_s','bn_d','bn_f','bn_g','bn_h','bn_j','bn_k','bn_l':
            self.bn_letters[i]['obj'] = wx.Button(self, label=self.bn_letters[i][ccase], size=self.bn_size)
            box3.Add( self.bn_letters[i]['obj'] )
        self.bn_sc['C']['obj'] = wx.Button(self, label=self.bn_sc['C'][ccase], size=self.bn_size)
        box3.Add( self.bn_sc['C']['obj'] )

        # LINE 4
        box4 = wx.BoxSizer(wx.HORIZONTAL)
        self.bn_sc['SH']['obj'] = wx.Button(self, label=self.bn_sc['SH'][ccase], size=self.bn_size)
        box4.Add( self.bn_sc['SH']['obj'] )
        for i in 'bn_z','bn_x','bn_c','bn_v','bn_b','bn_n','bn_m':
            self.bn_letters[i]['obj'] = wx.Button(self, label=self.bn_letters[i][ccase], size=self.bn_size)
            box4.Add( self.bn_letters[i]['obj'] )
        self.bn_letters['bn_dot']['obj'] = wx.Button(self, label=self.bn_letters['bn_dot'][ccase], size=self.bn_size)
        box4.Add( self.bn_letters['bn_dot']['obj'] )
        self.bn_letters['bn_dash']['obj'] = wx.Button(self, label=self.bn_letters['bn_dash'][ccase], size=self.bn_size)
        box4.Add( self.bn_letters['bn_dash']['obj'] )
        self.bn_sc['Close']['obj'] = wx.Button(self, label=self.bn_sc['Close'][ccase], size=self.bn_size)
        box4.Add( self.bn_sc['Close']['obj'] )

        # Bind
        for k in self.bn_numbers.keys():
            self.bn_numbers[k]['obj'].Bind(wx.EVT_BUTTON, self.OnButton)

        for k in self.bn_letters.keys():
            self.bn_letters[k]['obj'].Bind(wx.EVT_BUTTON, self.OnButton)
        
        self.bn_sc['OK']['obj'].Bind(wx.EVT_BUTTON, self.OnOk)
        self.bn_sc['Close']['obj'].Bind(wx.EVT_BUTTON, self.OnClose)
        self.bn_sc['BS']['obj'].Bind(wx.EVT_BUTTON, self.OnBackSpace)
        self.bn_sc['C']['obj'].Bind(wx.EVT_BUTTON, self.OnClear)
        self.bn_sc['CL']['obj'].Bind(wx.EVT_BUTTON, self.OnCapsLk)
        self.bn_sc['SH']['obj'].Bind(wx.EVT_BUTTON, self.OnShift)

        vbox.Add(box1)
        vbox.Add(box2)
        vbox.Add(box3)
        vbox.Add(box4)

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
            self.bn_sc['CL']['obj'].SetBackgroundColour(self.color_pushed)
            self.char_case = '2'
            self.change_layout('2')
        else:
            self.bn_sc['CL']['obj'].SetBackgroundColour(self.color_default)
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
        for i in self.bn_letters:
            self.bn_letters[i]['obj'].SetLabel(self.bn_letters[i][ccase])

        for i in self.bn_numbers:
            self.bn_numbers[i]['obj'].SetLabel(self.bn_numbers[i][ccase])


if __name__ == "__main__":
    app = wx.App()
    m = KeyBoard()
    m.Show()
    app.MainLoop()


