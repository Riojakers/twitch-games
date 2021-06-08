import threading
import time

import websocket
import logging

from api.config import oauth, nick, channel

from twitchAPI.twitch import Twitch

'''
# color: red, blue, grey....
# direction: up, down, left, right
def on_move_event(color, direction):
    pass


async def run_app():
    CommandChat(debug=False, on_move_event=on_move_event)


asyncio.get_event_loop().run_until_complete(run_app())
'''




class CommandChat:

    def __init__(self, on_move_event=None, debug=False):
        self.commands = {}
        self.lock = threading.Lock()
        self.on_move_event = on_move_event
        threading.Thread(target=self.timming_group).start()
        self.chat = ChatWrapper(oauth, nick, channel, self.on_command, self.on_error, debug)
        self.chat.start()

    def on_command(self, nick, command):
        # Standard replaces
        while "  " in command:
            command = command.replace("  ", " ")
        # Commands
        if command.startswith("!commands"):
            print("HEY")
            self.chat.send('PRIVMSG #<rimander> :This is a sample message')

        # Start with !move
        if not command.startswith("!move"):
            return

        color = command.split(" ")[1].strip()
        direction = command.split(" ")[2].strip()

        # Valid color
        if color not in ['red', 'blue', 'orange', 'white', 'black', 'yellow']:
            return

        # Valir direction
        if direction not in ['up', 'down', 'left', 'right']:
            return

        key = '{} {}'.format(color, direction)

        self.lock.acquire()
        try:
            if key not in self.commands.keys():
                self.commands[key] = 0

            self.commands[key] = self.commands[key] + 1

        except:
            logging.error("Count commands")
        self.lock.release()

    def on_error(self, content):
        print("Error: {}".format(content))

    # Calculate next move and emit event
    def _next_move(self):
        # Has commands
        if len(self.commands.values()) > 0:
            next_move = max(self.commands, key=self.commands.get)
            color = next_move.split(" ")[0]
            direction = next_move.split(" ")[1]
            self.on_move_event(color, direction)
            self.commands = {}

    # Each 10 seconds, next move
    def timming_group(self):
        while True:
            time.sleep(10)
            self._next_move()


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

    def send(self, pass_message):
        self.ws.send(pass_message)

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
