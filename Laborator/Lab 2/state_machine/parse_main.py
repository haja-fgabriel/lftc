import sys
from ui import UI
from state_machine import StateMachine

def parse_sequence(sm, sm2, sequence):
    prefix = sm2.get_longest_prefix(sequence)
    if len(prefix):
        print(f"Found constant {prefix}")
    _id = sequence[max(len(prefix)-2, 0):]
    if sm.check_sequence(_id):
        print(f"ID {_id} is accepted")
    else:
        print(f"ID {_id} is not accepted")
    pass

if __name__ == "__main__":
    sm = None
    if len(sys.argv) < 3 or sys.argv[1] in ['--help', '-h']:
        exit(f"Usage: {sys.argv[0]} <dfa_filename> <dfa2_filename> sequence")
    sm = StateMachine.read_file(sys.argv[1])
    sm2 = StateMachine.read_file(sys.argv[2])
    parse_sequence(sm, sm2, sys.argv[3])
    

