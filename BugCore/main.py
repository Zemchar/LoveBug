import base64
import datetime
import json
import random
import sys
import threading
import urllib.request
import aiohttp
import cv2
import asyncio
from desktop_notifier import DesktopNotifier
import numpy as np
import requests
import websocket
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (

    QApplication, QMainWindow, QComboBox, QLineEdit, QFileDialog, QTextEdit

)

from main_window_ui import Ui_LoveBug

comboGames = {}


class Window(QMainWindow, Ui_LoveBug):
    update_text_signal = pyqtSignal(str, bool)

    def __init__(self, parent=None):
        self.ws = None
        self.resp = None
        self.notifier = DesktopNotifier()
        super().__init__(parent)
        print("[SETUP][1/5] Loading UI")
        self.setupUi(self)
        print("[SETUP][2/5] Inserting Settings")
        if globalSettings["UserCode"] == "":
            self.SaveSettings(userCode=random.randint(900_000, 1_000_000))
        for setting in self.L_settings.findChildren((QLineEdit, QComboBox, QTextEdit)):
            if setting.__class__ == QLineEdit:
                setting.setProperty("text", globalSettings[setting.objectName().removeprefix("t_")])
            elif setting.__class__ == QComboBox:
                setting.setProperty("currentText", globalSettings[setting.objectName().removeprefix("cb_")])
            elif setting.__class__ == QTextEdit:
                setting.setProperty("markdown", globalSettings[setting.objectName().removeprefix("t_")])
        print("[SETUP][3/5] Initiate Server Connection")
        self.WindowNetwork("GET", globalSettings["URL"], "newLoad", globalSettings)
        print("[SETUP][4/5] Connecting Hooks")
        self.connectHooks()
        print("[SETUP][5/5] Populating Games")
        self.populateGames()
        print("[SETUP] Complete")
        self.update_text_signal.connect(self.update_text_browser)
        threading.Thread(target=self.WS_Receiver).start()

    def update_text_browser(self, msg, do_notif=True):
        text = ""
        notifTitle = ""
        try:
            msg = json.loads(msg)
        except Exception as e:
            msg = msg.replace('\'', '\"')
            msg = json.loads(msg)
        finally:
            if msg["EventType"] == "SEND_MOOD":

                if msg["Data"]["Sender"] != globalSettings["userName"]:
                    self.Mood.setText(json.loads(msg)["Data"]["Mood"])
                    text += f"{msg['Data']['Sender']} Updated their mood to {msg['Data']['Mood']}"
                    notifTitle = "Mood Update"
                else :
                    text += f"You Updated your mood to {msg['Data']['Mood']}"
            elif msg["EventType"] == "SEND_GAME":
                if msg["Data"]["Sender"] != globalSettings["userName"]:
                    text += f"{msg['Data']['Sender']} wants to play {msg['Data']['Game']}"
                    notifTitle = f"Your partner wants to play a game"
                else:
                    text += f"You requested to play {msg['Data']['Game']}"
                pass
            elif msg["EventType"] == "SEND_LOVE":
                if(msg["Data"]["Recipient"] == globalSettings["userName"]):
                    text += f"{msg['Data']['Sender']} loves you"
                    notifTitle = f"Your partner loves you"
                else:
                    text += f"You reminded {msg['Data']['Recipient']} that you love them"
            elif msg["EventType"] == "SEND_KISS":
                if(msg["Data"]["Recipient"] == globalSettings["userName"]):
                    text += f"{msg['Data']['Sender']} kissed you!"
                    notifTitle = f"Your partner kissed you"
                else:
                    text += f"You kissed {msg['Data']['Recipient']}!"
            elif msg["EventType"] == "SEND_THINK":
                if(msg["Data"]["Recipient"] == globalSettings["userName"]):
                    text += f"{msg['Data']['Sender']} is thinking about you!"
                    notifTitle = f"Your partner is thinking about you"
                else:
                    text += f"You are thinking about {msg['Data']['Recipient']}!"
            # notifTitle = "TESZT"
            if notifTitle != "" and globalSettings["NotifBox"] == "On" and do_notif:
                self.notifier.send_sync(notifTitle, text)
            msg["Epoch"] = int(msg["Epoch"])
            self.textBrowser.setPlainText(f'[{datetime.datetime.fromtimestamp(msg["Epoch"]).strftime( "%m-%d-%Y %H:%M:%S" )}] {text}' + "\n" + self.textBrowser.toPlainText())

    def WS_Receiver(self):
        print("[WS] Starting Receiver on thread " + threading.current_thread().name)
        try:
            if not self.ws:
                self.resp = self.WindowNetwork("GET", globalSettings["URL"], "reqWS", {"UserCode": globalSettings["UserCode"]})
                self.ws = websocket.WebSocket()
                self.ws.connect(f"ws://{self.resp['Host']}:{self.resp['Port']}/Nest")
                self.ws.send({"EventType": "init", "PCode": globalSettings["PartnerCode"], "Code": globalSettings["UserCode"]}.__str__())
            asyncio.run(self.WSR_Loop())
        except Exception as e:
            print("[WS] Connection Closed, Retrying in 10 seconds\n==> " + e.__str__())
            asyncio.run(self.WSR_Loop())
            self.label_5.setText(self.label_5.text() + "\nWebSocket Connection Failed")
            self.label_5.setStyleSheet("color: rgb(255, 0, 0); font-weight: bold; font-size: 8px;")

    async def WSR_Loop(self):
        print("[WS] Starting Loop on thread " + threading.current_thread().name)
        while True:
            try:
                while True:
                    if (self.ws.recv()):
                        resp = json.loads(self.ws.recv())
                        print(f"[WS] Received {resp}")
                        if (resp.keys().__contains__("MsgUpdate") and len(resp["MsgUpdate"]) > 0):
                            resp["MsgUpdate"].reverse()
                            for msg in resp["MsgUpdate"]:
                                msg["Data"] = json.loads(msg["Data"])
                                msg = msg.__str__().replace('\'', '\"')
                                self.update_text_signal.emit(f"{msg}", False)  # this is some bullshit.
                        if (resp.keys().__contains__("NewComm") and resp["NewComm"][0]["Code"] != globalSettings["UserCode"]):
                            resp['NewComm'][0] = resp['NewComm'][0].__str__().replace('\'', '\"')
                            self.update_text_signal.emit(f"{resp['NewComm'][0]}")
            except Exception as e:
                try:
                    if self.ws is not None:
                        self.ws.close()
                    print(f"[WS] Connection Closed due to error, Retrying...\n==> {e} {e.__traceback__.tb_lineno}")
                    self.resp = self.WindowNetwork("GET", globalSettings["URL"], "reqWS",
                                                   {"UserCode": globalSettings["UserCode"]})
                    self.ws = None
                    self.ws = websocket.WebSocket()
                    self.ws.connect(f"ws://{self.resp['Host']}:{self.resp['Port']}/Nest")
                    self.ws.send({"EventType": "init", "PCode": globalSettings["PartnerCode"], "Code": globalSettings["UserCode"]}.__str__())
                except Exception as e:
                    print(f"[WS] Failed to re-connect, Retrying in 10 seconds\n==> {e} {e.__traceback__.tb_lineno}")
                    self.label_5.setText(self.label_5.text() + "\nWebSocket Connection Failed")
                    self.label_5.setStyleSheet("color: rgb(255, 0, 0); font-weight: bold; font-size: 8px;")
                    await asyncio.sleep(10)

    def connectHooks(self):

        # Page 3, Page 2
        self.b_saveSettings.clicked.connect(self.SaveSettings)
        self.cb_SelectGame.currentIndexChanged.connect(self.ChangeGameImage)
        self.b_Randomize.clicked.connect(self.RandomizeGames)
        self.b_love.clicked.connect(self.WS_ButtonSend)  # i hate this this is dumb
        self.b_kiss.clicked.connect(self.WS_ButtonSend)
        self.b_think.clicked.connect(self.WS_ButtonSend)
        self.b_SubmitButton.clicked.connect(self.WS_ButtonSend)
        self.b_Request.clicked.connect(self.WS_ButtonSend)
        self.b_pfpSelect.clicked.connect(self.SelectPFP)

    def SelectPFP(self):  # Send IMMEDIATELY
        fname = QFileDialog.getOpenFileName(self, 'Open file', '', "Image files (*.jpg, *.png)")
        if fname[0] != "":
            with open(fname[0], "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                self.WindowNetwork("POST", globalSettings["URL"], "resource",
                                   {"Code": globalSettings["UserCode"], "Data": encoded_string.__str__()}.__str__())
                self.pfpLabel.setPixmap(QPixmap(QImage(fname[0])))

    def WS_ButtonSend(self):
        data = {}
        match (self.sender().objectName()):
            case "b_love":
                data = {"Code": globalSettings["UserCode"], "Data": {"Sender": f"{globalSettings['userName']}", "Recipient": f"{self.Name.text()}"},
                                      "EventType": "SEND_LOVE"}
                self.SendToWebSocket(data)
                data.update({"Epoch": int(datetime.datetime.now().timestamp())})
                self.update_text_browser(data.__str__())

            case "b_kiss":
                data = {"Code": globalSettings["UserCode"], "Data": {"Sender": f"{globalSettings['userName']}", "Recipient": f"{self.Name.text()}"},
                 "EventType": "SEND_KISS"}
                self.SendToWebSocket(data.__str__())
                data.update({"Epoch": int(datetime.datetime.now().timestamp())})
                self.update_text_browser(data.__str__())
            case "b_think":
                data = {"Code": globalSettings["UserCode"], "Data": {"Sender": f"{globalSettings['userName']}", "Recipient": f"{self.Name.text()}"},
                     "EventType": "SEND_THINK"}
                self.SendToWebSocket(data)
                data.update({"Epoch": int(datetime.datetime.now().timestamp())})
                self.update_text_browser(data.__str__())
            case "b_SubmitButton":
                data = {"Code": globalSettings["UserCode"], "Data": {"Sender": f"{globalSettings['userName']}", "Mood": f"{self.t_MoodBox.text()}"},
                     "EventType": "SEND_MOOD"}
                self.SendToWebSocket(data)
                data.update({"Epoch": int(datetime.datetime.now().timestamp())})
                self.update_text_browser(data.__str__())
                self.l_CurrentMood.setText(f"Your mood is currently: {self.t_MoodBox.text()}")
            case "b_Request":
                if (self.t_custom.toPlainText() != ""):
                    data = {"Code": globalSettings["UserCode"], "Data": {"Sender": f"{globalSettings['userName']}", "Game": f"{self.t_custom.toPlainText()}"},
                         "EventType": "SEND_GAME"}
                    self.SendToWebSocket(data.__str__())
                    data.update({"Epoch": int(datetime.datetime.now().timestamp())})
                    self.update_text_browser(data.__str__())
                    return  # dont do anything else
                data = {"Code": globalSettings["UserCode"], "Data": {"Sender": f"{globalSettings['userName']}", "Game": f"{self.cb_SelectGame.currentText()}"},
                     "EventType": "SEND_GAME"}
                self.SendToWebSocket(data)
                data.update({"Epoch": int(datetime.datetime.now().timestamp())})
                self.update_text_browser(data.__str__())

    def RandomizeGames(self):
        i =0
        while i < 20:  # Max 20 retries
            rand = random.choice(list(comboGames.keys()))
            if rand != self.cb_SelectGame.currentText():
                break
            i+=1
        self.cb_SelectGame.currentIndexChanged.disconnect()  # temporarily disconnect the signal
        self.cb_SelectGame.setCurrentText(rand)
        self.cb_SelectGame.currentIndexChanged.connect(self.ChangeGameImage)  # reconnect the signal
        self.ChangeGameImage()

    def ChangeGameImage(self):
        current = self.cb_SelectGame.currentText()
        if (comboGames[current] == "-1"):
            self.WindowNetwork("GET", globalSettings["URL"], "resource", {"ResourceType": "customGame"})  ##HANDED OFF
        else:
            asyncio.run(self.fetchImgAsync(current))

    async def fetchImgAsync(self, current):
        data =  requests.get(f"https://store.steampowered.com/api/appdetails/?appids={comboGames[current]}").json()
        self.game_img.setPixmap(url_to_image(data[f'{comboGames[current]}']["data"]["header_image"]))
    def SaveSettings(self, userCode: ""):
        settings = {}
        for setting in self.L_settings.findChildren((QLineEdit, QComboBox, QTextEdit)):
            if (setting.__class__ == QTextEdit):
                settings[setting.objectName().removeprefix("t_")] = setting.toPlainText()
            if setting.__class__ == QLineEdit:
                settings[setting.objectName().removeprefix("t_")] = setting.text()
                if (setting.objectName().removeprefix("t_") == "UserCode" and userCode):
                    print("Saving Code")
                    settings["UserCode"] = f"{userCode}"
                    globalSettings["UserCode"] = f"{userCode}"
                    continue
            elif setting.__class__ == QComboBox:
                settings[setting.objectName().removeprefix("cb_")] = setting.currentText()
        with open("settings.json", "r") as j:
            data = json.load(j)
            data |= settings  # merge dicts operator
            j.close()
        with open("settings.json", 'w+') as j:
            json.dump(data, j, indent=4)
            j.close()

        self.WindowNetwork("GET", data["URL"], "newLoad", data)
        self.SendToWebSocket({"EventType": "SettingsUpdate", "Settings": data, "Code": globalSettings["UserCode"]})
        ReloadSettings()

    def WindowNetwork(self, method, url, endpoint, data):
        print(f"[STATIC NETWORKING] Sending {method} request to {url}{endpoint}")
        try:
            resp = asyncio.run(networking(method, url, endpoint, data))
            resp = json.loads(resp)
            if (resp['status'] == "success"):
                if resp["responseType"] == 'ImageUpload':
                    return
                if resp["responseType"] == "R_GamePlaceholder":
                    i = base64.b64decode(resp["data"])
                    img_file = open('cgame.jpg', 'wb')
                    img_file.write(i)
                    img_file.close()
                    self.game_img.setPixmap(QPixmap(QImage("cgame.jpg")))
                    return
                resp["data"] = json.loads(resp["data"])
                if (resp["responseType"] == "PartnerProfile"):
                    d1 = {}
                    d1["PartnerName"] = resp["data"]["Name"]
                    globalSettings["PartnerSteamID"] = resp["data"]["SteamID"]
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
                if (resp["responseType"] == "WSInfo"):
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
            steamApiKey = globalSettings["APIKey"]
            slink1 = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steamApiKey}&steamid={globalSettings['SteamID']}&include_appinfo=1&format=json&include_played_free_games=1"
            r = requests.get(slink1)
            data = r.json()
            data2 = {}
            if (globalSettings["PartnerSteamID"] != ""):
                slink2 = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={steamApiKey}&steamid={globalSettings['PartnerSteamID']}&include_appinfo=1&format=json&include_played_free_games=1"
                r = requests.get(slink2)
                data2 = r.json()
            if (data["response"] == {} or data["response"] == None or data2["response"] == {} or data2[
                "response"] == None):
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

    def SendToWebSocket(self, data=None):
        try:
            self.ws.send(data.__str__())
        except Exception as e:
            print(f"[WS] Connection Closed\n==> {e} {e.__traceback__.tb_lineno}")
            self.label_5.setText(self.label_5.text() + "\nWebSocket Connection Failed")
            self.label_5.setStyleSheet("color: rgb(255, 0, 0); font-weight: bold; font-size: 8px;")
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
        elif method == "POST":
            async with session.post(f"/{endpoint}", data=data) as resp:
                return await resp.text()



if __name__ == "__main__":
    with open("settings.json", "r") as r:
        globalSettings = json.load(r)
        r.close()
    def ReloadSettings():
        global globalSettings
        globalSettings.clear()
        with open("settings.json", "r") as r:
            globalSettings = json.load(r)
            r.close()
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
