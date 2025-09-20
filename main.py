import Generator
import Quantizer
import Analyser
import Phonemes
from Analyser import analyse
from LocalTypes import *


source_notes = [
       Note(duration=500, phoneme="", pitch=30), Note(duration=500, phoneme="", pitch=30),
       Note(duration=500, phoneme="", pitch=1), Note(duration=500, phoneme="", pitch=1)
] * 10
lyrics = ["bum", "_"] * 20

notes = Generator.generate_from_lyrics(source_notes, lyrics, Phonemes.fixed_plosive_proportional_distributor)

Analyser.analyse(notes, Quantizer.reactive_error_quantizer, beats=source_notes)

