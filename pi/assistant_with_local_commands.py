#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Run a recognizer using the Google Assistant Library.

The Google Assistant Library has direct access to the audio API, so this Python
code doesn't need to record audio. Hot word detection "OK, Google" is supported.

It is available for Raspberry Pi 2/3 only; Pi Zero is not supported.
"""

import logging
import platform
import subprocess
import sys
import requests

from google.assistant.library.event import EventType

from aiy.assistant import auth_helpers
from aiy.assistant.library import Assistant
from aiy.board import Board, Led
from aiy.voice import tts

def power_off_pi():
    tts.say('Good bye!')
    subprocess.call('sudo shutdown now', shell=True)

def reboot_pi():
    tts.say('See you in a bit!')
    subprocess.call('sudo reboot', shell=True)

def say_ip():
    ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
    tts.say('My IP address is %s' % ip_address.decode('utf-8'))


min_list = ['small', 'smaller', 'tiny', 'tinier', 'little', 'littler', 'miniaturize']
max_list = ['large', 'larger', 'big', 'bigger', 'huge', 'huger', 'enormous', 'colossal', 'massive', 'enlarge']
player_list = ['mate', 'mates', 'partner', 'partners', 'colleague', 'colleagues', 'ally', 'allies', 'teammate', 'teammates', 'person', 'persons', 'user', 'users', 'player', 'players', 'friend', 'friends']
min_list = set(min_list)
max_list = set(max_list)
player_list = set(player_list)

quest_ip_address = "192.168.1.13:4444"
tts_volume = 75

def make_request(url):
    try:
        r = requests.get("http://" + quest_ip_address + url, timeout=3)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(e)

def find_in_list(sentence):
    make_small = False
    make_big = False
    player = False

    for word in sentence.split():
        if word in min_list:
            make_small = True
        if word in max_list:
            make_big = True
        if word in player_list:
            player = True

    if player and make_small:
        # submit GET request to /miniaturize
        tts.say('Making your team mate in VR smaller!', volume=tts_volume)
        make_request("/minimize")
        return True
    elif player and make_big:
        # submit GET request to /maximize
        tts.say('Making your team mate in VR larger!', volume=tts_volume)
        make_request("/maximize")
        return True

    return False


def process_event(assistant, led, event):
    logging.info(event)
    if event.type == EventType.ON_START_FINISHED:
        led.state = Led.BEACON_DARK  # Ready.
        print('Say "OK, Google" then speak, or press Ctrl+C to quit...')
    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        led.state = Led.ON  # Listening.
    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
        print('You said:', event.args['text'])
        text = event.args['text'].lower()
        if text == 'power off':
            assistant.stop_conversation()
            power_off_pi()
        elif text == 'reboot':
            assistant.stop_conversation()
            reboot_pi()
        elif text == 'ip address':
            assistant.stop_conversation()
            say_ip()
        elif find_in_list(text):
            assistant.stop_conversation()

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        led.state = Led.PULSE_QUICK  # Thinking.
    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        led.state = Led.BEACON_DARK  # Ready.
    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        sys.exit(1)


def main():
    logging.basicConfig(level=logging.INFO)

    credentials = auth_helpers.get_assistant_credentials()
    with Board() as board, Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(assistant, board.led, event)


if __name__ == '__main__':
    main()