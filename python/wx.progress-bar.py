#!/usr/bin/python3
import wx, threading, time

class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, size=(350,200))
        self.progress_increase = 5
        self.progress_interval = 0.5
        self.init()

    def init(self):
        msg = wx.MessageBox('Do you want to see the progress bar?', '', wx.YES_NO | wx.ICON_QUESTION)
        if msg == 2:
            self.progress_bar(self.my_function, (10,))  # <name of function without ()>, <tuple with args of function>
        self.Close()

    def my_function(self, t):
        time.sleep(t)

    def progress_bar(self, target, args):
        t=threading.Thread(target=target, args=args)
        t.start()
        count = 0
        dlg = wx.ProgressDialog('', 'Applying...')
        while t.is_alive():
            dlg.Update(count)
            time.sleep(self.progress_interval)
            count += self.progress_increase
        del dlg
        t.join()
        wx.MessageBox('Done', '', wx.OK)


if __name__ == "__main__":
    app = wx.App()
    top = Frame()
    top.Show()
    app.MainLoop()
