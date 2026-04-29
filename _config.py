from chaos_track import ChaosTrack

SEED = 3594052623
DAW_BPM = 99
CROSSFADE = 1071
SAMPLE_RATE = 44100
TARGET_LENGTH = 30 * 60 * SAMPLE_RATE

CHAOS = [
    ChaosTrack(
        label="1",
        data_dir=r"C:\ProgramData\Spectrasonics\SAGE\SAGE Libraries\User Libraries\Converted REX Files\spikes",
        track_name="spikes",
        disable_render=False,

        pattern_chance=0,
        repeat_chance=0,
        reverse_chance=0,

        timing_chance=0,
        timing_rush_drag=0,
        timing_range=0,

        speed_main=0,
        speed_chance=0,
        speed_down_up=0,
        speed_range=.5,

        start_idx=0,
        start_position=0
    )
]
