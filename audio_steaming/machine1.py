
from random import randint

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import pyaudio
import numpy as np
import soundcard as sc


class Client(DatagramProtocol):
    def startProtocol(self):
        py_audio = pyaudio.PyAudio()
        self.buffer = 1024  # 127.0.0.1
        # self.another_client = "127.0.0.1", int(3001)
        self.another_client = "192.168.1.6", int(3000)

        # self.output_stream = py_audio.open(format=pyaudio.paInt16,
        #                                    output=True, rate=44100, channels=2,
        #                                    frames_per_buffer=self.buffer)
        self.input_stream = py_audio.open(format=pyaudio.paInt16,
                                          input=True, rate=44100, channels=2,
                                          frames_per_buffer=self.buffer)

        self.default_speaker = sc.default_speaker()

        reactor.callInThread(self.record)


    def record(self):
        while True:
            data = self.input_stream.read(self.buffer)
            self.transport.write(data, self.another_client)

    def datagramReceived(self, datagram, addr):
        # self.output_stream.write(datagram)
        self.default_speaker.play(datagram/np.max(datagram), samplerate=44100)

if __name__ == '__main__':
    port = 3000
    print("Working on port: ", port)

    reactor.listenUDP(port, Client())
    reactor.run()
