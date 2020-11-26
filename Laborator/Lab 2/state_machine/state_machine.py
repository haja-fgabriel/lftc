import re

MAX_SEQUENCE_LENGTH = 99999999
if __name__ != "__main__":
    from utils.constants import *

class NonDeterministicError(Exception):
    pass

class State:
    def __init__(self, description, is_accept_state = False):
        self.description = description
        self.is_accept_state = is_accept_state
        self.transitions = {}
    

class StateMachine:
    def __init__(self, description = "", max_sequence_length=MAX_SEQUENCE_LENGTH):
        self.description = description
        self.__max_sequence_length = max_sequence_length
        self.start_state = None
        self.__input_alphabet = []
        self.states = []
        pass

    def __find_state(self, description):
        return next(s for s in self.states if s.description == description)

    def __getline(file = None):
        if not file:
            return input()
        return file.readline()

    def __parse_input(filename = None, max_sequence_length=MAX_SEQUENCE_LENGTH):
        f = None
        if filename: f = open(filename, "r")

        sm = StateMachine(max_sequence_length=max_sequence_length)
        if not f: print("List of states: ", end="")
        states = [x.strip() for x in StateMachine.__getline(f).split(',')]
        for state in states:
            s = State(state)
            sm.states.append(s)

        # print is shown only when providing state machine from console
        if not f: print("Input alphabet: ", end="")

        sm.__input_alphabet = [x.strip() for x in StateMachine.__getline(f).split(',')]
        # print(f"[DEBUG] Input alphabet: {sm.__input_alphabet}")

        if not f: print("Transitions: ", end="")

        transition_strings = [x.strip() for x in StateMachine.__getline(f).split(',')]
        #print(f"[DEBUG] Transition strings: {transition_strings}")
        for trans_str in transition_strings:
            letters = re.search(r"(\[)([^\[]*)(\])", trans_str).group(2).split()
            trans_states = re.sub(r"(\[)([^\[]*)(\]) ", "", trans_str).split()
            state0 = sm.__find_state(trans_states[0])
            state1 = sm.__find_state(trans_states[1])
            for letter in letters:
                if state0.transitions.get(letter):
                    raise NonDeterministicError(f"State '{state0.description}' already has transition with letter '{letter}' to '{state1.description}'")
                state0.transitions[letter] = state1
        
        if not f: print("Initial state: ", end="")
        
        init_state = StateMachine.__getline(f).strip()
        sm.start_state = sm.__find_state(init_state)

        if not f: print("Final states: ", end="")
        fin_states = [x.strip() for x in StateMachine.__getline(f).split(',')]
        # print(f"[DEBUG] Final states: {fin_states}")
        for state in fin_states:
            sm.__find_state(state).is_accept_state = True
        
        if f: f.close()
        return sm

    def read_file(filename, max_sequence_length=MAX_SEQUENCE_LENGTH):
        return StateMachine.__parse_input(filename, max_sequence_length)
    
    def read():
        return StateMachine.__parse_input()

    def get_start_state(self):
        return self.start_state.description

    def get_states(self):
        return [s.description for s in self.states]
    
    def get_alphabet(self):
        return self.__input_alphabet

    def get_transitions(self):
        result = {}
        for s in self.states:
            for t in s.transitions:
                pair = (s.description, s.transitions[t].description)
                try:
                    result[pair].append(t)
                except KeyError:
                    result[pair] = [t]
        return [(k[0], v, k[1]) for k, v in result.items()]

    def get_final_states(self):
        return [s.description for s in self.states if s.is_accept_state]
    
    def check_sequence(self, sequence, length=-1):
        state = self.start_state
        if length > 0:
            l = [x[length*i:min(length*(i+1), len(x))] for i in range(math.ceil(len(x)/length))]
        for c in sequence:
            try:
                state = state.transitions[c]
            except KeyError:
                return False
        return state.is_accept_state

    def get_longest_prefix(self, sequence, max_length=None):
        if not max_length:
            max_length = self.__max_sequence_length
        state = self.start_state
        tmp = ''
        result = '' if state.is_accept_state else None
        for c in sequence:
            if not max_length: break
            try:
                state = state.transitions[c]
                tmp += c
                if state.is_accept_state:
                    result = tmp
            except KeyError:
                break
            max_length -= 1
        return result


