import win32gui


def getWindowByTitle(name: int):
    return win32gui.FindWindow(None, name)


def moveWindow(window, x: int, y: int):
    return win32gui.MoveWindow(window, 0, 0, x, y, True)


def moveWindowToForeground(window):
    win32gui.SetForegroundWindow(window)


def getWindowSize(window):
    rect = win32gui.GetWindowRect(window)
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    print("Window %s:" % win32gui.GetWindowText(window))
    print("\tLocation: (%d, %d)" % (x, y))
    print("\tSize: (%d, %d)" % (w, h))
    return [x, y, w, h]
