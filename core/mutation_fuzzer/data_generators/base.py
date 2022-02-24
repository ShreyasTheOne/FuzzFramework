from random import random


class BaseGenerator:
    def _should_fuzz(self):
        """
        Based on the fuzz probability,
        decide whether to fuzz or not
        """
        rand = random()
        return random() < self.fuzz_prob
