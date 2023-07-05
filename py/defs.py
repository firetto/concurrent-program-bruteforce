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

    def __init__(
            self, 
            events: list, 
            selected1: int, 
            selected2: int,
            skip_setup_blocks=False,
            event_in_block=[]
    ):
        self.events = tuple(events)
        self.selected1 = selected1
        self.selected2 = selected2
        self.rf = []
        self.blocks = set()
        self.event_in_block = event_in_block.copy()

        self.setup_rf()

        if not skip_setup_blocks:
            
            self.setup_blocks()


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
    

    def setup_rf(self):
        # for every variable, we keep track of the index of the last write for
        # that variable. This will help with the read-from ordering.
        last_write = dict()

        for i in range(len(self.events)):
            e = self.events[i]

            if e.write:
                last_write[e.variable] = i
                self.rf.append(-1) # rf should not be defined for writes!
            
            else:
                # we are assuming that there are no loose reads,
                # but let's check nevertheless!
                if e.variable not in last_write:
                    raise Exception("Loose reads!")
                
                self.rf.append(last_write[e.variable])


    def setup_blocks(self):

        # maps variable to the corresponding set of blocks. If a block
        # is in here, then if you see a read of teh same variable while
        # the block is not ongoing, then you remove it. If you see a write of
        # the same variable and there is a block in here, then add it to
        # self.blocks.
        candidate_block = dict()

        # maps variable to whether or not the current block is ongoing 
        # (i.e. the last few events have been a block)
        block_ongoing = dict()

        for i in range(len(self.events)):
            e = self.events[i]

            # if it is a write
            if e.write:
                if e.variable in candidate_block:
                    self.blocks.add(frozenset(candidate_block[e.variable]))

                candidate_block[e.variable] = {i}
                block_ongoing[e.variable] = True

            # if it is a read
            else:
                # if the block is ongoing, add to it.
                if e.variable in candidate_block and block_ongoing[e.variable]:
                    candidate_block[e.variable].add(i)

                # if the block is no longer ongoing, then the candidate
                # block is not really a block!
                elif e.variable in candidate_block:
                    candidate_block.pop(e.variable)
                    block_ongoing.pop(e.variable)

            for var in candidate_block:
                if var != e.variable:
                    block_ongoing[var] = False

        # Add all the remaining candidate blocks
        for var in candidate_block:
            self.blocks.add(frozenset(candidate_block[var]))

        # set up self.event_in_block
        for i in range(len(self.events)):
            e = self.events[i]

            in_some_block = False

            for block in self.blocks:
                if i in block:
                    in_some_block = True

            self.event_in_block.append(in_some_block)


    def check_commute(self, print_sequence=False):

        sequence = []

        result = self._check_commute_dfs(sequence)

        if result and print_sequence:
            pprint.pprint([program for program in sequence])

        return result
    

    def _check_commute_dfs(self, sequence: list):
        if self in can_commute:
            if can_commute[self]:
                sequence.append(self)
            return can_commute[self]
    
        if self in visited:
            return False
        
        visited.add(self)

        if self.selected2 < self.selected1:
            can_commute[self] = True
            sequence.append(self)
            return True

        # first, check every consecutive pair of elements.
        for i in range(len(self.events) - 1):
            e1, e2 = self.events[i], self.events[i+1]
            # if the two events are dependent
            dependent = (e1.thread == e2.thread) or (
                (e1.variable == e2.variable) and (e1.write or e2.write)
                )
            
            if not dependent:
                # if e1.selected and e2.selected:
                #     can_commute[p] = True
                #     sequence.append(p)
                #     return True
                
                new_events = self.events[:i] + (e2,) + (e1,) + self.events[i+2:]

                new_event_in_block = self.event_in_block[:i] \
                    + [self.event_in_block[i+1]] \
                    + [self.event_in_block[i]] \
                    + self.event_in_block[i+2:]

                if self.selected1 == i:
                    new_selected1 = i+1
                elif self.selected1 == i+1:
                    new_selected1 = i
                else:
                    new_selected1 = self.selected1

                if self.selected2 == i:
                    new_selected2 = i+1
                elif self.selected2 == i+1:
                    new_selected2 = i
                else:
                    new_selected2 = self.selected2

                new_p = Program(
                    new_events, 
                    new_selected1, 
                    new_selected2, 
                    skip_setup_blocks=True, 
                    event_in_block=new_event_in_block.copy()
                )

                if new_p._check_commute_dfs(sequence):
                    can_commute[self] = True
                    sequence.append(self)
                    # print("A")
                    return True

        # now, check all possible block swaps
        # note that e will be the write corresponding to the first block of the 
        # block pair, so we ignore the last event of the program.
        for i in range(len(self.events)-1):
            e = self.events[i]

            if not e.write or not self.event_in_block[i]:
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
            for j in range(i+1, len(self.events)):
                f = self.events[j]
                
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
                    if f.thread in thread_set or not self.event_in_block[j]:
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
            for j in range(new_block_start_index+1, len(self.events)):
                f = self.events[j]

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
                new_block_end_index = len(self.events) - 1

            # # if selected1 is in block 1 and selected2 is in block2, then
            # # they can swap! so we return True.
            # if  (i <= p.selected1 <= new_block_start_index - 1) and \
            #     (new_block_start_index <= p.selected2 <= new_block_end_index):
            #     can_commute[p] = True
            #     sequence.append(p)
            #     return True
            
            # otherwise, just make the new program.
            new_events = self.events[:i] \
                + self.events[new_block_start_index:new_block_end_index+1] \
                + self.events[i:new_block_start_index] \
                + self.events[new_block_end_index+1:]
            
            new_event_in_block = self.event_in_block[:i] \
                + self.event_in_block[new_block_start_index:new_block_end_index+1] \
                + self.event_in_block[i:new_block_start_index] \
                + self.event_in_block[new_block_end_index+1:]
            

            # if selected1 is in the first block, 
            # move it to the same position but in the second.
            if i <= self.selected1 <= new_block_start_index - 1:
                new_selected1 = self.selected1 + new_block_end_index - new_block_start_index + 1

            # if selected1 is in the second block, 
            # move it to the same position but in the first
            elif new_block_start_index <= self.selected1 <= new_block_end_index:
                new_selected1 = self.selected1 - new_block_start_index + i
            
            else:
                new_selected1 = self.selected1
            
            # same for selected2
            if i <= self.selected2 <= new_block_start_index - 1:
                new_selected2 = self.selected2 + new_block_end_index - new_block_start_index + 1
            elif new_block_start_index <= self.selected2 <= new_block_end_index:
                new_selected2 = self.selected2 - new_block_start_index + i
            else:
                new_selected2 = self.selected2

            new_p = Program(
                new_events, 
                new_selected1, 
                new_selected2,
                skip_setup_blocks=True,
                event_in_block=new_event_in_block.copy()
            )

            # print(i, new_block_start_index, new_block_end_index, new_p)

            if new_p._check_commute_dfs(sequence):
                can_commute[self] = True
                sequence.append(self)
                # print("B", i, new_block_start_index, new_block_end_index)
                return True

        return False
    

    def generate_dependency_edges(self):

        # this will be a map of 2-tuples of indices of dependent events.
        edges = set()

