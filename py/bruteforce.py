import random
from defs import Event, Program

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
