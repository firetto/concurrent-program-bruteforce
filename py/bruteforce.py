import random
from queue import Queue
import pprint

can_commute = dict()
visited = set()

class Event:
    def __init__(self, write: bool, variable: int, 
                 thread: int, selected:bool=False):
        self.write = write
        self.variable = variable
        self.thread = thread
        self.selected = selected

    def __str__(self) -> str:
        return f"{'!' if self.selected else ''}{'w' if self.write else 'r'}({self.variable}),{self.thread}"
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.write == other.write and self.variable == other.variable \
            and self.thread == other.thread and self.selected == other.selected

    def __hash__(self):
        return hash((self.write, self.variable, self.thread, self.selected)) 

class Program:
    def __init__(self, events: list, selected1: int, selected2: int):
        self.events = tuple(events)
        self.selected1 = selected1
        self.selected2 = selected2

    def __str__(self) -> str:
        return self.events.__str__()
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash(self.events)
    
    def __eq__(self, other):
        return self.events == other.events \
            and self.selected1 == other.selected1 \
            and self.selected2 == other.selected2
        


def generate_random_program(threads: int, variables: int, length: int):
    lst = []

    for i in range(length):
        lst.append(Event(
            write=bool(random.randint(0,1)),
            variable=random.randrange(0, variables),
            thread=random.randrange(0, threads),
            selected=False
        ))

    selected1, selected2 = random.sample(range(length), 2)

    lst[selected1].selected = True
    lst[selected2].selected = True

    result = Program(lst, selected1, selected2)

    return result


def generate_every_program(threads: int, variables: int, length: int):
    lst = []

    for w in range(2): # write
            for v in range(variables): # variables
                for t in range(threads): # threads
                    for s1 in range(length-1):
                        for s2 in range(s1+1, length):    
                            program = []
                            for _ in range(length):
                                program.append(Event(
                                    write=bool(w),
                                    variable=v,
                                    thread=t,
                                    selected=False
                                ))
                            program[s1].selected = True
                            program[s2].selected = True

                            item = Program(program, s1, s2)
                            lst.append(item)

    return lst


# check whether the two selected events in a list can commute
def check_commute(program: Program, print_sequence=False):

    sequence = []

    result = check_commute_dfs(program, sequence)

    if result and print_sequence:
        pprint.pprint(sequence)

    return result


