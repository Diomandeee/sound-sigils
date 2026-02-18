"""
Sound Sigils — Audio representations of N'Ko sigils.

Each N'Ko character is mapped to a distinctive sonic signature that
reflects its semantic meaning through tone, rhythm, and spatial audio.

Usage::

    from sound_sigils import SoundSigils

    ss = SoundSigils()
    ss.play("ߛ")                    # play by character
    ss.play("stabilization")        # play by name
    ss.export("ߛ", "out.wav")      # export to WAV
    data = ss.generate("ߛ")         # get raw WAV bytes
"""

from sound_sigils.engine import SoundSigils
from sound_sigils.models import SigilSound, SigilDefinition

__version__ = "1.0.0"
__all__ = ["SoundSigils", "SigilSound", "SigilDefinition", "__version__"]
