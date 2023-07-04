import unittest
from bruteforce import *

class TestProgramCommute(unittest.TestCase):
    def test_1(self):
        e1 = Event(write=True, variable=0, thread=0, selected=True)
        e2 = Event(write=True, variable=0, thread=0, selected=True)
        program = Program([e1, e2], 0, 1)
        self.assertEqual(False, check_commute(program),"FAIL!")

    def test_2(self):
        e1 = Event(write=True, variable=0, thread=0, selected=True)
        e2 = Event(write=True, variable=0, thread=1, selected=True)
        program = Program([e1, e2], 0, 1)
        self.assertEqual(True, check_commute(program), "FAIL!")

    def test_3(self):
        e1 = Event(write=True, variable=0, thread=0, selected=True)
        e2 = Event(write=True, variable=1, thread=1, selected=True)
        program = Program([e1, e2], 0, 1)
        self.assertEqual(True, check_commute(program), "FAIL!")

    def test_4(self):
        e1 = Event(write=True, variable=0, thread=0, selected=True)
        e2 = Event(write=False, variable=0, thread=1, selected=True)
        program = Program([e1, e2], 0, 1)
        self.assertEqual(False, check_commute(program), "FAIL!")

    def test_5(self):
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=True, variable=1, thread=1, selected=False),
            Event(write=False, variable=1, thread=0, selected=False),
            Event(write=True, variable=0, thread=2, selected=False),
            Event(write=False, variable=0, thread=1, selected=False),
            Event(write=True, variable=1, thread=2, selected=True)
        ]
        program = Program(events, 0, 5)
        self.assertEqual(False, check_commute(program, False), "FAIL!")

if __name__ == "__main__":

    unittest.main() 