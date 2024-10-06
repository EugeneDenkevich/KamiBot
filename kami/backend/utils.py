from io import BytesIO
from typing import Optional

from pydub import AudioSegment


def convert_bytes_to(audio_bytes: bytes, format: Optional[str] = "ogg") -> bytes:
    """
    Convert audio bytes in ogg format bytes.

    :param audio: Audio bytes.
    :return: Ogg format bytes.
    """

    audio_io = BytesIO(initial_bytes=audio_bytes)
    audio: AudioSegment = AudioSegment.from_file(file=audio_io, format="mp3")
    ogg_io = BytesIO()

    audio.export(out_f=ogg_io, format=format, codec="libopus")

    return ogg_io.getvalue()
