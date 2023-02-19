__author__ = "Quang Hai, Nguyen"
__copyright__ = "Copyright 2023, Protocol Compatibility Measurement"
__credits__ = ["Quang Hai, Nguyen"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Quang Hai"
__email__ = "hai.nguyen.quang@outlook.com"
__status__ = "Development"

"""Unit test for graph class
"""

import pytest
from .graph import Transition, TransitionType
from .graph import State, StateType
from .graph import Graph


@pytest.fixture
def transitions() -> tuple:
    transition1 = Transition(name="test_transition_1",
                            next_state="next_state_1",
                            type=TransitionType.EMISSION,
                            params=["param1:type1", "param2:type2", "param3:type3"])
    transition2 = Transition(name="test_transition_2",
                            next_state="next_state_2",
                            type=TransitionType.RECEPTION,
                            params=["param1:type1", "param2:type2"])
    transition3 = Transition(name="test_transition_3",
                            next_state="next_state_3",
                            type=TransitionType.EMISSION,
                            params=["param1:type1", "param2:type2", "param3:type3"])
    transition4 = Transition(name="test_transition_4",
                            next_state="next_state_4",
                            type=TransitionType.RECEPTION,
                            params=["param1:type1", "param2:type2"])
    return (transition1, transition2, transition3, transition4)


@pytest.fixture
def normal_state(transitions) -> State:
    
    state = State(name="test_state",
                  type=StateType.NORMAL,
                  incoming= [transitions[0], transitions[1]],
                  outgoing= [transitions[2], transitions[3]]
                  )
    
    return state


@pytest.fixture
def init_state(transitions) -> State:
    
    state = State(name="test_state",
                  type=StateType.INIT,
                  outgoing= [transitions[2], transitions[3]]
                  )
    
    return state


@pytest.fixture
def final_state(transitions) -> State:
    
    state = State(name="test_state",
                  type=StateType.FINAL,
                  incoming= [transitions[0], transitions[1]]
                  )
    
    return state


def test_create_graph(init_state, normal_state, final_state, transitions):
    
    new_state = State(name="new_state",
                  type=StateType.NORMAL,
                  incoming= [transitions[0], transitions[1]],
                  outgoing= [transitions[2], transitions[3]]
                  )
    
    graph = Graph(name="graph", 
                  states=[init_state, normal_state, final_state])

    assert len(graph.get_states_list()) == 3
    
    assert (init_state in graph.get_states_list()) == True
    assert (normal_state in graph.get_states_list()) == True
    assert (final_state in graph.get_states_list()) == True
    
    assert normal_state.get_name() == graph.get_state(normal_state.get_name()).get_name()

    
    graph.add_state(new_state)
    assert len(graph.get_states_list()) == 4
    assert (new_state in graph.get_states_list()) == True
    
    graph.add_state(None)
    assert len(graph.get_states_list()) == 4
    
    
    