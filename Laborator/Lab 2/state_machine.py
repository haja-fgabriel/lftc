import re

class State:
    def __init__(self, description, is_accept_state = False):
        self.description = description
        self.is_accept_state = is_accept_state
        self.transitions = {}
    

class StateMachine:
    def __init__(self, description = ""):
        self.description = description
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

    def __parse_input(filename = None):
        f = None
        if filename: f = open(filename, "r")

        sm = StateMachine()
        states = [x.strip() for x in StateMachine.__getline(f).split(',')]
        for state in states:
            s = State(state)
            sm.states.append(s)

        sm.__input_alphabet = [x.strip() for x in StateMachine.__getline(f).split(',')]
        transition_strings = [x.strip() for x in f.readline().split(',')]
        for trans_str in transition_strings:
            letters = re.search(r"(\[)([^\[]*)(\])", trans_str).group(2).split()
            trans_states = re.sub(r"(\[)([^\[]*)(\]) ", "", trans_str).split()
            state0 = sm.__find_state(trans_states[0])
            state1 = sm.__find_state(trans_states[1])
            for letter in letters:
                state0.transitions[letter] = state1
        
        init_state = StateMachine.__getline(f).strip()
        sm.start_state = sm.__find_state(init_state)

        fin_states = [x.strip() for x in StateMachine.__getline(f).split(',')]
        for state in fin_states:
            sm.__find_state(state).is_accept_state = True
        
        if f: f.close()
        return sm

    def read_file(filename):
        return StateMachine.__parse_input(filename)
    
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
    
    def check_sequence(self, sequence):
        state = self.start_state
        for c in sequence:
            try:
                state = state.transitions[c]
            except KeyError:
                return False
        return True

    def get_longest_prefix(self, sequence):
        state = self.start_state
        result = ''
        for c in sequence:
            try:
                state = state.transitions[c]
                result += c
            except KeyError:
                break
        return result
        

