import sys
from ui import UI
from state_machine import StateMachine

if __name__ == "__main__":
    sm = None
    if len(sys.argv) < 2:
        sm = StateMachine.read()
    else:
        if sys.argv[1] in ['--help', '-h']:
            exit(f"Usage: {sys.argv[0]} [<dfa_filename>]")
        sm = StateMachine.read_file(sys.argv[1])

    UI(sm).run()
