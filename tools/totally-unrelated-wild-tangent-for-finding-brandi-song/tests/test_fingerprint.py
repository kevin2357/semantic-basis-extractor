import unittest

import numpy as np

from songfinder.core import SAMPLE_RATE, compare, index_reference


class FingerprintTests(unittest.TestCase):
    def test_finds_reference_inside_long_noisy_recording(self):
        rng = np.random.default_rng(42)
        t = np.arange(SAMPLE_RATE * 12) / SAMPLE_RATE
        # A repeatable broadband bed plus changing tones approximates musical texture.
        reference = signal = rng.normal(0, .08, len(t)).astype(np.float32)
        for start, freq in [(0, 311), (2, 523), (4, 877), (6, 659), (8, 1047), (10, 433)]:
            mask = (t >= start) & (t < start + 1.6)
            signal[mask] += np.sin(2 * np.pi * freq * t[mask]).astype(np.float32)
        candidate = rng.normal(0, .00001, SAMPLE_RATE * 40).astype(np.float32)
        # Align to an analysis hop here; a separate test below exercises codec drift.
        insertion = 360 * 512
        candidate[insertion:insertion + len(reference)] += reference
        result = compare(index_reference(reference), candidate)
        self.assertGreater(result.unique_hashes, 10)
        self.assertAlmostEqual(result.offset_seconds, insertion / SAMPLE_RATE, delta=.15)


if __name__ == "__main__":
    unittest.main()
