import socket
from threading import Thread
import time
import requests

from app.utils.event import Event

class ChannelNotFoundError(Exception):
    def __init__(self, channel_name):
        super().__init__(f"Canal '{channel_name}' não encontrado. Verifique o nome e tente novamente.")

class TwitchConnection(Thread):
    STATUS_UNCONNECTED = "Desconectado"
    STATUS_CONNECTED = "Conectado"
    STATUS_ERROR = "Erro"
    STATUS_AWAITING = "Aguardando conexão"
    
    def __init__(self, channel_name):
        super().__init__()
        self.event_call = Event()
        if not self.__channel_exist__(channel_name):
            raise ChannelNotFoundError(channel_name)
        
        self.channel_name = channel_name
        self.HOST = "irc.chat.twitch.tv"
        self.PORT = 6667
        self.s = socket.socket()
        
        self.running = False
        
        self.status = None
        self.__status_change__(self.STATUS_UNCONNECTED)
        
    def __channel_exist__(self, channel_name):
        url = "https://gql.twitch.tv/gql"
        payload = [{
                "operationName": "GetUserID",
                "variables": {
                    "login": channel_name,
                    "lookupType": "ACTIVE"
                },
                "extensions": {
                    "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "bf6c594605caa0c63522f690156aa04bd434870bf963deb76668c381d16fcaa5"
                    }
                }
            }
        ]
        response = requests.post(url, json=payload, headers={"client-id": "kimne78kx3ncx6brgo4mv6wki5h1ko"})
        if response.status_code == 200:
            response_data = response.json()
            user_id = response_data[0].get("data", {}).get("user", None)
            return user_id is not None
        return False
        
    def __status_change__(self, new_status):
        if self.status != new_status:
            self.status = new_status
            self.event_call.trigger("status_change", new_status)    
    
    def connect(self):
        self.__status_change__(self.STATUS_AWAITING)
        self.s.connect((self.HOST, self.PORT))
        
        self.s.send("CAP REQ :twitch.tv/tags twitch.tv/commands\r\n".encode('utf-8'))
        self.s.send("PASS SCHMOOPIIE\r\n".encode('utf-8'))
        self.s.send("NICK justinfan64198\r\n".encode('utf-8'))
        self.s.send("USER justinfan64198 8 * :justinfan64198\r\n".encode('utf-8'))
        self.running = True

    def run(self):
        self.connect()

        try:
            while self.running:
                self.__status_change__(self.STATUS_CONNECTED)
                response = self.s.recv(2048).decode('utf-8')
                if not response:
                    break

                parts = response.split("\r\n")
                for part in parts:
                    if part.startswith("PING"):
                        self.s.send("PONG\r\n".encode('utf-8'))
                        # print(">> Mantendo conexão ativa (Respondido ao PING da Twitch)")
                        continue

                    if part.startswith(":tmi.twitch.tv"):
                        self.s.send(f"JOIN #{self.channel_name}\r\n".encode('utf-8'))
                        
                    if part.startswith("@") and "PRIVMSG" in part:
                        self.event_call.trigger("message", part.strip()[1:])
                        
        except ConnectionAbortedError:
            self.running = False
        except Exception:
            self.status = self.STATUS_ERROR
            self.__status_change__(self.STATUS_ERROR)
    def stop(self):
        self.running = False
        self.s.close()
        self.__status_change__(self.STATUS_UNCONNECTED)

    """ events """
    def on_message(self, callback):
        self.event_call.add("message", callback)
        
    def on_change_status(self, callback):
        self.event_call.add("status_change", callback)

if __name__ == "__main__":
    def print_message(msg):
        print("Nova mensagem:", msg)

    twitch = TwitchConnection("gambitzeros")
    
    twitch.on_message(print_message)
    twitch.start()
    
    time.sleep(10)  # Mantenha a conexão por 10 segundos para testar
    twitch.stop()