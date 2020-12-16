class Mouse:
    def __init__(self, ahk):
        self.ahk = ahk

    def click(self, poi=None, mode=None):
        cmd = ''
        if poi is not None:
            x, y = poi
            cmd += f'{x},{y}'
        if mode is not None:
            cmd += f' {mode}'
        self.ahk.call_func("_MouseClick", cmd)

    def move(self, poi, speed=None, r=None):
        args = []

        x, y = poi
        args.append(x)
        args.append(y)
        args.append(speed)
        args.append(r)
        self.ahk.call_func("_MouseMove", *args)


class Key:
    def __init__(self, ahk):
        self.ahk = ahk

    def get_key_state(self, key, mode=None):
        args = [key]
        if mode:
            args.append(mode)
        state = self.ahk.call_func('GetKeyState', *args, results=True)

        return state

    def send(self, keys):
        cmd = f'{keys} '
        self.ahk.call_func('_KeySend', cmd)
