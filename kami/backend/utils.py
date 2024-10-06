from io import BytesIO
from typing import Optional

from pydub import AudioSegment


def convert_bytes(
    audio_bytes: bytes,
    format_in: Optional[str] = "mp3",
    format_out: Optional[str] = "ogg",
) -> bytes:
    """
    Convert audio bytes in ogg format bytes.

    :param audio: Audio bytes.
    :param format_in: Input format.
    :param format_out: Output format.
    :return: Ogg format bytes.
    """

    audio_io = BytesIO(initial_bytes=audio_bytes)
    audio: AudioSegment = AudioSegment.from_file(file=audio_io, format=format_in)
    ogg_io = BytesIO()

    audio.export(out_f=ogg_io, format=format_out, codec="libopus")

    return ogg_io.getvalue()
