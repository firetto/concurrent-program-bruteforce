import random
from defs import Event, Program, clear_histories
from tqdm import tqdm

# need to do this otherwise it will run into recursion errors even though it's completely fine!
import resource, sys
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**7)  

def generate_random_program(threads: int, variables: int, length: int):
    lst = []

    seen_a_write = [False for _ in range(variables)]
    for i in range(length):
        var = random.randrange(0, variables)
        lst.append(Event(
            write=True if not seen_a_write[var] else bool(random.randint(0,1)),
            variable=var,
            thread=random.randrange(0, threads),
            selected=False
        ))
        seen_a_write[var] = True

    selected1, selected2 = random.sample(range(length), 2)

    lst[selected1].selected = True
    lst[selected2].selected = True

    result = Program(lst, selected1, selected2)

    return result


# def generate_random_program_2vars_3threads(length: int):
#     lst = []

#     # assume that each program has both variables (otherwise it is trivial),
#     # and that the first event is always w(0),0

    

#     for selected1 in range(length-1):
#         first_event = Event(write=True, variable=0, thread=0, selected=(selected1 == 0))

#         for selected2 in range(selected1+1, length):
#             for first_1_pos in range(1, length - 1):
#                 for i in range(length):
                    



# def generate_every_program(threads: int, variables: int, length: int):
#     lst = []

#     for w in range(2): # write
#             for v in range(variables): # variables
#                 for t in range(threads): # threads
#                     for s1 in range(length-1):
#                         for s2 in range(s1+1, length):    
#                             program = []
#                             for _ in range(length):
#                                 program.append(Event(
#                                     write=bool(w),
#                                     variable=v,
#                                     thread=t,
#                                     selected=False
#                                 ))
#                             program[s1].selected = True
#                             program[s2].selected = True
#                             try: 
#                                 item = Program(program, s1, s2)
#                                 lst.append(item)
#                             except:
#                                 pass

#     return lst

if __name__ == "__main__":

    threads = 3
    variables = 2
    # length = 6

    for _ in tqdm(range(10000000)):

        length = 8

        clear_histories()

        program = generate_random_program(threads, variables, length)

        # print(count, length, program)

        can_commute = program.check_commute()

        program.generate_dependency_edges()
        in_dependency_graph = (program.selected1, program.selected2) in program.dependency_edges

        if can_commute == in_dependency_graph:
            print("--------------------------------------------------------")
            print(program)
            print("CAN COMMUTE:", can_commute)
            print(program.dependency_edges)

    # for length in range(12, 13):
        
        

    #         # try:
    #         #     # clear_histories()

    #         #     # program = generate_random_program(threads, variables, length)

    #         #     # can_commute = program.check_commute()

    #         #     # program.generate_dependency_edges()
    #         #     # in_dependency_graph = (program.selected1, program.selected2) in program.dependency_edges

    #         #     # if can_commute == in_dependency_graph:
    #         #     #     print("--------------------------------------------------------")
    #         #     #     print("FOUND!")
    #         #     #     print(program)
    #         #     #     print("CAN COMMUTE:", can_commute)
    #         #     #     print(program.dependency_edges)

    #         #     # count += 1

    #         # except:
    #         #     pass
    #     print(count)
    #     # for t in program:
    #     #     print(t)
    #     # print(str(program))

    # all_programs = generate_every_program(threads,variables,length)
    # print(len(all_programs))

    # for program in all_programs:
    #     print(program)
    #     can_commute = program.check_commute()

    #     program.generate_dependency_edges()
    #     in_dependency_graph = (program.selected1, program.selected2) in program.dependency_edges
    #     if can_commute == in_dependency_graph:
    #         print("--------------------------------------------------------")
    #         print("FOUND!")
    #         print(program)
    #         print("CAN COMMUTE:", can_commute)
    #         print(program.dependency_edges)