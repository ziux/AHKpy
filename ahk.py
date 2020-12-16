import subprocess
import time
import os
import json
from func import Mouse, Key
from event import Event
import threading
from queue import Queue


class AHK:
    process = None
    running = False
    hotkey_map = None
    mouse: Mouse = None
    key: Key = None
    input_file_name = 'input'
    output_file_name = 'output'
    input_file = None
    output_file = None
    events = None
    loop = None

    def __init__(self, frequency=0.2, io_file_path='./temp'):
        self.frequency = frequency
        self.mouse = Mouse(self)
        self.key = Key(self)
        self.hotkey_map = {}
        self.events = {}
        self.hotkey_queue = Queue()
        self.io_file_path = os.path.abspath(io_file_path)
        self.input_file_path = os.path.join(self.io_file_path, self.input_file_name)
        self.output_file_path = os.path.join(self.io_file_path, self.output_file_name)

    def start(self):
        self._make_hotkey_script()
        self.make_pipe_file()
        cwd = os.path.join(os.getcwd(), 'script', )
        script_path = os.path.join(cwd, 'AutoHotkeyU64.exe')
        self.process = subprocess.Popen(
            f"{script_path} main.ahk",
            cwd=cwd,
            env={"FrequencyTimeout": str(int(self.frequency * 1000)),
                 "IO_INPUT_FILE": self.input_file_path,
                 "IO_OUTPUT_FILE": self.output_file_path
                 })
        self.running = True
        self.loop = threading.Thread(target=self._listen)
        self.loop.start()

    def make_pipe_file(self):
        if not os.path.exists(self.io_file_path):
            os.mkdir(self.io_file_path)
        self.input_file = open(self.input_file_path, 'w+')
        with open(self.output_file_path, 'w+'):
            pass
        self.output_file = open(self.output_file_path, 'r')

    def add_hotkey(self, keys, func):
        if self.running:
            raise ValueError("请在start之前添加hotkey")
        self.hotkey_map[keys] = func

    def _make_hotkey_script(self):
        h = []
        for keys in self.hotkey_map:
            tmpl = f"{keys}::\n"
            tmpl += f'{{\nHotKeyIt("{keys}")\nreturn\n}}\n'
            h.append(tmpl)
        with open('./script/_hotkey.ahk', 'r') as f:
            data = f.read()
        with open('./script/hotkey.ahk', 'w+') as f:
            f.write(data)
            f.write('\n')
            f.write('\n'.join(h))

    def call_func(self, func_name, *args, results=False, timeout=10):
        e = None
        data = {'func': func_name, 'args': args, 'results': int(results), 'uuid': ''}
        if results:
            e = Event()
            self.events[e.uuid] = e
            data['uuid'] = e.uuid
        self.input_file.write(json.dumps(data))
        self.input_file.write('\n')
        self.input_file.flush()
        return e

    def read_data(self):
        results = self.output_file.readlines()
        if results:
            return results
        return None

    def _listen(self):
        while self.running:
            results = self.read_data()
            if results:
                for result in results:
                    if not result.strip():
                        continue
                    result = json.loads(result)
                    if result.get('uuid'):
                        uuid = result['uuid']
                        e = self.events.get(uuid)
                        if e:
                            e.set_result(result.get('results'))
                    elif result.get('keys'):
                        keys = result['keys']
                        self.hotkey_queue.put_nowait(keys)
                    else:
                        print(result)
            time.sleep(self.frequency)

    def listen_hotkey(self):
        try:
            while self.running:
                keys = self.hotkey_queue.get()
                self.hotkey_map[keys](self)
        except KeyboardInterrupt as e:
            self.close()

    def close(self):
        self.process.kill()
        self.input_file.close()
        self.output_file.close()


def a(ahk: AHK):
    print('aaa')
    # ahk.mouse.click((413, 613))
    r = ahk.key.get_key_state("a").result()
    print(r)


if __name__ == '__main__':
    ahk = AHK(0.2)
    ahk.add_hotkey('F1', a)
    ahk.start()
    ahk.listen_hotkey()
