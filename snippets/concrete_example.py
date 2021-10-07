from dataclasses import dataclass
from typing import Callable, Generator, Iterator, Mapping, Sequence, Set, Tuple
from enum import Enum, auto


# Possibly mutable
@dataclass
class UserState():
    prey: float
    predator: float


@dataclass
class MetaState():
    timestep: int
    substep: int


@dataclass
class MutableState():
    user_state: UserState
    meta_state: MetaState

# Always immutable


@dataclass
class ModelParameters():
    alpha: float
    beta: float
    delta: float
    gamma: float


@dataclass
class MetaParameters():
    N_timesteps: int
    N_runs: int


@dataclass
class ImmutableState():
    model_parameters: ModelParameters
    meta_parameters: MetaParameters


class Signals(Enum):
    add_prey = auto()
    add_predator = auto()


Signal = Mapping[Signals, object]
Policy = Callable[[ImmutableState, MutableState], Signal]
UpdateFunction = Callable[[ImmutableState, MutableState, Signal], object]
BlockPolicies = Sequence[Policy]
BlockUpdates = Mapping[Signals, UpdateFunction]


@dataclass
class PartialStateUpdateBlock():
    policies: BlockPolicies
    updates: BlockUpdates


def render_default_signal() -> Signal:
    # This should be adaptable
    return {Signals.add_prey: 0.0,
            Signals.add_predator: 0.0}


def render_default_updates():
    # TODO
    pass


def p_prey_born(params: ImmutableState,
                state: MutableState) -> Signal:
    value = state.user_state.prey * params.model_parameters.alpha
    signal = {Signals.add_prey: value}
    return signal


def p_prey_deaths(params: ImmutableState,
                  state: MutableState) -> Signal:
    value = -1 * state.user_state.prey * state.user_state.predator
    value *= params.model_parameters.beta
    signal = {Signals.add_prey: value}
    return signal


def p_predator_born(params: ImmutableState,
                    state: MutableState) -> Signal:
    value = state.user_state.prey * state.user_state.predator
    value *= params.model_parameters.delta
    signal = {Signals.add_predator: value}
    return signal


def p_predator_deaths(params: ImmutableState,
                      state: MutableState) -> Signal:
    value = -1 * state.user_state.predator
    value *= params.model_parameters.gamma
    signal = {Signals.add_predator: value}
    return signal


def s_update_prey(params: ImmutableState,
                  state: MutableState,
                  signal: Signal) -> object:
    return state.user_state.prey + signal[Signals.add_prey]


def s_update_predator(params: ImmutableState,
                      state: MutableState,
                      signal: Signal) -> object:
    return state.user_state.predator + signal[Signals.add_predator]


def aggregate_signals(signals: Sequence[Signal]) -> Signal:
    aggregate_signal = render_default_signal()
    for signal in signals:
        for signal_key, signal_value in signal.items():
            # Hypothesis: aggregation rule is a simple sum
            # This should be modifiable
            aggregate_signal[signal_key] += signal_value
    return aggregate_signal


def block_update(block: PartialStateUpdateBlock,
                 params: ImmutableState,
                 state: MutableState) -> MutableState:

    signals: Sequence[Signal] = (policy(params, state)
                                 for policy
                                 in block.policies)

    aggregate_signal = aggregate_signals(signals)

    update_results = {key: function(params, state, aggregate_signal)
                      for key, function
                      in block.updates.items()}

    new_user_state = UserState(**update_results)

    state = MutableState(new_user_state, state.meta_state)

    return state


Blocks = Sequence[PartialStateUpdateBlock]


def timestep_update(blocks: Blocks,
                    params: ImmutableState,
                    state: MutableState) -> Iterator[MutableState]:
    for block in blocks:
        state = block_update(block, params, state)
        new_meta_state = MetaState(state.meta_state.timestep,
                                   state.meta_state.substep + 1)
        state.meta_state = new_meta_state
        yield state


def trajectory_run(blocks: Blocks,
                   params: ImmutableState,
                   state: MutableState) -> Iterator[MutableState]:
    yield state
    for timestep in range(params.meta_parameters.N_timesteps):
        new_meta_state = MetaState(timestep, 0)
        state.meta_state = new_meta_state
        for state in timestep_update(blocks, params, state):
            yield state


block_1 = PartialStateUpdateBlock(
    policies=[p_prey_born, p_prey_deaths],
    updates={Signals.add_prey: s_update_prey}
)

block_2 = PartialStateUpdateBlock(
    policies=[p_predator_born, p_predator_deaths],
    updates={Signals.add_predator: s_update_predator}
)

blocks = [block_1, block_2]


initial_state = MutableState(UserState(prey=0.0, predator=0.0),
                             MetaState(timestep=0, substep=0))

params = ImmutableState(ModelParameters(alpha=0.1, beta=0.1, delta=0.1, gamma=0.1),
                        MetaParameters(N_timesteps=10, N_runs=3))

records = trajectory_run(blocks,
                         params,
                         initial_state)


x = list(records)

print('done')