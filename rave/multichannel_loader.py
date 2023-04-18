import numpy as np
import pdb
from tqdm import tqdm
from random import randint
from pathlib import Path
from os import path
from udls import SimpleDataset
from udls.transforms import Transform
import librosa as li

def simple_audio_preprocess(sampling_rate, N, n_channels = 2):
    def preprocess(name):
        try:
            x, sr = li.load(name, sr=sampling_rate, mono=False)
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print(e)
            return None

        pad = (N - (x.shape[-1] % N)) % N
        if len(x.shape) == 1:
            x = np.expand_dims(x, axis=0).repeat(n_channels, axis=0)
        if x.shape[0] > n_channels:
            x = x[:n_channels]
        try:
            if len(x.shape) > 1:
                x = np.pad(x, (*((0,0)*(len(x.shape)-1),), (0, int(pad))))
            else:
                x = np.pad(x, (0, int(pad)))
        except TypeError:
            pdb.set_trace()
        try:
            x = x.reshape(-1, n_channels, N)
        except Exception as e:
            pdb.set_trace()
        x = x.reshape(n_channels, -1, N)
        x = np.transpose(x, (1, 0, 2))
        return x.astype(np.float32)

    return preprocess


class RandomCrop(Transform):
    """
    Randomly crops signal to fit n_signal samples
    """
    def __init__(self, n_signal):
        self.n_signal = n_signal

    def __call__(self, x: np.ndarray):
        in_point = randint(0, x.shape[-1] - self.n_signal)
        x = x[..., in_point:in_point + self.n_signal]
        return x


class Dequantize(Transform):
    def __init__(self, bit_depth):
        self.bit_depth = bit_depth

    def __call__(self, x: np.ndarray):
        x += np.random.rand(x.shape[-1]) / 2**self.bit_depth
        return x


class MCDataset(SimpleDataset):
    def _preprocess(self):
        extension = self.extension.split(",")
        idx = 0
        wavs = []

        # POPULATE WAV LIST
        if self.folder_list is not None:
            for f, folder in enumerate(self.folder_list.split(",")):
                print("Recursive search in {}".format(folder))
                for ext in extension:
                    wavs.extend(list(Path(folder).rglob(ext)))

        else:
            with open(self.file_list, "r") as file_list:
                wavs = file_list.read().split("\n")

        loader = tqdm(wavs)
        for wav in loader:
            loader.set_description("{}".format(path.basename(wav)))
            output = self.preprocess_function(wav)
            if output is not None:
                for o in output:
                    self.env[idx] = o
                    idx += 1

    def __getitem__(self, index):
        data = self.env[self.index[index + self.offset]]
        if self.transforms is not None:
            data = self.transforms(data)
        return data
