__author__ = "Quang Hai, Nguyen"
__copyright__ = "Copyright 2023, Protocol Compatibility Measurement"
__credits__ = ["Quang Hai, Nguyen"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Quang Hai"
__email__ = "hai.nguyen.quang@outlook.com"
__status__ = "Development"

"""Unit test for state class
"""

import pytest
from graph import Transition, TransitionType
from graph import State, StateType


@pytest.fixture
def transitions() -> tuple:
    transition1 = Transition(name="test_transition_1",
                            next_state="next_state_1",
                            type=TransitionType.EMISSION,
                            params=["param1:type1", "param2:type2", "param3:type3"])
    transition2 = Transition(name="test_transition_2",
                            next_state="next_state_2",
                            type=TransitionType.RECPTION,
                            params=["param1:type1", "param2:type2"])
    transition3 = Transition(name="test_transition_3",
                            next_state="next_state_3",
                            type=TransitionType.EMISSION,
                            params=["param1:type1", "param2:type2", "param3:type3"])
    transition4 = Transition(name="test_transition_4",
                            next_state="next_state_4",
                            type=TransitionType.RECPTION,
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


def test_create_normal_state(normal_state:State, transitions):
    incoming = [transitions[0], transitions[1]]
    outgoing = [transitions[2], transitions[3]]
    
    assert normal_state.is_final_state() == False
    assert normal_state.is_initial_state() == False
    assert normal_state.get_num_of_incoming_transistions() == 2
    assert normal_state.get_num_of_outgoing_transitions() == 2
    
    test_incoming = normal_state.get_incoming_transitions_list()
    assert incoming == test_incoming
    
    test_outgoing = normal_state.get_outgoing_transitions_list()
    assert outgoing == test_outgoing
    
    
def test_create_int_final_state(init_state:State, final_state:State):
    assert init_state.is_initial_state() == True
    assert init_state.is_final_state() == False
    assert final_state.is_final_state() == True
    assert final_state.is_initial_state() == False
    
    assert init_state.get_num_of_outgoing_transitions() == 2
    assert init_state.get_num_of_incoming_transistions() == 0
    incoming = init_state.get_incoming_transitions_list()
    assert incoming == []
    
    assert final_state.get_num_of_incoming_transistions() == 2
    assert final_state.get_num_of_outgoing_transitions() == 0
    outgoing = final_state.get_outgoing_transitions_list()
    assert outgoing == []
    
    
def test_get_transition(normal_state:State, transitions):
    assert transitions[0] == normal_state.get_incoming_transtition(transitions[0].name)
    assert transitions[1] == normal_state.get_incoming_transtition(transitions[1].name)
    assert transitions[2] == normal_state.get_outgoing_transtition(transitions[2].name)
    assert transitions[3] == normal_state.get_outgoing_transtition(transitions[3].name)
    
    
def test_set_transition(normal_state:State, transitions):
    new_transition = Transition(name="new_transition",
                            next_state="new_transition_next",
                            type=TransitionType.RECPTION,
                            params=["param1:type1", "param2:type2"])
    
    normal_state.add_incoming_transition(new_transition)
    assert normal_state.get_num_of_incoming_transistions() == 3
    
    assert transitions[0] == normal_state.get_incoming_transtition(transitions[0].name)
    assert transitions[1] == normal_state.get_incoming_transtition(transitions[1].name)
    assert new_transition == normal_state.get_incoming_transtition(new_transition.name)
    
    normal_state.add_incoming_transition(None)
    assert normal_state.get_num_of_incoming_transistions() == 3
    
    normal_state.add_outgoing_transition(new_transition)
    assert normal_state.get_num_of_outgoing_transitions() == 3
    
    assert transitions[2] == normal_state.get_outgoing_transtition(transitions[2].name)
    assert transitions[3] == normal_state.get_outgoing_transtition(transitions[3].name)
    assert new_transition == normal_state.get_outgoing_transtition(new_transition.name)
    
    normal_state.add_outgoing_transition(None)
    assert normal_state.get_num_of_outgoing_transitions() == 3
    
    
def test_create_init_state_fail(transitions):
    with pytest.raises(Exception):
        state = State(name="test_state",
                  type=StateType.INIT,
                  incoming= [transitions[0], transitions[1]],
                  outgoing= [transitions[2], transitions[3]]
                  )
     
        
def test_create_final_state_fail(transitions):
    with pytest.raises(Exception):
        state = State(name="test_state",
                  type=StateType.FINAL,
                  incoming= [transitions[0], transitions[1]],
                  outgoing= [transitions[2], transitions[3]]
                  )
     
        
def test_add_incoming_transition_to_init_state(init_state, transitions):
    new_transition = Transition(name="new_transition",
                            next_state="new_transition_next",
                            type=TransitionType.RECPTION,
                            params=["param1:type1", "param2:type2"])
    
    with pytest.raises(Exception):
        init_state.add_incoming_transition(new_transition)
     
        
def test_add_outgoing_transition_to_final_state(final_state, transitions):
    new_transition = Transition(name="new_transition",
                            next_state="new_transition_next",
                            type=TransitionType.RECPTION,
                            params=["param1:type1", "param2:type2"])
    
    with pytest.raises(Exception):
        final_state.add_outgoing_transition(new_transition)