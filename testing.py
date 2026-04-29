import numpy as np
import soundfile as sf
from collections import deque

from _config import *
from c_rand import CRandom
from chaos_track import ChaosTrack
from audio_tools import AudioTools
from load_sage_rx2 import LoopSliceSeq


class SegmentInfo:
    index = 0
    speed = 0
    is_reversed = False
    timing_shift = 0

    mark_pattern = False
    mark_repeat = False
    mark_pitch = False

    def __repr__(self):
        result = [""] * 7

        result[0] = f"Segment [idx={self.index}"
        if self.mark_pattern: result[1] = ", pattern"
        if self.mark_repeat: result[2] = ", repeat"
        if self.is_reversed: result[3] = ", reverse"
        if self.mark_pitch: result[4] = f", speed={self.speed}"
        if self.timing_shift != 0: result[5] = f", shift={self.timing_shift}"
        result[6] = "]"

        return "".join(result)


def get_frame_audio(seg: SegmentInfo, audio: np.ndarray, frame_length: int):
    init_length = audio.shape[0]

    # Reverse quirk
    if seg.is_reversed:
        audio = audio[:frame_length]

    # Change speed
    if seg.speed == 0:
        # We'll need an independent copy, not just link to greater array
        audio = audio.copy()
    else:
        audio = AudioTools.speed_change(audio, seg.speed)

    # Reverse + More quirky behaviour
    if seg.is_reversed:
        audio = audio[::-1]
        audio = audio[:init_length+CROSSFADE]

    # Cut to frame
    audio = audio[:frame_length+CROSSFADE]

    # Frame fade-out
    if seg.is_reversed: #Reversed segments fade out differently
        fade_out = audio.shape[0] - min(init_length, frame_length)
    else:
        fade_out = audio.shape[0] - frame_length
    if fade_out > 0:
        AudioTools.fade_out(audio, fade_out_ramp[:fade_out])

    return audio


def get_random_segment(chaos: ChaosTrack, frame_length: int):
    seg = SegmentInfo()

    # Pattern
    if chaos.pattern_chance > 0 and rng.rand_bool(chaos.pattern_chance):
        seg.index = rng.rand_int(chaos.seq.slice_count)
        seg.mark_pattern = True
    else:
        seg.index = chaos.seg_idx % chaos.seq.slice_count

        # Repeat
        if chaos.repeat_chance > 0 and rng.rand_bool(chaos.repeat_chance/2):
            seg.index = seg.index-1
            seg.mark_repeat = True

    # Reverse (Was passive increment just from reverse?)
    if rng.rand_bool(chaos.reverse_chance):
        seg.is_reversed = True

    # Speed variant
    if chaos.speed_chance > 0 and rng.rand_bool(chaos.speed_chance):
        rang = int(rng.rand_float() * 24 * chaos.speed_range + 0.5)
        if not rng.rand_bool(chaos.speed_down_up): rang *= -1

        seg.speed = chaos.speed_main + rang
        seg.speed = max(-24, min(seg.speed, 24)) # Limit between [-24; +24]
        seg.mark_pitch = True
    else:
        seg.speed = chaos.speed_main

    # Timing
    if chaos.timing_chance > 0 and rng.rand_bool(chaos.timing_chance):
        rang = 1

        if not rng.rand_bool(chaos.timing_rush_drag): rang *= -1
        rang*=round(rng.rand_int(48) * chaos.timing_range)

        seg.timing_shift = int(frame_length * rang / 420)

    return seg


def tick_to_samp(tick: int, tpq: int):
    result = (tick / tpq) * (60 / DAW_BPM)
    return int(result * SAMPLE_RATE)


def get_frame_length(seq: LoopSliceSeq, idx: int):
    loops = idx // seq.slice_count
    idx1 = idx % seq.slice_count

    base_tick = seq.slice_start[-1] * loops
    start = tick_to_samp(base_tick + seq.slice_start[idx1], seq.tpq)
    end = tick_to_samp(base_tick + seq.slice_start[idx1+1], seq.tpq)

    return end - start


def scramble():
    rng.set_seed(SEED)
    output = np.zeros(shape=(TARGET_LENGTH, 2), dtype=np.int16)

    while True:
        # Choose track
        chaos = min(CHAOS, key=lambda c: c.position)
        seq = chaos.seq

        # Quit if generated enough
        if chaos.position >= TARGET_LENGTH:
            return output

        # Get frame length
        frame_length = get_frame_length(seq, chaos.seg_idx)

        # Generate segment and place it
        if chaos.position>=0:
            # Generating random segment parameters
            segment = get_random_segment(chaos, frame_length)

            # Disabling render removes track, but it still affects RNG
            if not chaos.disable_render:
                seg_audio = seq.slice_data[segment.index]
                seg_audio = get_frame_audio(segment, seg_audio, frame_length)

                placement_pos = chaos.position + segment.timing_shift
                AudioTools.place(output, seg_audio, placement_pos)

                log_txt = f"Track {chaos.label} at {placement_pos}: {segment}\n"
                scramble_log.append(log_txt)

        # Move index
        chaos.position += frame_length
        chaos.seg_idx += 1


rng = CRandom()
fade_out_ramp = np.linspace(1, 0, CROSSFADE)[:, np.newaxis]
scramble_log = deque()

print("Scrambling...")
scrambled = scramble()

print("Exporting...")
sf.write("test.flac", scrambled, SAMPLE_RATE)

with open("tracking.txt", "w") as f:
    for line in scramble_log:
        f.write(line)
