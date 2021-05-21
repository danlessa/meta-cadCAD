from dataclasses import dataclass, make_dataclass
from typing import NamedTuple, Tuple, Union

class InitialValue(NamedTuple):
    value: object
    value_type: type




InitialState = dict[str, InitialValue]
Param = InitialValue
ParamSweep = Tuple[list[object], type]
Parameters = dict[str, Union[Param, ParamSweep]]


initial_state = {'a': InitialValue(0.0, float),
                 'b': InitialValue(1.0, float)}

State = make_dataclass('State',  initial_state.items())