# Just comfortable way of storing settings etc
from load_sage_rx2 import LoopSliceSeq

class ChaosTrack:
    def __init__(self,
                 label: str,
                 data_dir: str,
                 track_name: str,
                 disable_render: bool = False,

                 pattern_chance: float = 0.0,
                 repeat_chance: float = 0.0,
                 reverse_chance: float = 0.0,

                 timing_chance: float = 0.0,
                 timing_rush_drag: float = 0.5,
                 timing_range: float = 0.5,

                 speed_main: int = 0,
                 speed_chance: float = 0.0,
                 speed_down_up: float = 0.5,
                 speed_range: float = 0.5,

                 start_idx: int = 0,
                 start_position: int = 0,
                ):

        self.label = label
        self.disable_render = disable_render

        self.pattern_chance = pattern_chance
        self.repeat_chance = repeat_chance
        self.reverse_chance = reverse_chance

        self.timing_chance = timing_chance
        self.timing_rush_drag = timing_rush_drag
        self.timing_range = timing_range

        self.speed_main = speed_main
        self.speed_chance = speed_chance
        self.speed_down_up = speed_down_up
        self.speed_range = speed_range

        self.seg_idx = start_idx
        self.position = start_position
        self.seq = LoopSliceSeq(data_dir, track_name)
