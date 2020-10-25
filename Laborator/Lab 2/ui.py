from colorama import *

class UI:
    def __init__(self, state_machine):
        self.__state_machine = state_machine
        
    def __print_all_states(self):
        print(Fore.BLUE + str(self.__state_machine.get_states()))

    def __print_alphabet(self):
        print(Fore.BLUE + str(self.__state_machine.get_alphabet()))

    def __print_transitions(self):
        for trans in self.__state_machine.get_transitions():
            print(Fore.YELLOW + "     State: " + Fore.BLUE + trans[0])
            print(Fore.YELLOW + "   Letters: " + Fore.BLUE + str(trans[1]))
            print(Fore.YELLOW + "Next state: " + Fore.BLUE + trans[2] + '\n')
    
    def __print_final_states(self):
        print(Fore.BLUE + str(self.__state_machine.get_final_states()))
    
    def __check_acceptance(self, sequence):
        result = self.__state_machine.check_sequence(sequence)
        print(Fore.BLUE + f"'{sequence}'" + Fore.YELLOW + f" is {(Fore.RED + 'not ' + Fore.YELLOW) if result is False else ''}accepted")

    def __get_prefix(self, sequence):
        result = self.__state_machine.get_longest_prefix(sequence)
        print(Fore.RED + result + Fore.BLUE + sequence[len(result):])

    def run(self):
        methods = [
            self.__print_all_states, 
            self.__print_alphabet, 
            self.__print_transitions, 
            self.__print_final_states,
            self.__check_acceptance,
            self.__get_prefix
        ]
        while True:
            x = input(Fore.RESET + """Pick an option:
  1. Print all states
  2. Print alphabet
  3. Print transitions
  4. Print final states
  5. Check if sequence is accepted
  6. Get longest accepted prefix
  0. Exit
Option: """).split()
            if not len(x): continue
            if x[0] == '0': 
                print('Exiting...')
                break
            else:
                k = int(x[0])
                if k < 5: methods[k-1]()
                else: 
                    if len(x) > 1:
                        methods[k-1](x[1])
                    else:
                        print('Provide a sequence of characters alongside with the option.')
                input(Fore.RESET + 'Press RETURN to continue...')

        
