import asyncio
import base64
import datetime
import random
import sys
import aiohttp
import async_timeout
import requests
from PyQt6.QtGui import QImage, QPixmap
from aiohttp import client_exceptions, client
from PyQt6.QtCore import QCoreApplication
import numpy as np
import urllib.request
import cv2
import websocket
import json
import threading
from PyQt6.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox, QComboBox, QPushButton, QLineEdit

)

from PyQt6.uic import loadUi
from steam.webapi import WebAPI

from main_window_ui import Ui_LoveBug

comboGames = {}

class Window(QMainWindow, Ui_LoveBug):


    def __init__(self, parent=None):
        self.ws = None
        super().__init__(parent)
        self.setupUi(self)
        self.WindowNetwork("GET", s["URL"], "newLoad", s)
        self.connectHooks()
        if s["UserCode"] == "":
            print("Generating Code")
            self.SaveSettings(userCode=random.randint(900_000, 1_000_000))
        for setting in self.L_settings.findChildren((QLineEdit, QComboBox)):
            if setting.__class__ == QLineEdit:
                setting.setProperty("text", s[setting.objectName().removeprefix("t_")])
            elif setting.__class__ == QComboBox:
                setting.setProperty("currentText", s[setting.objectName().removeprefix("cb_")])
        self.populateGames()
        threading.Thread(self.WebSocket()).start()

    def connectHooks(self):

        # Page 3, Page 2
        self.b_saveSettings.clicked.connect(self.SaveSettings)
        self.cb_SelectGame.currentIndexChanged.connect(self.ChangeGameImage)
        self.b_Randomize.clicked.connect(self.RandomizeGames)

    def RandomizeGames(self):
        while True:  # No repeats
            rand = random.choice(list(comboGames.keys()))
            if rand != self.cb_SelectGame.currentText():
                break
        self.cb_SelectGame.currentIndexChanged.disconnect()  # temporarily disconnect the signal
        self.cb_SelectGame.setCurrentText(rand)
        self.cb_SelectGame.currentIndexChanged.connect(self.ChangeGameImage)  # reconnect the signal
        self.ChangeGameImage()

    def ChangeGameImage(self):
        current = self.cb_SelectGame.currentText()
        if (comboGames[current] == "-1"):
            self.WindowNetwork("GET", s["URL"], "resource", {"ResourceType": "customGame"})  ##HANDED OFF
        else:
            data = requests.get(f"https://store.steampowered.com/api/appdetails/?appids={comboGames[current]}").json()
            self.game_img.setPixmap(url_to_image(data[f'{comboGames[current]}']["data"]["header_image"]))

    def SaveSettings(self, userCode: ""):
        settings = {}
        for setting in self.L_settings.findChildren((QLineEdit, QComboBox)):
            if setting.__class__ == QLineEdit:
                if (setting.objectName().removeprefix("t_") == "AdditionalGames"):
                    if (setting.text() != ""):
                        settings[setting.objectName().removeprefix("t_")] = setting.text()
                    else:
                        settings[setting.objectName().removeprefix("t_")] = ""
                    continue
                settings[setting.objectName().removeprefix("t_")] = setting.text()
                if (setting.objectName().removeprefix("t_") == "UserCode" and userCode):
                    print("Saving Code")
                    settings["UserCode"] = f"{userCode}"
                    s["UserCode"] = f"{userCode}"
                    continue
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
        self.WindowNetwork("GET", data["URL"], "newLoad", data)

    def WindowNetwork(self, method, url, endpoint, data):
        print(f"Sending {method} request to {url}{endpoint}")
        try:
            resp = asyncio.run(networking(method, url, endpoint, data))
            resp = json.loads(resp)
            if (resp['status'] == "success"):
                if (resp["responseType"] == "R_GamePlaceholder"):
                    print(resp["data"])
                    i = base64.b64decode(resp["data"])
                    img_file = open('cgame.jpg', 'wb')
                    img_file.write(i)
                    img_file.close()
                    self.game_img.setPixmap(QPixmap(QImage("cgame.jpg")))
                    return
                resp["data"] = json.loads(resp["data"])
                if (resp["responseType"] == "partnerInfo"):
                    d1 = {}
                    d1["PartnerName"] = resp["data"]["Name"]
                    s["PartnerSteamID"] = resp["data"]["SteamID"]
                    self.Name.setText(resp["data"]["Name"])
                    self.Mood.setText(resp["data"]["Mood"])
                    if (resp["data"]["AdditionalGames"]):
                        d1["AdditionalPartnerGames"] = resp["data"]["AdditionalGames"]
                        r = resp["data"]["AdditionalGames"].split(",")
                        for game in r:
                            comboGames[game] = "-1"
                            self.cb_SelectGame.addItem(game)
                    if (resp["data"]["pfp"]):
                        pfp = base64.b64decode(resp["data"]["pfp"])
                        img_file = open('pfp.jpg', 'wb')
                        img_file.write(pfp)
                        img_file.close()
                        self.PFP.setPixmap(QPixmap(QImage("pfp.jpg")))

                    with open("settings.json", "r") as j:
                        data = json.load(j)
                        data |= d1  # merge dicts operator
                        j.close()
                    with open("settings.json", 'w+') as j:
                        json.dump(data, j, indent=4)
                        j.close()
                if(resp["responseType"] == "WSInfo"):
                    return resp["data"]
            if (resp['status'] == "failure"):
                raise Exception(resp["data"])
        except Exception as e:
            print(e)
            print(e.__traceback__.tb_lineno)
            self.label_5.setText(f"Remote Server URL\n{e}")
            self.label_5.setStyleSheet("color: rgb(255, 0, 0); font-weight: bold; font-size: 8px;")
            return
        self.label_5.setText(f"Remote Server URL")
        self.label_5.setStyleSheet("color: rgb(0, 255, 0);")

    def populateGames(self):
        try:
            steamApiKey = s["APIKey"]
            slink1 = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steamApiKey}&steamid={s['SteamID']}&include_appinfo=1&format=json&include_played_free_games=1"
            r = requests.get(slink1)
            data = r.json()
            data2 = {}
            if (s["PartnerSteamID"] != ""):
                slink2 = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steamApiKey}&steamid={s['PartnerSteamID']}&include_appinfo=1&format=json&include_played_free_games=1"
                r = requests.get(slink2)
                data2 = r.json()
            if(data["response"] == {} or data["response"] == None or data2["response"] == {} or data2["response"] == None):
                raise "[ERROR] Steam did not respond (rate limited?)"
                # use dictionary comprehension to merge the two dictionaries
            # Extract game app IDs from both dictionaries and convert them into sets
            app_ids1 = {game["appid"] for game in data["response"]["games"]}
            app_ids2 = {game["appid"] for game in data2["response"]["games"]}
        except Exception as e:
            print(e)
            app_ids1 = {game["appid"] for game in data["response"]["games"]}
            app_ids2 = set()

        # Find the common app IDs present in both dictionaries
        common_app_ids = app_ids1.intersection(app_ids2)

        data = {
            "response": {
                "game_count": len(common_app_ids),
                "games": [game for game in data["response"]["games"] if game["appid"] in common_app_ids]
                # only keep first persons responses so dupes dont show up
            }
        }

        data = sorted(data["response"]["games"], key=lambda x: x["playtime_forever"], reverse=True)
        for game in data:
            self.cb_SelectGame.addItem(game["name"])
            comboGames[game["name"]] = game["appid"]

    def WebSocket(self, data=None):
        try:
            if not self.ws:
                resp = self.WindowNetwork("GET", s["URL"], "reqWS", {"UserCode": s["UserCode"]})
                self.ws = websocket.WebSocket()
                self.ws.connect(f"ws://{resp['Host']}:{resp['Port']}/Nest")
                self.ws.send("INITIALIZE")
                print('[WS RESPONSE] ' + self.ws.recv())
            if(data):
                self.ws.send(data)
                while True:
                    if self.ws.recv() != "":
                      print("[WS RESPONSE]" + self.ws.recv())
        except Exception as e:
            print(f"Failed to connect to websocket server\n{e.with_traceback(e.__traceback__)} ({e.__traceback__.tb_lineno})")

            return


def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = QImage(image, image.shape[1], image.shape[0], QImage.Format.Format_BGR888)
    return QPixmap(image)


async def networking(method, url, endpoint, data):
    if endpoint.startswith("/"):
        endpoint = endpoint.removeprefix("/")
        print("Invalid Endpoint Format. Auto-Fixed")
    async with aiohttp.ClientSession(url) as session:
        if method == "GET":
            async with session.get(f"/{endpoint}", params=data) as resp:
                return await resp.text()

if __name__ == "__main__":
    with open("settings.json", "r") as r:
        s = json.load(r)
        r.close()
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
