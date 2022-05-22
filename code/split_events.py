from datetime import datetime
from enum import Enum
from typing import Tuple

class States(Enum):
    READY = 1
    NOT_READY = 2
    ACCUMULATING = 3
    FINISHING = 4


class StateMachine:
    def __init__(self, trigger_level: int):
        self.trigger_level = trigger_level
        self.counter = 0
        self.result_list: list[list[float]] = []
        self.result_list_dates: list[list[datetime]] = []
        self.accumulate_list: list[float] = []
        self.accumulate_list_dates: list[float] = []
        self.state = States.NOT_READY
        
    def __not_ready_transition(self, pr, d):
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
        
    def __ready_transition(self, pr, d):
        if pr > 0:
            self.state = States.ACCUMULATING
            self.accumulate_list.append(pr)
            self.accumulate_list_dates.append(d)
        
    def __accumulate_tranision(self, pr, d):
        if pr == 0:
            self.counter += 1
            self.state = States.FINISHING
        else:
            self.accumulate_list.append(pr)
            self.accumulate_list_dates.append(d)
        
    def __finish_transition(self, pr, d):
        if pr == 0: # bleibt im finishing
            self.counter += 1
            # print(self.counter)
            if self.counter >= self.trigger_level:
                # independent storms below 30 min duration are ignored
                if len(self.accumulate_list)>3:
                    self.result_list.append(self.accumulate_list)
                    self.result_list_dates.append(self.accumulate_list_dates)
                self.accumulate_list = []
                self.accumulate_list_dates = []
                self.counter = 0
                self.state = States.READY
        else:
            self.accumulate_list = []
            self.accumulate_list_dates = []
            self.counter = 0
            self.state = States.NOT_READY
        
    def feed(self, pr: float, d: datetime):
        match self.state:
            case States.NOT_READY:
                self.__not_ready_transition(pr,d)
            case States.READY:
                self.__ready_transition(pr,d)
            case States.ACCUMULATING:
                self.__accumulate_tranision(pr,d)
            case States.FINISHING:
                self.__finish_transition(pr,d)


def find_precipitation_events(precipitation: list[float], dates: list[datetime], trigger_level: int = 36) -> Tuple[list[list[float]], list[list[datetime]]]:
    # ! return empty list for empty input list
    if precipitation == []:
        return [],[]
    # ! raise error if trigger level is one
    if trigger_level < 2:
        raise ValueError("Trigger level must be larger than 2")
    # ! raise error if precipitation input list is not of type float or int
    if type(precipitation[0]) not in (float, int):
        raise TypeError("Input list is not of type float.")
    
    state_machine = StateMachine(trigger_level)
    for (p,d) in zip(precipitation,dates):
        state_machine.feed(p,d)
        
    return state_machine.result_list, state_machine.result_list_dates