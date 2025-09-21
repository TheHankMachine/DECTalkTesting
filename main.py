import Generator
import Quantizer
import Analyser
import Phonemes
from Analyser import analyse
from LocalTypes import *


source_notes = [
       Note(duration=196.078, pitch=1, phoneme="_"),
       Note(duration=196.078, pitch=20, phoneme="dear"),
       Note(duration=196.078, pitch=24, phoneme="in"),
       Note(duration=196.078, pitch=27, phoneme="spir"),
       Note(duration=196.078, pitch=32, phoneme="a"),
       Note(duration=196.078, pitch=27, phoneme="tion"),
       Note(duration=196.078, pitch=24, phoneme="i'm"),
       Note(duration=196.078, pitch=20, phoneme="the"),
       Note(duration=196.078, pitch=22, phoneme="fool"),
       Note(duration=196.078, pitch=22, phoneme="in"),
       Note(duration=196.078, pitch=22, phoneme="your"),
       Note(duration=392.156, pitch=24, phoneme="wake"),
       Note(duration=196.078, pitch=1, phoneme="_"),
       Note(duration=196.078, pitch=19, phoneme="you"),
       Note(duration=196.078, pitch=20, phoneme="for"),
       Note(duration=196.078, pitch=22, phoneme="got"),
       Note(duration=392.156, pitch=22, phoneme="a"),
       Note(duration=196.078, pitch=20, phoneme="bout"),
       Note(duration=392.156, pitch=1, phoneme="_"),
       Note(duration=196.078, pitch=19, phoneme="my"),
       Note(duration=392.156, pitch=20, phoneme="luc"),
       Note(duration=392.156, pitch=20, phoneme="ky"),
       Note(duration=196.078, pitch=8, phoneme="break"),
] * 2

lyrics = "_ dear inspiration I'm the fool in your wake _ you forgot about _ my lucky break".split(" ") * 2

notes = Generator.generate_from_lyrics(source_notes, lyrics, Phonemes.fixed_plosive_proportional_distributor)

Analyser.analyse(notes, Quantizer.reactive_error_quantizer, beats=source_notes)

