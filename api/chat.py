import threading
import time

import websocket
import logging


class ChatWrapper:

    def __init__(self, oauth, nick, channel, on_command=None, on_error=None, debug=False):
        # Config
        self.oauth = oauth
        self.nick = nick
        self.channel = channel

        # Events
        self.on_command = on_command
        self.on_error = on_error

        # WSS Debug
        self.debug = debug

    def start(self):
        websocket.enableTrace(self.debug)
        self.ws = websocket.WebSocketApp('wss://irc-ws.chat.twitch.tv:443',
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_open=self.on_open,
                                         on_close=self.on_close)
        # Start using thread
        threading.Thread(target=self.ws.run_forever).start()

    def on_message(self, ws, message):
        ## priv
        if 'PRIVMSG' in message:
            # Extract content and user
            # TODO: Change to regular expresion
            content = message.split(':')[-1]
            user = message.split(':')[1].split('!')[0]

            if content.startswith('!') and self.on_command is not None:
                self.on_command(user, content)
        ## notice
        elif 'NOTICE' in message:
            if self.on_error is not None:
                # Extract content
                # TODO: Change to regular expresion
                content = message.split(':')[-1]
                self.on_error(content)

        logging.debug('Message: {}'.format(message))

    def on_error(self, ws, error):
        if self.debug:
            logging.error('Error: {}'.format(error))

    def on_close(self, ws):
        if self.debug:
            logging.info('WSS closed')

    def on_open(self, ws):
        def run(*args):
            # Login with pass and nick
            pass_message = 'PASS {}'.format(self.oauth)
            ws.send(pass_message)
            nick_message = 'NICK {}'.format(self.nick)
            ws.send(nick_message)
            # Wait logged
            time.sleep(3)
            # Join in channel
            channel_message = 'JOIN #{}'.format(self.channel)
            ws.send(channel_message)

        # Start using thread
        threading.Thread(target=run).start()
