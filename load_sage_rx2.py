import os
import struct
import numpy as np
import soundfile as sf
from xml.etree import ElementTree as Et
from audio_tools import AudioTools


def ieee754(string: str):
    return struct.unpack('!f', int(string, 16).to_bytes(4, byteorder='big'))[0]


class LoopSliceSeq:
    def __init__(self, data_dir: str, track_name: str,
                 x_volume: float=1.0, x_pan: float=0.0, x_stereo_swap: bool=False):

        _path_data = os.path.join(data_dir, "data.xml")
        _path_audio = os.path.join(data_dir, track_name, "Audio")

        self.sample_rate: int = 0
        self._slice_pos: list[tuple[int, int]] = []

        self.tempo: float = 0
        self.slice_count: int = 0
        self.slice_data: list[np.ndarray] = []
        self.slice_lengths: list[float] = []  # In beats

        self._get_slices_info(_path_data, track_name)
        self._load_slices_data(_path_audio, x_volume, x_pan, x_stereo_swap)

    def _get_slices_info(self, xml_path, track_name):
        xml_data = Et.parse(xml_path).getroot()
        loop_data = xml_data.find(f'LOOP[@AUDIOFILENAME="{track_name}"]')

        # Slice data
        for slice_data in loop_data.findall("SLICE"):
            slice_begin = int(slice_data.get("BEGIN"))
            slice_end = int(slice_data.get("END"))
            self._slice_pos.append((slice_begin, slice_end))
        self.slice_count = len(self._slice_pos)

        # Tempo
        slice_seq = loop_data.find("SLICESEQ")
        self.tempo = ieee754(slice_seq.get("TEMPO"))

        # True slices length
        ticks_per_quarter = int(slice_seq.get("TICKSPERQUARTER"))
        for sst in slice_seq.findall("SLICESEQSTEP"):
            slice_begin = int(sst.get("BEGIN"))
            slice_end = int(sst.get("END"))
            if slice_end == -1: break

            slice_length = slice_end - slice_begin + 1
            length_beats = slice_length / ticks_per_quarter
            self.slice_lengths.append(length_beats)

    def _load_slices_data(self, aud_path, volume=1.0, pan=0.0, s_swap=False):
        audio, self.sample_rate = sf.read(aud_path, dtype=np.float32, always_2d=True)

        if audio.shape[1] == 1:  # Force 2 channels
            audio = np.repeat(audio, 2, axis=1)

        if volume != 1:  # Change volume
            audio *= volume
        if pan != 0:  # Apply panning
            AudioTools.pan(audio, pan)
        if s_swap:  # Stereo swap
            audio = audio[:, ::-1]

        for slice_begin, slice_end in self._slice_pos:
            one_slice = audio[slice_begin:slice_end+1]
            self.slice_data.append(one_slice)
