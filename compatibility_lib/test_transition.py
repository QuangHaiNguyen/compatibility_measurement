__author__ = "Quang Hai, Nguyen"
__copyright__ = "Copyright 2023, Protocol Compatibility Measurement"
__credits__ = ["Quang Hai, Nguyen"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Quang Hai"
__email__ = "hai.nguyen.quang@outlook.com"
__status__ = "Development"

"""Unit test for graph.py module
"""

import pytest
from .graph import Transition, TransitionType



@pytest.fixture
def normal_transition() -> Transition:
    transition = Transition(name="test_transition",
                            next_state="next_state",
                            type=TransitionType.EMISSION,
                            params=["param1:type1", "param2:type2", "param3:type3"])
    return transition


def test_create_normal_transition(normal_transition:Transition):
    assert normal_transition.name == "test_transition"
    assert normal_transition.next_state == "next_state"
    assert normal_transition.type == TransitionType.EMISSION
    
    assert normal_transition.get_param_type("param1") == "type1"
    assert normal_transition.get_param_type("param2") == "type2"
    assert normal_transition.get_param_type("param3") == "type3"
    assert normal_transition.get_param_type("param4") == None
    assert normal_transition.get_param_type("param5") == None


def test_get_type_normal_transition(normal_transition:Transition):    
    data_type1 = ["type1", "type2", "type3"]
    data_type2 = ["type1", "type2", "type3", "type4"]
    
    assert sorted(normal_transition.get_data_types()) == sorted(data_type1)
    assert sorted(normal_transition.get_data_types()) != sorted(data_type2)

    
def test_get_type_no_diplicate_normal_transition(normal_transition:Transition):    
    types = normal_transition.get_data_types()
    assert len(types) == len(set(types))


def test_create_tau_transition_with_no_empty_params():
    with pytest.raises(Exception):
        tau_transition = Transition(name="test_transition",
                                    next_state="next_state",
                                    type=TransitionType.TAU,
                                    params=["param1:type1", "param2:type2", "param3:type3"])

        
def test_create_tau_transition_with_empty_params():
    tau_transition = Transition(name="test_transition",
                                next_state="next_state",
                                type=TransitionType.TAU)
    assert tau_transition.params == []