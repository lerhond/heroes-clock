import keyboard
import time


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

battleground = None
current_state = None
count_until = None


def key_pressed(bg_config):
    global count_until
    count_until = time.time() + bg_config['next_spawn_time']


def format_time(t):
    return '{m:.0f}:{s:02.0f}'.format(m=t//60, s=t%60)


if __name__ == '__main__':
    battleground = 'Infernal Shrines'
    bg_config = config[battleground]
    print('Press {hotkey} when the gates open.'.format(hotkey=hotkey))
    keyboard.wait(hotkey)
    count_until = time.time() + bg_config['first_spawn_time']
    keyboard.add_hotkey(hotkey, key_pressed, args=(bg_config,))
    while True:
        time_left = count_until - time.time()
        if time_left > 0:
            print('{timer_text} {time}'.format(
                timer_text=bg_config['timer_text'],
                time=format_time(time_left)))
        else:
            print(bg_config['during_objective_text'])
            print(bg_config['hotkey_prompt'].format(hotkey=hotkey))
        time.sleep(1)
