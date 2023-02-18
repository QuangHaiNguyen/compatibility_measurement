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

class Transition():
    def __init__(self, name: str,
                 type: TransitionType,
                 next_state: str,
                 params: list = None) -> None:
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


if __name__ == '__main__':
    transition = Transition(name="test_transition",
                            next_state="next_state",
                            type=TransitionType.EMISSION,
                            params=["param1:type1", "param2:type2", "param3:type3"])
    logger.info("list of data types: ")
    logger.info(transition.get_data_types())