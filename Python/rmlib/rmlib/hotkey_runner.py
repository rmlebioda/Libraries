from dataclasses import dataclass
from typing import Callable, List
from pynput import keyboard

@dataclass
class Combination:
    list_of_trigger_keys: List[set[keyboard.KeyCode]]
    callback: Callable[[], None]

class HotkeyRunner:
    __currently_pressed_keys = set()
    __combinations: List[Combination] = []

    def __init__(self):
        pass

    def add_hotkey(self, keys: List[set[keyboard.KeyCode]], callback: Callable[[], None]):
        self.__add_hotkey(Combination(list_of_trigger_keys=keys, callback=callback))

    def __add_hotkey(self, combination: Combination):
        self.__combinations.append(combination)

    def listen(self):
        def on_press(key):
            if key not in self.__currently_pressed_keys:
                self.__currently_pressed_keys.add(key)
            for combination in [combination for combination in self.__combinations]:
                if any([self.__currently_pressed_keys == trigger_keys for trigger_keys in combination.list_of_trigger_keys]):
                    combination.callback()

        def on_release(key):
            if key in self.__currently_pressed_keys:
                self.__currently_pressed_keys.remove(key)

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
