import subprocess
import time
import os
import json
from func import Mouse

input_file = './script/input'
output_file = './script/output'
hotkey_output_file = './script/output_hotkey'


class AHK:
    process = None
    running = False
    hotkey_map = {}
    mouse: Mouse = None

    def __init__(self, frequency=0.4):
        self.frequency = frequency
        self.mouse = Mouse(self)

    def start(self):
        self._make_hotkey_script()
        self.make_pipe_file()
        cwd = os.path.join(os.getcwd(), 'script', )
        script_path = os.path.join(cwd, 'AutoHotkeyU64.exe')
        self.process = subprocess.Popen(
            f"{script_path} main.ahk",
            cwd=cwd,
            env={"FrequencyTimeout": str(int(self.frequency * 1000))})
        self.running = True

    def make_pipe_file(self):
        with open(input_file, 'w+'):
            pass
        with open(output_file, 'w+'):
            pass
        with open(hotkey_output_file, 'w+'):
            pass

    def add_hotkey(self, keys, func):
        if self.running:
            raise ValueError("请在start之前添加hotkey")
        self.hotkey_map[keys] = func

    def _make_hotkey_script(self):
        h = []
        for keys in self.hotkey_map:
            tmpl = f"{keys}::\n"
            tmpl += f'{{HotKeyIt("{keys}")\nreturn\n}}\n'
            h.append(tmpl)
        with open('./script/_hotkey.ahk', 'r') as f:
            data = f.read()
        with open('./script/hotkey.ahk', 'w+') as f:
            f.write(data)
            f.write('\n')
            f.write('\n'.join(h))

    def call_func(self, func_name, *args, results=False, timeout=10):
        data = {'func': func_name, 'args': args, 'results': int(results)}
        with open(input_file, 'w+') as f:
            f.write(json.dumps(data))
        if results:
            while timeout:
                data = self.read_data(output_file)
                if data:
                    data = json.loads(data)
                    return data['results']
                timeout -= self.frequency
                time.sleep(self.frequency)
            raise ValueError('timeout')

    def read_data(self, file):
        if os.path.getsize(file):
            with open(hotkey_output_file, 'a+') as f:
                f.seek(0, 0)
                data = f.read()
                f.seek(0, 0)
                f.truncate()
                return data
        return None

    def listen_hotkey(self):
        while self.running:
            data = self.read_data(hotkey_output_file)
            if data:
                data = json.loads(data)
                keys = data['keys']
                self.hotkey_map[keys](self)
            time.sleep(self.frequency)

    def close(self):
        self.process.kill()


def a(ahk: AHK):
    ahk.mouse.click((413, 413), 'right')


if __name__ == '__main__':
    ahk = AHK(1)
    ahk.add_hotkey('F1', a)
    ahk.start()

    ahk.listen_hotkey()
