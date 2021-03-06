import keyboard
import time
import wx

from wx import xrc


hotkey = 'F2'


config = {
    'before_game_text': 'Press {hotkey} when the gates open (at 0:00 game time).',
    'Infernal Shrines': {
        'first_spawn_time': 5,
        'next_spawn_time': 10,
        'timer_text': 'The Shrine will spawn in',
        'during_objective_text': 'The Shrine has spawned.',
        'hotkey_prompt': 'Press {hotkey} when the Punisher dies.'
    }
}


def format_time(t):
    return '{m:.0f}:{s:02.0f}'.format(m=t // 60, s=t % 60)


class ClockApplication(wx.App):
    count_until = None
    bg_config = None

    # noinspection PyAttributeOutsideInit
    def OnInit(self):
        self.bg_config = config['Infernal Shrines']
        self.res = xrc.XmlResource('window.xrc')
        self.frame = self.res.LoadFrame(None, 'main_frame')
        self.above_timer_label = xrc.XRCCTRL(self.frame, 'above_timer_label')
        self.timer_label = xrc.XRCCTRL(self.frame, 'timer_label')
        self.prompt_label = xrc.XRCCTRL(self.frame, 'prompt_label')
        self.update_timer()
        self.timer = wx.Timer(self, -1)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self.update_timer)
        keyboard.add_hotkey(hotkey, self.handle_hotkey)
        self.frame.Show()
        return True

    def update_timer(self, event=None):
        time_left = (self.count_until - time.time()
                     if self.count_until is not None else None)
        if time_left is None:
            self.above_timer_label.Show(False)
            self.timer_label.Show(False)
            self.prompt_label.SetLabel(config['before_game_text'].format(hotkey=hotkey))
            self.prompt_label.Show(True)
        elif time_left > 0:
            self.above_timer_label.SetLabel(self.bg_config['timer_text'])
            self.above_timer_label.Show(True)
            self.timer_label.SetLabel(format_time(time_left))
            self.timer_label.Show(True)
            self.prompt_label.SetLabel(self.bg_config['hotkey_prompt'].format(hotkey=hotkey))
            self.prompt_label.Show(True)
        else:
            self.above_timer_label.SetLabel(self.bg_config['during_objective_text'])
            self.above_timer_label.Show(True)
            self.timer_label.Show(False)
            self.prompt_label.SetLabel(self.bg_config['hotkey_prompt'].format(hotkey=hotkey))
            self.prompt_label.Show(True)
        self.above_timer_label.Parent.Sizer.Layout()

    def handle_hotkey(self):
        self.count_until = time.time() + self.bg_config[
            'first_spawn_time' if self.count_until is None
            else 'next_spawn_time']
        self.update_timer()


if __name__ == '__main__':
    app = ClockApplication()
    app.MainLoop()
