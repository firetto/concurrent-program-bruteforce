import unittest
from bruteforce import *
from defs import *

class TestProgramCommute(unittest.TestCase):
    def test_1(self):
        can_commute.clear()
        visited.clear()
        e1 = Event(write=True, variable=0, thread=0, selected=True)
        e2 = Event(write=True, variable=0, thread=0, selected=True)
        program = Program([e1, e2], 0, 1)
        self.assertEqual(False, program.check_commute(),"FAIL!")

    def test_2(self):
        can_commute.clear()
        visited.clear()
        e1 = Event(write=True, variable=0, thread=0, selected=True)
        e2 = Event(write=True, variable=0, thread=1, selected=True)
        program = Program([e1, e2], 0, 1)
        self.assertEqual(True, program.check_commute(), "FAIL!")

    def test_3(self):
        can_commute.clear()
        visited.clear()
        e1 = Event(write=True, variable=0, thread=0, selected=True)
        e2 = Event(write=True, variable=1, thread=1, selected=True)
        program = Program([e1, e2], 0, 1)
        self.assertEqual(True, program.check_commute(), "FAIL!")

    def test_4(self):
        can_commute.clear()
        visited.clear()
        e1 = Event(write=True, variable=0, thread=0, selected=True)
        e2 = Event(write=False, variable=0, thread=1, selected=True)
        program = Program([e1, e2], 0, 1)
        self.assertEqual(False, program.check_commute(), "FAIL!")

    def test_5(self):
        can_commute.clear()
        visited.clear()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=True, variable=1, thread=1, selected=False),
            Event(write=False, variable=1, thread=0, selected=False),
            Event(write=True, variable=0, thread=2, selected=False),
            Event(write=False, variable=0, thread=1, selected=False),
            Event(write=True, variable=1, thread=2, selected=True)
        ]
        program = Program(events, 0, 5)
        self.assertEqual(False, program.check_commute(), "FAIL!")

    def test_6(self):
        can_commute.clear()
        visited.clear()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=True, variable=1, thread=1, selected=False),
            Event(write=False, variable=1, thread=0, selected=False),
            Event(write=True, variable=0, thread=2, selected=False),
            Event(write=False, variable=0, thread=1, selected=False),
            Event(write=True, variable=2, thread=2, selected=True)
        ]
        program = Program(events, 0, 5)
        self.assertEqual(True, program.check_commute(), "FAIL!")

    def test_7(self):
        can_commute.clear()
        visited.clear()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=True, variable=1, thread=1, selected=False),
            Event(write=False, variable=1, thread=0, selected=False),
            Event(write=True, variable=0, thread=3, selected=False),
            Event(write=False, variable=0, thread=2, selected=False),
            Event(write=True, variable=1, thread=2, selected=True)
        ]
        program = Program(events, 0, 5)
        self.assertEqual(True, program.check_commute(), "FAIL!")

    def test_8(self):
        can_commute.clear()
        visited.clear()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=False, variable=0, thread=1, selected=False),
            Event(write=True, variable=0, thread=2, selected=True),
            Event(write=False, variable=0, thread=1, selected=False),
        ]
        program = Program(events, 0, 2)
        self.assertEqual(False, program.check_commute(), "FAIL!")

    def test_9(self):
        can_commute.clear()
        visited.clear()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=False, variable=0, thread=1, selected=False),
            Event(write=True, variable=0, thread=2, selected=True),
        ]
        program = Program(events, 0, 2)
        self.assertEqual(True, program.check_commute(), "FAIL!")

    def test_10(self):
        can_commute.clear()
        visited.clear()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=False, variable=0, thread=1, selected=False),
            Event(write=True, variable=0, thread=2, selected=True),
            Event(write=True, variable=1, thread=0, selected=False),
            Event(write=False, variable=0, thread=0, selected=False),
        ]
        program = Program(events, 0, 2)
        self.assertEqual(False, program.check_commute(), "FAIL!")

    def test_11(self):
        can_commute.clear()
        visited.clear()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=False, variable=0, thread=1, selected=False),
            Event(write=True, variable=0, thread=2, selected=True),
            Event(write=True, variable=1, thread=0, selected=False),
        ]
        program = Program(events, 0, 2)
        self.assertEqual(True, program.check_commute(), "FAIL!")

    def test_12(self):
        can_commute.clear()
        visited.clear()
        events1 = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=True, variable=1, thread=1, selected=False),
            Event(write=False, variable=0, thread=0, selected=False),
            Event(write=True, variable=0, thread=1, selected=True),
        ]
        program1 = Program(events1, 0, 3)
        self.assertEqual(False, program1.check_commute(), "FAIL!")
    
    def test_13(self):
        can_commute.clear()
        visited.clear()
        events = [
            Event(write=True, variable=1, thread=1, selected=False),
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=False, variable=0, thread=0, selected=False),
            Event(write=True, variable=0, thread=1, selected=True),
        ]
        program = Program(events, 1, 3)
        self.assertEqual(True, program.check_commute(), "FAIL!")

if __name__ == "__main__":

    unittest.main() 