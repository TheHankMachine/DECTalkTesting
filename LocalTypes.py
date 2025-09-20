from typing import TypedDict, Callable, List

class Note(TypedDict):
    pitch: int # pitch in half steps from Ab1 (C4=28, min A1=1, max E5=47))
    duration: float # duration in milliseconds
    phoneme: str # phoneme

type DurationQuantizer = Callable[[List[Note]], str]
type NoteGenerator = Callable[[], List[Note]]
type PhonemeDistributor = Callable[[float, List[str]], List[float]]

