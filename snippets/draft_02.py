from dataclasses import dataclass, make_dataclass
from typing import Callable, Generator, Mapping, NamedTuple, Sequence, Tuple, Union


# Core classes and relationships
State = object
StateRecords = Sequence[State]
PartialStateUpdateBlock = Mapping[State, State]
StateUpdatePipeline = Sequence[PartialStateUpdateBlock]
ExitCondition = Callable[[State], bool]
Job = Tuple[State, StateUpdatePipeline, ExitCondition]
Trajectory =  Generator[State]
Simulation = Callable[[Job], Trajectory]



