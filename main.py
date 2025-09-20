import NoteGenerators
import Quantizers
import Analyser


notes = NoteGenerators.pulse_generator(500, 100)
Analyser.analyse(notes, Quantizers.reactive_error_quantizer)

