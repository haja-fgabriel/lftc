class State:
    def __init__(self, description, is_accept_state, transitions):
        self.__description = description
        self.__is_accept_state = is_accept_state
        self.__transitions = transitions
        pass

class StateMachine:
    def __init__(self, description = "", start_state, states):
        self.__description = description
        self.__start_state = start_state
        self.__states = states
        pass