#!/usr/bin/env python

__author__ = "Quang Hai, Nguyen"
__copyright__ = "Copyright 2023, Protocol Compatibility Measurement"
__credits__ = ["Quang Hai, Nguyen"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Quang Hai"
__email__ = "hai.nguyen.quang@outlook.com"
__status__ = "Development"

"""Provide the definitions for graph, state and transition class.
The module parser will read the data from the json files and create graph,
states, and transitions based on this module.
"""

from enum import Enum, auto
import logging

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)
#logger.setLevel(logging.WARNING)
#logger.setLevel(logging.ERROR)
#logger.setLevel(logging.CRITICAL)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

class TransitionType(Enum):
    TAU = auto()
    EMISSION = auto()
    RECPTION = auto()

class StateType(Enum):
    INIT = auto()
    FINAL = auto()
    NORMAL = auto()

class Transition():
    def __init__(self, name: str,
                 type: TransitionType,
                 next_state: str,
                 params: list = []) -> None:
        """__init__ constructore for Transition class

        Args:
            name (str): name of the transition
            type (TransitionType): type of the transition
            next_state (str): name of the next state, where the transition going to
            params (list, optional): parameter list of the transiotion.
                                    Defaults to []. For TAU transition, this argument
                                    must be []

        Raises:
            Exception: Tau transition has list of parameters, i.e., params is
                        not empty
        """
          
        self.name = name
        self.type = type
        self.next_state = next_state
        self.params = params
        
        if self.type == TransitionType.TAU and params:
            raise Exception("Illegal transition. tau has no parameters list")

    def get_param_type(self, param_name: str) -> str:
        """Get the data type of a parameter

        Args:
            param_name (str): name of the parameter

        Returns:
            str: data type or None
        """
        data_type = None
        logger.debug("get data type of [parameter = {}]".format(param_name))
        
        if self.params:
            for param in self.params:
                if param_name in param:
                    data_type = param.split(":")[1]
        else:
            logger.warning("parameters list is empty")
            
        return data_type
    
    def get_data_types(self)-> list:
        """Get list of data type of the transition

        Returns:
            list: list of data type or None
        """
        data_types = []
        if self.params:
            for param in self.params:
                # Only get this type if it is not duplicated
                if param.split(":")[1] not in data_types:
                    data_types.append(param.split(":")[1])        
        else:
            logger.warning("parameters list is empty")
        
        return data_types

class State():
    def __init__(self, name: str,
                 type: StateType,
                 incoming: list = [],
                 outgoing: list = []) -> None:
        """Constructor of the State class
        Args:
            name (str): name of the state
            type (StateType): type of the state
            incoming (list, optional): Incoming transition. Defaults to None.
            outgoing (list, optional): Outgoing transition. Defaults to None.

        Raises:
            Exception: Initial state does not have incoming transition
            Exception: Final state does not have outgoing transition
        """
        self._name = name
        self._type = type
        self._incoming = incoming
        self._outgoing = outgoing
        
        if self._type == StateType.INIT and self._incoming:
            raise Exception("Initial state does not have incoming transition")
    
        if self._type == StateType.FINAL and self._outgoing:
            raise Exception("Final state does not have outgoing transition")

    def add_incoming_transition(self, transition: Transition):
        """Add an incoming transition

        Args:
            transition (Transition): transition to be added

        Raises:
            Exception: Initial state does not have incoming transition
        """
        if transition is None:
            return
        
        logger.debug("add new incoming transition [name = {}]".format(transition.name))
        if self._type == StateType.INIT:
            raise Exception("Initial state does not have incoming transition")
        else:
            self._incoming.append(transition)
    
    def add_outgoing_transition(self, transition: Transition):
        """Add an outgoing transition

        Args:
            transition (Transition): transition to be added

        Raises:
            Exception: Final state does not have outgoing transition
        """
        if transition is None:
            return
        
        logger.debug("add new outgoing transition [name = {}]".format(transition.name))
        if self._type == StateType.FINAL:
            raise Exception("Final state does not have outgoing transition")
        else:
            self._outgoing.append(transition)
    
    def get_incoming_transtition(self, name: str) -> Transition:
        """Get an incoming transition

        Args:
            name (str): name of the transition

        Returns:
            Transition: incoming transition
        """
        logger.debug("get incoming transition [name = {}]".format(name))
        ret_transition = None
        
        if self._type != StateType.INIT:
            for transition in self._incoming:
                if name == transition.name:
                    ret_transition = transition
                    logger.debug("transition found")
                    break
        else:
            logger.warning("Initial state has no incoming transitions")
        return ret_transition
    
    def get_outgoing_transtition(self, name: str) -> Transition:
        """Get out going transition

        Args:
            name (str): name of the transition

        Returns:
            Transition: outgoing transition
        """
        logger.debug("get outgoing transition [name = {}]".format(name))
        ret_transition = None
        
        if self._type != StateType.FINAL:
            for transition in self._outgoing:
                if name == transition.name:
                    ret_transition = transition
                    logger.debug("transition found")
                    break
        else:
            logger.warning("Final state has no outgoing transitions")
                    
        return ret_transition
    
    def get_incoming_transitions_list(self) -> list:
        """Get the list on incoming transitions

        Returns:
            list: incoming transitions list
        """
        return self._incoming
    
    def get_outgoing_transitions_list(self) -> list:
        """Get the list of outgoing transitions

        Returns:
            list: outgoing transitions list
        """
        return self._outgoing
    
    def get_num_of_incoming_transistions(self) -> int:
        """Get number of incoming transition

        Returns:
            int: number of transitions
        """
        return len(self._incoming)
    
    def get_num_of_outgoing_transitions(self) -> int:
        """Get number of outgoing transition

        _extended_summary_

        Returns:
            int: number of transitions
        """
        return len(self._outgoing)
    
    def is_final_state(self) -> bool:
        """Check if state is final state

        Returns:
            bool: True if final state
        """
        if self._type == StateType.FINAL:
            logger.debug("[state = {}] is FINAL state".format(self._name))
            return True
        else:
            logger.debug("[state = {}] is NOT FINAL state".format(self._name))
            return False
    
    def is_initial_state(self) -> bool:
        """check if state is initial state

        Returns:
            bool: True if initial state
        """
        if self._type == StateType.INIT:
            logger.debug("[state = {}] is INIT state".format(self._name))
            return True
        else:
            logger.debug("[state = {}] is NOT INIT state".format(self._name))
            return False
    
    
if __name__ == '__main__':
    transition = Transition(name="test_transition",
                            next_state="next_state",
                            type=TransitionType.EMISSION,
                            params=["param1:type1", "param2:type2", "param3:type3"])
    logger.info("list of data types: ")
    logger.info(transition.get_data_types())