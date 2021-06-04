import asyncio
import argparse
import sys
import time
from datetime import datetime
from os import path
from enum import Enum
from PIL import Image
from ctypes import windll
import win32gui
import win32ui
import win32api
import win32con
import winerror

from classes.bot import Bot

class Notifier:
    """ Notify user when boss waves occur in Mindustry """

    CHECK_STATE_INTERVAL = 0.5
    CHECK_MESSAGE_INTERVAL = 0.1
    MIN_BOSS_INTERVAL = 120

    def __init__(self,currentBot:Bot):
        self.windows_notifier = WindowsNotifier(currentBot)
        self.prev_state = None
        self.status_time = 0
        # Always send notification for first boss wave, even if it happens immediately after starting game
        self.active_time_without_boss = Notifier.MIN_BOSS_INTERVAL
        print("Notifier started.")

    async def monitor(self):
        while self.windows_notifier.alive:
            await self.message_aware_sleep(Notifier.CHECK_STATE_INTERVAL, Notifier.CHECK_MESSAGE_INTERVAL)

    @staticmethod
    async def message_aware_sleep(total_time, msg_time):
        """ Sleep for total_time, while calling PumpWaitingMessages() every msg_time """
        for _ in range(int(total_time / msg_time)):
            win32gui.PumpWaitingMessages()
            await asyncio.sleep(msg_time)

class WindowsNotifier:
    started = False
    bot :Bot = None

    def __init__(self,currentBot:Bot):
        self.alive = True
        self.bot = currentBot


        icon_normal = path.realpath("assets/iconesmall.ico")
        print(icon_normal)

        self.icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        self.nid_flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP

        # Register the window class
        message_map = {
            win32con.WM_DESTROY: self.on_destroy,
            win32con.WM_COMMAND: self.on_command,
            win32con.WM_USER + 20: self.on_taskbar_notify,
        }
        self.wc = win32gui.WNDCLASS()
        hinst = self.wc.hInstance = win32api.GetModuleHandle(None)
        self.wc.lpszClassName = "DofusbotNotifierTaskbar"
        self.wc.lpfnWndProc = message_map


        try:
            class_atom = win32gui.RegisterClass(self.wc)
        except win32gui.error as err:
            if err.winerror != winerror.ERROR_CLASS_ALREADY_EXISTS:
                raise

        # Create the window
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(class_atom, "Taskbar", style, 0, 0, win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT, 0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)

        # Create icons
        try:
            self.hicon_normal = win32gui.LoadImage(hinst, icon_normal, win32con.IMAGE_ICON, 0, 0, self.icon_flags)
        except Exception as err:
            self.hicon_normal = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
            print(err)


        nid = (self.hwnd, 0, self.nid_flags, win32con.WM_USER + 20, self.hicon_normal, "Dofus Bot")
        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        except win32gui.error:
            print("Failed to create taskbar icon. Possibly explorer has crashed or has not yet started.")

    def on_destroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32api.PostQuitMessage(0)
        sys.exit(1)

    def on_taskbar_notify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_RBUTTONUP:
            menu = win32gui.CreatePopupMenu()
            # win32gui.AppendMenu(menu, self.menu_mindustry_flags[self.game_state], 1024, "Show Mindustry Game")
            win32gui.AppendMenu(menu, self.started, 1020, "Start")
            win32gui.AppendMenu(menu, not self.started, 1021, "Pause")
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1025, "Exit Notifier")
            pos = win32gui.GetCursorPos()
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return 1

    def on_command(self, hwnd, msg, wparam, lparam):
        wid = win32api.LOWORD(wparam)
        if wid == 1020:
            self.started = True
            self.bot.start()
        elif wid == 1021:
            self.started =False
            self.bot.stop()
            # WindowsNotifier.show_game_window()
        elif wid == 1025:
            win32gui.DestroyWindow(self.hwnd)
            win32gui.UnregisterClass(self.wc.lpszClassName, None)
            self.alive = False
        else:
            print(f"Unknown command: {wid}")

def launchnotif(currentBot:Bot):
    notifier = Notifier(currentBot)
    loop = asyncio.get_event_loop()
    future = loop.create_task(notifier.monitor())
    loop.run_until_complete(future)