def check_commute_dfs(p: Program, sequence: list):
    if p in can_commute:
        if can_commute[p]:
            sequence.append(p)
        return can_commute[p]
    
    if p in visited:
        return False
    
    visited.add(p)

    if p.selected2 < p.selected1:
        can_commute[p] = True
        sequence.append(p)
        return True

    # first, check every consecutive pair of elements.
    for i in range(len(p.events) - 1):
        e1, e2 = p.events[i], p.events[i+1]
        # if the two events are dependent
        dependent = (e1.thread == e2.thread) or (
            (e1.variable == e2.variable) and (e1.write or e2.write)
            )
        
        if not dependent:
            # if e1.selected and e2.selected:
            #     can_commute[p] = True
            #     sequence.append(p)
            #     return True
            
            new_events = p.events[:i] + (e2,) + (e1,) + p.events[i+2:]

            if p.selected1 == i:
                new_selected1 = i+1
            elif p.selected1 == i+1:
                new_selected1 = i
            else:
                new_selected1 = p.selected1

            if p.selected2 == i:
                new_selected2 = i+1
            elif p.selected2 == i+1:
                new_selected2 = i
            else:
                new_selected2 = p.selected2

            new_p = Program(new_events, new_selected1, new_selected2)

            if check_commute_dfs(new_p, sequence):
                can_commute[p] = True
                sequence.append(p)
                # print("A")
                return True

    # now, check all possible block swaps
    # note that e will be the write corresponding to the first block of the 
    # block pair, so we ignore the last event of the program.
    for i in range(len(p.events)-1):
        e = p.events[i]

        if not e.write:
            continue

        # e is a write, and i is the start index of the first block.

        thread_set = set()
        thread_set.add(e.thread)

        # if this is false at the end of the following for loop, then we reached
        # the end of the program events without the current block ending.
        found_end_of_block = False
        cant_swap_below = False
        new_block_start_index, new_block_end_index = -1, -1 

        # find the end of this block
        for j in range(i+1, len(p.events)):
            f = p.events[j]
            
            # if f is of a different variable than e, then there is no block
            # below e that can swap with it 
            if e.variable != f.variable:
                cant_swap_below = True
                found_end_of_block = True
                break

            elif f.write:
                # here, f is the start of a new block
                # first, check if f is on a different thread than the entire
                # block
                if f.thread in thread_set:
                    cant_swap_below = True
                    break
                else:
                    found_end_of_block = True
                    new_block_start_index = j
                    break

            else:
                # here, f is a read of the same variable 
                # and therefore part of the same block as e
                thread_set.add(f.thread)

        if cant_swap_below or not found_end_of_block:
            continue

        # here, we are assuming that the event at new_block_start_index is the
        # start of a new block that is directly adjacent to the block that e is
        # in.

        found_different_variable = False
        found_end_of_block = False


        # find the end of this second block starting at new_block_start_index
        for j in range(new_block_start_index+1, len(p.events)):
            f = p.events[j]

            if found_different_variable:
                if e.variable == f.variable \
                    and not f.write:
                    cant_swap_below = True
                    break
            else:
        
                if e.variable != f.variable:
                    found_different_variable = True
                    found_end_of_block = True
                    new_block_end_index = j-1
                    continue

                elif f.write:
                    found_end_of_block = True
                    new_block_end_index = j-1
                    break

                elif f.thread in thread_set:
                    cant_swap_below = True
                    break

        if cant_swap_below:
            continue

        # otherwise, we can swap with this block!

        if not found_end_of_block:
            # this block goes until the very end of the string, so:
            new_block_end_index = len(p.events) - 1

        # # if selected1 is in block 1 and selected2 is in block2, then
        # # they can swap! so we return True.
        # if  (i <= p.selected1 <= new_block_start_index - 1) and \
        #     (new_block_start_index <= p.selected2 <= new_block_end_index):
        #     can_commute[p] = True
        #     sequence.append(p)
        #     return True
        
        # otherwise, just make the new program.
        new_events = p.events[:i] \
            + p.events[new_block_start_index:new_block_end_index+1] \
            + p.events[i:new_block_start_index] \
            + p.events[new_block_end_index+1:]
        

        # if selected1 is in the first block, 
        # move it to the same position but in the second.
        if i <= p.selected1 <= new_block_start_index - 1:
            new_selected1 = p.selected1 + new_block_end_index - new_block_start_index + 1

        # if selected1 is in the second block, 
        # move it to the same position but in the first
        elif new_block_start_index <= p.selected1 <= new_block_end_index:
            new_selected1 = p.selected1 - new_block_start_index + i
        
        else:
            new_selected1 = p.selected1
        
        # same for selected2
        if i <= p.selected2 <= new_block_start_index - 1:
            new_selected2 = p.selected2 + new_block_end_index - new_block_start_index + 1
        elif new_block_start_index <= p.selected2 <= new_block_end_index:
            new_selected2 = p.selected2 - new_block_start_index + i
        else:
            new_selected2 = p.selected2

        new_p = Program(new_events, new_selected1, new_selected2)

        # print(i, new_block_start_index, new_block_end_index, new_p)

        if check_commute_dfs(new_p, sequence):
            can_commute[p] = True
            sequence.append(p)
            # print("B", i, new_block_start_index, new_block_end_index)
            return True

    return False


# if __name__ == "__main__":

#     # threads = 3
#     # variables = 2
#     # length = 8

#     # # program = generate_random_program(threads, variables, length)
#     # # for t in program:
#     # #     print(t)
#     # # print(str(program))

#     # all_programs = generate_every_program(threads,variables,length)
#     # # print(len(all_programs))
