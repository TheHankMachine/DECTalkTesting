import unittest
import random
import math

import Sequencer
from Sequencer import *

# white box testing for Sequencer
class Tests(unittest.TestCase):

    def assert_agg_lyrics_match(self, input_lyrics: list[str], output_lyrics: list[str]):
        events = [create_event(1, 100, lyric) for lyric in input_lyrics]

        proc_events = pre_process_phonemic_events(events)
        aggregate_hyphenated_lyrics(proc_events)

        self.assertListEqual(output_lyrics, [event["lyric"] for event in proc_events])


    def assert_spread_lyrics_match(self, input_lyrics: list[str], output_lyrics: list[str]):
        events = [create_event(1, 100, lyric) for lyric in input_lyrics]

        proc_events = pre_process_phonemic_events(events)
        aggregate_hyphenated_lyrics(proc_events)
        convert_to_phonemic_lyrics(proc_events)
        spread_lyrics(proc_events)

        self.assertEqual(output_lyrics, [event["lyric"] for event in proc_events])


    def test_agg_lyrics(self):
        # basic
        self.assert_agg_lyrics_match(["stop"], ["STOP"])
        self.assert_agg_lyrics_match(["stop", "_"], ["STOP", "_"])

        # multiple syllables
        self.assert_agg_lyrics_match(["mis-", "ter"], ["MISTER", "|"])

        # multiple notes per syllable
        self.assert_agg_lyrics_match(["mis-", "", "ter"], ["MISTER", "+", "|"])
        self.assert_agg_lyrics_match(["mis-", "", "ter", ""], ["MISTER", "+", "|", "+"])
        self.assert_agg_lyrics_match(["mis-", "_", "ter"], ["MISTER", "_", "|"])
        self.assert_agg_lyrics_match(["mis-", "_", "", "ter"], ["MISTER", "_", "+", "|"])

        # phonemic input
        self.assert_agg_lyrics_match(["[SAEF-", "TIY]"], ["SAEF", "TIY"])

        # cutting off multi-syllable word
        self.assert_agg_lyrics_match(["mister", "stop"], ["MISTER", "STOP"])

        # self.assert_agg_lyrics_match(["", "stop"], ["_", "STOP"])


    def test_spread_lyrics(self):
        # basic
        self.assert_spread_lyrics_match(["stop"], ["S T AA P"])

        # spreading one syllable to multiple notes
        self.assert_spread_lyrics_match(["stop", ""], ["S T AA", "AA P"])
        self.assert_spread_lyrics_match(["s-", "top"], ["S T AA", "AA P"])

        # cutting off multi-syllable word
        self.assert_spread_lyrics_match(["mister", "stop"], ["M IH S T", "S T AA P"])

        # phonemic input
        self.assert_spread_lyrics_match(["[SAEF-", "TIY]"], ["S AE F", "T IY"])
        self.assert_spread_lyrics_match(["[SAEF-", "", "TIY]"], ["S AE", "AE F", "T IY"])

        # unknown word
        self.assert_spread_lyrics_match(["kjh"], [DEFAULT_PHONEME])
        self.assert_spread_lyrics_match(["kjh-", "aah"], [DEFAULT_PHONEME, DEFAULT_PHONEME])

        # invalid phonemic
        self.assert_spread_lyrics_match(["[qqq]"], [DEFAULT_PHONEME])

        #
        self.assert_agg_lyrics_match(["", "stop"], ["_", "S T AA P"])


    def test_monkey_multiple(self):
        for _ in range(500):
            self.monkey_test()

    # random inputs to try to crash
    def monkey_test(self):
        word_list = list(CMUDict.keys())

        num_lyrics = random.randint(10, 20)
        lyrics = []
        for _ in range(num_lyrics):

            if random.random() > 0.75:
                lyrics += ["_"]
                continue

            lyric = random.choice(word_list)
            num_syllables = CMUDict[lyric].count(" | ") + 1

            syllable_splits = num_syllables - 1 + math.floor(random.random() * 1.5 - 0.25)
            for _ in range(syllable_splits):
                l = random.randrange(0, len(lyric))
                lyrics += [lyric[:l] + "-" ]
                lyric = lyric[l:]

            lyrics += [lyric]

        input = [
            create_event(
                random.randint(0, 40),
                random.randint(0, 1_000),
                lyric
            ) for lyric in lyrics
        ]

        try:
            process(input)
        except:
            print("failed on input ")
            print(input)

            self.assertTrue(False)
