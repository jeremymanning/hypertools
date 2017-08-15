import json
import sys
import numpy as np
import time
import zmq
from sklearn.decomposition import PCA as PCA
from .._shared.helpers import *
import threading, time
from pynput import keyboard

global LASTKEY; LASTKEY = None

def on_press(key):
    global LASTKEY
    LASTKEY = key.char

def zscore(X, y):
    return (y - np.mean(X)) / np.std(X) if len(set(y))>1 else np.zeros(y.shape)

def scale(x):
    m1 = np.min(x)
    m2 = np.max(x - m1)
    f = lambda x: 2*((x - m1) / m2) - 1
    return f(x), m1, m2

class Interface:
    def __init__(self, port=3000, verbose=False):
        context = zmq.Context()
        self._socket = context.socket(zmq.PAIR)
        self._socket.connect("tcp://localhost:%d" % int(port))
        self.verbose = verbose

        if self.verbose:
            print("Client Ready!")

        # Send a quick message to tell node process we are up and running
        self.send(json.dumps({
            'action': 'started',
            'command': 'status',
            'message': time.time()*1000.0
        }))

    def send(self, msg):
        """
        Sends a message to TCP server
        :param msg: str
            A string to send to node TCP server, could be a JSON dumps...
        :return: None
        """
        if self.verbose:
            print('<- out ' + msg)
        self._socket.send(msg)
        return

    def recv(self):
        """
        Checks the ZeroMQ for data
        :return: str
            String of data
        """
        return self._socket.recv()


class RingBuffer(np.ndarray):
    """A multidimensional ring buffer."""

    def __new__(cls, input_array):
        obj = np.asarray(input_array).view(cls)
        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return

    def __array_wrap__(self, out_arr, context=None):
        return np.ndarray.__array_wrap__(self, out_arr, context)

    def append(self, x):
        """Adds element x to the ring buffer."""
        x = np.asarray(x)
        self[:, :-1] = self[:, 1:]
        self[:, -1] = x

class Stream:
    """
    """
    def __init__(self, port=3000, buffer_size=2500, nb_chans=8, sample_rate=250,
                 verbose=False):

        # port
        self.port = port

        #  size
        self.buffer_size = buffer_size

        # sample rate
        self.sample_rate = sample_rate

        # number of channels
        self.nb_chans = nb_chans

        # create a new python interface.
        self.interface = Interface(port=port, verbose=verbose)

        # create buffer
        self.signal = RingBuffer(np.zeros((nb_chans, buffer_size)))

        # attach methods
        self.start = self.start
        self.get = self.get
        self.init = self.init
        self.parse_sample = self.parse_sample

    def init(self, duration=10, model='PCA'):
        """
        """
        print('Fitting dimensionality reduction model...')
        self.model_signal = np.zeros((self.sample_rate * duration, self.nb_chans))
        i=0
        while i < (self.sample_rate * duration):
            self.model_signal[i,:]=self.parse_sample(self.interface.recv())
            i+=1
        self.model = PCA(n_components=3)
        self.model.fit(self.model_signal)
        print('Model fit!')

        self.model_signal, self.model_signal_min, self.model_signal_max \
        = scale(self.model.transform(self.model_signal))

    def transform(self, x):
        return self.model.transform(x)

    def scale(self, x):
        return 2 * ((x - self.model_signal_min) / self.model_signal_max) - 1

    def get(self, samples):
        return self.scale(self.transform(self.signal[:, -samples:].T))

    def start(self):

        def stream():
            while True:
                msg = self.interface.recv()
                self.signal.append(self.parse_sample(msg))

        thread = threading.Thread(target=stream)
        thread.start()

    def parse_sample(self, msg):
        try:
            dicty = json.loads(msg)
            action = dicty.get('action')
            command = dicty.get('command')
            message = dicty.get('message')

            if command == 'sample':
                if action == 'process':
                    # Do sample processing here
                    try:
                        if type(message) is not dict:
                            print("sample is not a dict", message)
                            raise ValueError

                        # Get keys of sample
                        data = np.zeros(8)

                        data = message.get('channelData')

                        return data

                        # print(message.get('sampleNumber', data))

                    except ValueError as e:
                        print(e)
            elif command == 'status':
                if action == 'active':
                    interface.send(json.dumps({
                        'action': 'alive',
                        'command': 'status',
                        'message': time.time() * 1000.0
                    }))

        except BaseException as e:
            print(e)
