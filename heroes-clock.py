import keyboard
import time
import wx


hotkey = 'F2'


config = {
    'before_game_text': 'Press {hotkey} when the gates open (at 0:00 game time).',
    'Infernal Shrines': {
        'first_spawn_time': 115,
        'next_spawn_time': 115,
        'timer_text': 'The Shrine will spawn in',
        'during_objective_text': 'The Shrine has spawned.',
        'hotkey_prompt': 'Press {hotkey} when the Punisher dies.'
    }
}


def format_time(t):
    return '{m:.0f}:{s:02.0f}'.format(m=t//60, s=t%60)


class MainFrame(wx.Frame):
    count_until = None
    bg_config = None


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        panel = wx.Panel(self)
        self.bg_config = config['Infernal Shrines']
        self.timer_label = wx.StaticText(panel, label='Initializing...')
        self.update_timer(None)
        self.Show(True)
        self.timer = wx.Timer(self, -1)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self.update_timer)
        self_frame = self
        keyboard.add_hotkey(hotkey, self.handle_hotkey)


    def update_timer(self, event):
        time_left = (self.count_until - time.time()
            if self.count_until is not None else None)
        if time_left is None:
            self.timer_label.SetLabel(config['before_game_text'].format(hotkey=hotkey))
        elif time_left < 0:
            self.timer_label.SetLabel(self.bg_config['during_objective_text'])
        else:
            self.timer_label.SetLabel('{timer_text} {time}'.format(
                timer_text=self.bg_config['timer_text'],
                time=format_time(time_left)))


    def handle_hotkey(self):
        self.count_until = time.time() + self.bg_config[
            'first_spawn_time' if self.count_until is None
            else 'next_spawn_time']
        self.update_timer(None)


if __name__ == '__main__':
    app = wx.App(False)
    frame = MainFrame(None, wx.ID_ANY, 'Heroes Clock')
    app.MainLoop()
