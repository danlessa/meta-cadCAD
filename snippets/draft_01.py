from dataclasses import dataclass, make_dataclass
from typing import NamedTuple, Tuple, Union

class InitialValue(NamedTuple):
    value: object
    value_type: type





InitialState = dict[str, InitialValue]
Param = InitialValue
ParamSweep = Tuple[list[object], type]
Parameters = dict[str, Union[Param, ParamSweep]]


initial_state = {'prey_count': InitialValue(100.0, float),
                 'predator_count': InitialValue(10.0, float)}

def process_initial_state(initial_state: dict[str, InitialValue]) -> tuple[str, object]:
    for key, initial_value in initial_state.items():
        yield (key, initial_value[1])

gen_expr = ((k, v[1]) for k, v in initial_state.items())
State = make_dataclass('State',  gen_expr)

@dataclass
class MetaState():
    """
    State associated with execution rather than physical details.
    """
    timestep: int
    substep: int

Signal = None

def trajectory(initial_state: State):
    """
    
    """
    pass


def timestep_transition(state: State, timestep_block) -> State:
    """
    Evolve the state in real time.
    """
    
    virtual_state = state
    for substep_block in timestep_block:
        virtual_state = substep_transition(virtual_state, substep_block)

    new_state = virtual_state
    return new_state




def substep_signal(state: State) -> Signal:
    pass


def substep_state_mutate(state: State, signal: Signal) -> State:
    pass

def substep_transition(state: State) -> State:
    """
    Evolve the state in virtual time.
    """
    signal = substep_signal(state)
    mutated_state = substep_state_mutate(state, signal)
    return mutated_state



