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

