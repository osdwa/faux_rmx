import numpy as np

class AudioTools:
    @staticmethod
    def place(output: np.ndarray, buffer: np.ndarray, position: int):
        position = max(0, position)  # Placeholder?

        output_length = output.shape[0]
        if position > output_length:
            return

        buffer_length = buffer.shape[0]
        placement_end = position + buffer_length
        if placement_end > output_length:
            buffer = buffer[:output_length-position]

        output[position:placement_end] += buffer

    @staticmethod
    def speed_change(data: np.ndarray, speed: int):
        k_speed = (1.05946309436) ** (speed)
        new_length = int(data.shape[0] / k_speed)

        old_x = np.arange(data.shape[0])
        new_x = np.linspace(0, data.shape[0], num=new_length)

        channels = []
        for channel in data.T:
            channels.append(
                np.interp(new_x, old_x, channel).astype(data.dtype)
            )

        return np.array(channels).T

    @staticmethod
    def fade_out(data: np.ndarray, ramp: np.ndarray):
        duration = ramp.shape[0]
        if duration <= 0:
            return

        fade_part = data[-duration:] * ramp
        data[-duration:] = fade_part.astype(data.dtype)
