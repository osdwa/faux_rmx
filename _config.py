from chaos_track import ChaosTrack

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
