import Generator
import Quantizer
import Analyser
import Phonemes
from LocalTypes import *

repeat = 1
# lyrics = "hat _"
# syllable_split_lyrics = "hat _"
lyrics = "mister sand man _ I'm so alone _ don't have nobody _ to call my own"
syllable_split_lyrics = "mis ter sand man _ I'm so a lone _ don't have no bo dy _ to call my own"

lyrics = lyrics.split(" ") * repeat
syllable_split_lyrics = syllable_split_lyrics.split(" ") * repeat

source_notes = [Note(duration=400, phoneme=lyric, pitch=25) for lyric in syllable_split_lyrics]

notes = Generator.generate_from_lyrics(source_notes, lyrics, Phonemes.fixed_plosive_proportional_distributor)

Analyser.analyse(notes, Quantizer.naive_quantizer, source_notes)
#

# notes = Generator.generate_phoneme_pulses([400], 50, ["ah", "_"])
# Analyser.analyse(notes, Quantizer.reactive_error_quantizer)
