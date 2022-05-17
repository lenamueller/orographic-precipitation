from enum import Enum
import sys

class States(Enum):
    READY = 1
    NOT_READY = 2
    ACCUMULATING = 3
    FINISHING = 4


class StateMachine:
    def __init__(self, trigger_level: int):
        self.trigger_level = trigger_level
        self.counter = 0
        self.result_list = []
        self.accumulate_list = []
        self.state = States.NOT_READY
        
    def __not_ready_transition(self, pr):
        # check if value is zero precipitation
        if pr == 0:
            self.counter +=1
            # add up counter and check if level is reached
            if self.counter >= self.trigger_level:
                self.state = States.READY
                self.counter = 0
        # reset counter 
        else:
            self.counter = 0
        
    def __ready_transition(self, pr):
        if pr > 0:
            self.state = States.ACCUMULATING
            self.accumulate_list.append(pr)
        
    def __accumulate_tranision(self, pr):
        if pr == 0:
            self.counter += 1
            self.state = States.FINISHING
        else:
            self.accumulate_list.append(pr)
        
    def __finish_transition(self, pr):
        if pr == 0: # bleibt im finishing
            self.counter += 1
            print(self.counter)
            if self.counter >= self.trigger_level:
                self.result_list.append(self.accumulate_list)
                self.accumulate_list = []
                self.counter = 0
                self.state = States.READY
        else:
            self.accumulate_list = []
            self.counter = 0
            self.state = States.NOT_READY
        
    def feed(self, pr: float):
        match self.state:
            case States.NOT_READY:
                self.__not_ready_transition(pr)
            case States.READY:
                self.__ready_transition(pr)
            case States.ACCUMULATING:
                self.__accumulate_tranision(pr)
            case States.FINISHING:
                self.__finish_transition(pr)


def find_special_events(precipitation: list[float], trigger_level: int = 72) -> list[list[float]]:
    if trigger_level < 2:
        raise ValueError("Trigger level must be larger than 2")
    
    if type(precipitation) != list[float]:
        raise TypeError("Input list is not of type float.")
    
    state_machine = StateMachine(trigger_level)
    for p in precipitation:
        state_machine.feed(p)
        
    return state_machine.result_list


# example = [0,0,0,1,2,3,0,0,2,0,0,0,0]
# example = [0,1,0]
# print(find_special_events(example, trigger_level=1))