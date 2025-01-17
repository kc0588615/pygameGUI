import os
from common.file_helpers import get_sounds_directory

NUM_GLASS_CLINKS = 3
GLASS_CLINKS = list(
    os.path.join(get_sounds_directory(), f"glass_clink_{i}.wav")
    for i in range(NUM_GLASS_CLINKS)
)
