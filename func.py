

class Mouse:
    def __init__(self, ahk):
        self.ahk = ahk

    def click(self, poi=None, mode=None):
        cmds = ''
        if poi is not None:
            x, y = poi
            cmds += f'{x},{y}'
        if mode is not None:
            cmds += f' {mode}'
        self.ahk.call_func("_MouseClick", cmds)

    def move(self, poi, speed=None, r=None):
        args = []

        x, y = poi
        args.append(x)
        args.append(y)
        args.append(speed)
        args.append(r)
        self.ahk.call_func("_MouseMove", *args)
