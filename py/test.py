import unittest
from bruteforce import *
from defs import *

class TestProgramCommute(unittest.TestCase):
    def test_1(self):
        clear_histories()
        e1 = Event(write=True, variable=0, thread=0, selected=True)
        e2 = Event(write=True, variable=0, thread=0, selected=True)
        program = Program([e1, e2], 0, 1)
        program.generate_dependency_edges()
        self.assertEqual(False, program.check_commute(),"FAIL!")
        self.assertEqual(True, (0, 1) in program.dependency_edges,"FAIL!")

    def test_2(self):
        clear_histories()
        e1 = Event(write=True, variable=0, thread=0, selected=True)
        e2 = Event(write=True, variable=0, thread=1, selected=True)
        program = Program([e1, e2], 0, 1)
        program.generate_dependency_edges()
        self.assertEqual(True, program.check_commute(), "FAIL!")
        self.assertEqual(False, (0, 1) in program.dependency_edges, "FAIL!")

    def test_3(self):
        clear_histories()
        e1 = Event(write=True, variable=0, thread=0, selected=True)
        e2 = Event(write=True, variable=1, thread=1, selected=True)
        program = Program([e1, e2], 0, 1)
        program.generate_dependency_edges()
        self.assertEqual(True, program.check_commute(), "FAIL!")
        self.assertEqual(False, (0, 1) in program.dependency_edges, "FAIL!")

    def test_4(self):
        clear_histories()
        e1 = Event(write=True, variable=0, thread=0, selected=True)
        e2 = Event(write=False, variable=0, thread=1, selected=True)
        program = Program([e1, e2], 0, 1)
        program.generate_dependency_edges()
        self.assertEqual(False, program.check_commute(), "FAIL!")
        self.assertEqual(True, (0, 1) in program.dependency_edges, "FAIL!")

    def test_5(self):
        clear_histories()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=True, variable=1, thread=1, selected=False),
            Event(write=False, variable=1, thread=0, selected=False),
            Event(write=True, variable=0, thread=2, selected=False),
            Event(write=False, variable=0, thread=1, selected=False),
            Event(write=True, variable=1, thread=2, selected=True)
        ]
        program = Program(events, 0, 5)
        program.generate_dependency_edges()
        self.assertEqual(False, program.check_commute(), "FAIL!")
        self.assertEqual(True, (0, 5) in program.dependency_edges, "FAIL!")

    def test_6(self):
        clear_histories()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=True, variable=1, thread=1, selected=False),
            Event(write=False, variable=1, thread=0, selected=False),
            Event(write=True, variable=0, thread=2, selected=False),
            Event(write=False, variable=0, thread=1, selected=False),
            Event(write=True, variable=2, thread=2, selected=True)
        ]
        program = Program(events, 0, 5)
        program.generate_dependency_edges()
        self.assertEqual(True, program.check_commute(), "FAIL!")
        self.assertEqual(False, (0, 5) in program.dependency_edges, "FAIL!")

    def test_7(self):
        clear_histories()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=True, variable=1, thread=1, selected=False),
            Event(write=False, variable=1, thread=0, selected=False),
            Event(write=True, variable=0, thread=3, selected=False),
            Event(write=False, variable=0, thread=2, selected=False),
            Event(write=True, variable=1, thread=2, selected=True)
        ]
        program = Program(events, 0, 5)
        program.generate_dependency_edges()
        self.assertEqual(True, program.check_commute(), "FAIL!")
        self.assertEqual(False, (0, 5) in program.dependency_edges, "FAIL!")

    def test_8(self):
        clear_histories()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=False, variable=0, thread=1, selected=False),
            Event(write=True, variable=0, thread=2, selected=True),
            Event(write=False, variable=0, thread=1, selected=False),
        ]
        program = Program(events, 0, 2)
        program.generate_dependency_edges()
        self.assertEqual(False, program.check_commute(), "FAIL!")
        self.assertEqual(True, (0, 2) in program.dependency_edges, "FAIL!")

    def test_9(self):
        clear_histories()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=False, variable=0, thread=1, selected=False),
            Event(write=True, variable=0, thread=2, selected=True),
        ]
        program = Program(events, 0, 2)
        program.generate_dependency_edges()
        self.assertEqual(True, program.check_commute(), "FAIL!")
        self.assertEqual(False, (0, 2) in program.dependency_edges, "FAIL!")

    def test_10(self):
        clear_histories()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=False, variable=0, thread=1, selected=False),
            Event(write=True, variable=0, thread=2, selected=True),
            Event(write=True, variable=1, thread=0, selected=False),
            Event(write=False, variable=0, thread=0, selected=False),
        ]
        program = Program(events, 0, 2)
        program.generate_dependency_edges()
        self.assertEqual(False, program.check_commute(), "FAIL!")
        self.assertEqual(True, (0, 2) in program.dependency_edges, "FAIL!")

    def test_11(self):
        clear_histories()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=False, variable=0, thread=1, selected=False),
            Event(write=True, variable=0, thread=2, selected=True),
            Event(write=True, variable=1, thread=0, selected=False),
        ]
        program = Program(events, 0, 2)
        program.generate_dependency_edges()
        self.assertEqual(True, program.check_commute(), "FAIL!")
        self.assertEqual(False, (0, 2) in program.dependency_edges, "FAIL!")

    def test_12(self):
        clear_histories()
        events = [
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=True, variable=1, thread=1, selected=False),
            Event(write=False, variable=0, thread=0, selected=False),
            Event(write=True, variable=0, thread=1, selected=True),
        ]
        program = Program(events, 0, 3)
        program.generate_dependency_edges()
        self.assertEqual(False, program.check_commute(), "FAIL!")
        self.assertEqual(True, (0, 3) in program.dependency_edges, "FAIL!")
    
    def test_13(self):
        clear_histories()
        events = [
            Event(write=True, variable=1, thread=1, selected=False),
            Event(write=True, variable=0, thread=0, selected=True),
            Event(write=False, variable=0, thread=0, selected=False),
            Event(write=True, variable=0, thread=1, selected=True),
        ]
        program = Program(events, 1, 3)
        program.generate_dependency_edges()
        self.assertEqual(True, program.check_commute(), "FAIL!")
        self.assertEqual(False, (1, 3) in program.dependency_edges, "FAIL!") 

    def test_14(self):
        clear_histories()
        events = [
            Event(write=True, variable=1, thread=2, selected=False),
            Event(write=False, variable=1, thread=2, selected=True),
            Event(write=True, variable=1, thread=1, selected=False),
            Event(write=True, variable=0, thread=1, selected=True),
            Event(write=True, variable=1, thread=1, selected=False),
            Event(write=False, variable=1, thread=1, selected=False),
        ]
        program = Program(events, 1, 3)
        program.generate_dependency_edges()
        self.assertEqual(True, program.check_commute(), "FAIL!")
        self.assertEqual(False, (1, 3) in program.dependency_edges, "FAIL!") 

    def test_15(self):
        clear_histories()
        events = [
            Event(write=True, variable=1, thread=0, selected=False),
            Event(write=True, variable=1, thread=2, selected=True),
            Event(write=True, variable=0, thread=0, selected=False),
            Event(write=True, variable=1, thread=0, selected=True),
            Event(write=False, variable=1, thread=0, selected=False),
            Event(write=True, variable=0, thread=2, selected=False),
        ]
        program = Program(events, 1, 3)
        program.generate_dependency_edges()
        self.assertEqual(True, program.check_commute(), "FAIL!")
        self.assertEqual(False, (1, 3) in program.dependency_edges, "FAIL!") 

if __name__ == "__main__":

    unittest.main() 