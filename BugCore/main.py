import asyncio
import sys
import aiohttp
from aiohttp import client_exceptions, client
import json
from PyQt6.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox, QComboBox, QPushButton, QLineEdit

)

from PyQt6.uic import loadUi

from main_window_ui import Ui_LoveBug


class Window(QMainWindow, Ui_LoveBug):
    def __init__(self, parent=None):

        super().__init__(parent)
        self.setupUi(self)
        self.connectHooks()

        for setting in self.L_settings.findChildren((QLineEdit, QComboBox)):
            if setting.__class__ == QLineEdit:
                setting.setProperty("text", s[setting.objectName().removeprefix("t_")])
            elif setting.__class__ == QComboBox:
                setting.setProperty("currentText", s[setting.objectName().removeprefix("cb_")])

    def connectHooks(self):

        # Page 3, Page 2
        self.b_saveSettings.clicked.connect(self.SaveSettings)

    def SaveSettings(self):
        settings = {}
        for setting in self.L_settings.findChildren((QLineEdit, QComboBox)):
            if setting.__class__ == QLineEdit:
                settings[setting.objectName().removeprefix("t_")] = setting.text()
            elif setting.__class__ == QComboBox:
                settings[setting.objectName().removeprefix("cb_")] = setting.currentText()
        data = {}
        with open("settings.json", "r") as j:
            data = json.load(j)
            data |= settings  # merge dicts operator
            j.close()
        with open("settings.json", 'w+') as j:
            json.dump(data, j, indent=4)
            j.close()


async def networking(data):
    print("Networking")
    try:
        async with aiohttp.ClientSession(data["URL"]) as session:
            async with session.get("/ketchup", params={"epoch": 1}) as resp:
                print(resp.status)
                print(await resp.text())
            async with session.post("/updateSettings", params=data) as resp:
                print(await resp.text())
    except aiohttp.client_exceptions.ClientConnectionError as e:
        print("No Server Found!")


with open("settings.json", "r") as r:
    s = json.load(r)
    r.close()
asyncio.run(networking(s))
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
