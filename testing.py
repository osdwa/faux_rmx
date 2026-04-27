import numpy as np
import soundfile as sf

from c_rand import CRandom
from chaos_track import ChaosTrack
from audio_tools import AudioTools

### Parameters

SEED = 1606282789 #2339899427 # 3594052623
TRACKSTART=16394014 #18004836
DAW_BPM = 66
CROSSFADE = 1071  # Exact value, afaik
SAMPLE_RATE = 44100  # Make sure all track have the same SR!
TARGET_LENGTH = 3 * 60 * SAMPLE_RATE

CHAOS = [
    ChaosTrack(
        label="FMS",
        data_dir=r"C:\Users\DELL\Documents\SAGE\SAGE Libraries\User Libraries\Converted REX Files\fms",
        track_name="07 False memory syndrome",
        disable_render=False,

        pattern_chance=34./58.,
        repeat_chance=10./58.,
        reverse_chance=31./58.,

        timing_chance=0,
        timing_rush_drag=0,
        timing_range=0,

        speed_main=-6,
        speed_chance=0,
        speed_down_up=0,
        speed_range=0,

        start_idx=0,
        start_position=15354848 - TRACKSTART
    ),

    ChaosTrack(
        label="Contemplation",
        data_dir=r"C:\Users\DELL\Documents\SAGE\SAGE Libraries\User Libraries\Converted REX Files\h1 l3",
        track_name="13 Contemplation",
        disable_render=False,

        pattern_chance=30./58.,
        repeat_chance=11./58.,
        reverse_chance=32./58.,

        timing_chance=0,
        timing_rush_drag=0,
        timing_range=0,

        speed_main=-8,
        speed_chance=0,
        speed_down_up=0,
        speed_range=0,

        start_idx=0,
        start_position=11827009 - TRACKSTART
    ),
     ChaosTrack(
        label="F8",
        data_dir=r"C:\Users\DELL\Documents\SAGE\SAGE Libraries\User Libraries\Converted REX Files\h1 l3",
        track_name="F8 - Mournful cameraderie",
        disable_render=False,

        pattern_chance=55./58.,
        repeat_chance=0./58.,
        reverse_chance=29./58.,

        timing_chance=1,
        timing_rush_drag=.5,
        timing_range=.2,

        speed_main=-8,
        speed_chance=0,
        speed_down_up=0,
        speed_range=0,

        start_idx=0,
        start_position=160362 - TRACKSTART
    ),
       ChaosTrack(
        label="DSFD 3",
        data_dir=r"C:\Users\DELL\Documents\SAGE\SAGE Libraries\User Libraries\Converted REX Files\h1 l3",
        track_name="DSFD3",
        disable_render=False,

        pattern_chance=32./58.,
        repeat_chance=0./58.,
        reverse_chance=17./58.,

        timing_chance=0,
        timing_rush_drag=0,
        timing_range=0,

        speed_main=-9,
        speed_chance=0,
        speed_down_up=0,
        speed_range=0,

        start_idx=0,
        start_position=13470645 - TRACKSTART
    )
]

###

class SegmentInfo:
    index = 0
    speed = 0
    is_reversed = False
    timing_shift = 0

    mark_pattern = False
    mark_repeat = False
    mark_pitch = False

    def as_string(self):
        text = f"Segment [idx={self.index}"
        if self.mark_pattern: text += ", pattern"
        if self.mark_repeat: text += ", repeat"
        if self.mark_pitch: text += f", speed={self.speed}"
        if self.timing_shift != 0: text += f", shift={self.timing_shift}"
        if self.is_reversed: text += ", reverse"
        text += "]"

        return text


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

    # Passive increment
    rng.roll()
     # Reverse
    if rng.rand_bool(chaos.reverse_chance, roll=False):
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
        
      
        rang*=int(rng.rand_float() * 40 * chaos.timing_range + 0.5)
        if not rng.rand_bool(chaos.timing_rush_drag): rang *= -1
        seg.timing_shift = int(frame_length * rang / 200)  # 200 = 2 [from snapping] * 100 [from %]

   

    return seg


def scramble():
    rng.set_seed(SEED)

    while True:
        # Choose track
        chaos = min(CHAOS, key=lambda c: c.position)
        seq = chaos.seq

        # Quit if generated enough
        if chaos.position >= TARGET_LENGTH:
            return

        # Get frame length
        slice_length = seq.slice_lengths[chaos.seg_idx % seq.slice_count]
        frame_length = round(round(slice_length * SAMPLE_RATE) / DAW_BPM)

        # Generating random segment parameters

        if chaos.position>=0:
          segment = get_random_segment(chaos, frame_length)

        # Generate segment and place it
          if not chaos.disable_render:
            # Disabling render removes track, but it still affects RNG

              seg_audio = seq.slice_data[segment.index]
              seg_audio = get_frame_audio(segment, seg_audio, frame_length)

              placement_pos = chaos.position + segment.timing_shift
              AudioTools.place(output, seg_audio, placement_pos)

              print("Track", chaos.label, "at", placement_pos, ":", segment.as_string())

        # Move index
        chaos.position += frame_length
        chaos.seg_idx += 1


rng = CRandom()
output = np.zeros(shape=(TARGET_LENGTH, 2), dtype=np.int16)
fade_out_ramp = np.linspace(1, 0, CROSSFADE)[:, np.newaxis]

scramble()
print("Exporting...")
sf.write("test.flac", output, SAMPLE_RATE)
