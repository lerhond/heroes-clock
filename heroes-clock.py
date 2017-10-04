import keyboard
import time


hotkey = 'F2'


config = {
    'Infernal Shrines': {
        # 'before_game_text': 'Press {hotkey} when the gates open.',
        'first_spawn_time': 115,
        'next_spawn_time': 115,
        'timer_text': 'The Shrine will spawn in',
        'during_objective_text': 'The Shrine has spawned.',
        'hotkey_prompt': 'Press {hotkey} when the Punisher dies.'
    }
}

battleground = None
current_state = None
last_time = None


def key_pressed():
    pass


if __name__ == '__main__':
    battleground = 'Infernal Shrines'
    bg_config = config[battleground]
    print('Press {hotkey} when the gates open.'.format(hotkey=hotkey))
    keyboard.wait(hotkey)
    last_time = time.time()
    current_state = 'first_countdown'
    keyboard.add_hotkey(hotkey, key_pressed)
    while True:
        time.sleep(1)
