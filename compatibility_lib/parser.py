#!/usr/bin/env python

__author__ = "Quang Hai, Nguyen"
__copyright__ = "Copyright 2023, Protocol Compatibility Measurement"
__credits__ = ["Quang Hai, Nguyen"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Quang Hai"
__email__ = "hai.nguyen.quang@outlook.com"
__status__ = "Development"

"""This module verify the input json file following a defined format and parser
the data in the json file to corresponding graph.

The format of the json file is:

{
    "graph_name":"NAME_OF_THE_GRAPH",
    "states":
    [
        {
            "state_name":"NAME_OF_STATE",
            "state_type":"STATE_TYPE"
            "transitions":
            [
                {
                    "transition_name":"NAME_OF_THE_TRANSITION"
                    "transition_type":"TRANSITION_TYPE"
                    "params":["name:data_type", "name:data_type", "name:data_type"]
                    "next_state":"NAME_OF_STATE"
                }
            ]
        },
        {
            "state_name":"NAME_OF_STATE",
            "state_type":"STATE_TYPE"
            "transitions":
            [
                {
                    "transition_name":"NAME_OF_THE_TRANSITION"
                    "transition_type":"TRANSITION_TYPE"
                    "params":["name:data_type", "name:data_type", "name:data_type"]
                    "next_state":"NAME_OF_STATE"
                }
            ]
        },
    ]
}
"""

from .graph import *
import logging
import os.path
import json

GRAPH_NAME_KEY = "graph_name"
STATES_KEY = "states"

STATE_NAME_KEY = "state_name"
STATE_TYPE_KEY = "state_type"
STATE_TRANSITION_KEY = "transitions"

TRANSITION_NAME_KEY = "transition_name"
TRANSITION_TYPE_KEY = "transition_type"
TRANSITION_PARAM_KEY = "params"
TRANSITION_NEXT_STATE_KEY = "next_state"

# create logger

logger = logging.getLogger("PARSER")

#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)
#logger.setLevel(logging.WARNING)
#logger.setLevel(logging.ERROR)
#logger.setLevel(logging.CRITICAL)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(name)s - %(funcName)s - %(levelname)s - %(message)s')


# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


def is_transaction_valid(transaction_dict: dict) -> bool:
    valid = False
    
    if TRANSITION_NAME_KEY in transaction_dict and transaction_dict[TRANSITION_NAME_KEY] != "":
        valid = True
    else:
        logger.error("transition_name property invalid")
        return False
    
    logger.info("processing transition = {}...".format(transaction_dict[TRANSITION_NAME_KEY]))
    
    if TRANSITION_TYPE_KEY in transaction_dict:
        if transaction_dict[TRANSITION_TYPE_KEY] == "reception" or transaction_dict[TRANSITION_TYPE_KEY] == "emission":
            valid = True
        else:
            logger.error("transition_type has wrong value, get = {}".format(transaction_dict[TRANSITION_TYPE_KEY]))
            return False
    else:
        logger.error("transition_type property invalid")
        return False
    
    if TRANSITION_PARAM_KEY in transaction_dict and type(transaction_dict[TRANSITION_PARAM_KEY]) == list:
        valid = True
    else:
        logger.error("params has wrong property invalid")
        return False
    
    if TRANSITION_NEXT_STATE_KEY in transaction_dict and transaction_dict[TRANSITION_NEXT_STATE_KEY] != "":
        valid = True
    else:
        logger.error("next_state has wrong property invalid")
        return False
    
    if(valid):
        logger.info("transition = {} is valid".format(transaction_dict[TRANSITION_NAME_KEY]))
        logger.info("   type = {}".format(transaction_dict[TRANSITION_TYPE_KEY]))
        logger.info("   num of param = {}".format(len(transaction_dict[TRANSITION_PARAM_KEY])))
        logger.info("   next_state = {}".format(transaction_dict[TRANSITION_NEXT_STATE_KEY]))
    
    return valid


def is_state_format_valid(states: list) -> bool:
    Succes = False
    
    for state in states:
        if STATE_NAME_KEY in state and state[STATE_NAME_KEY] != "":
            Succes = True
        else:
            logger.error("state_name properties error")
            Succes = False
        
        logger.info("processing [state = {}]...".format(state[STATE_NAME_KEY]))
        
        if Succes == True and STATE_TYPE_KEY in state and state[STATE_TYPE_KEY] != "":
            if state[STATE_TYPE_KEY] == "initial" or state[STATE_TYPE_KEY] == "final" or state[STATE_TYPE_KEY] == "normal":
                Succes = True
            else:
                logger.error("state_type property error")
                Succes = False
        else:
            logger.error("state_type properties error")
            Succes = False
            
        if Succes == True and STATE_TRANSITION_KEY in state and type(state[STATE_TRANSITION_KEY]) == list:
            Succes = True
        else:
            logger.error("transition property error")
            Succes = False
        
        if Succes == True:
            logger.info("state = {} OK".format(state[STATE_NAME_KEY]))
            logger.info("   [type = {}]".format(state[STATE_TYPE_KEY]))
            logger.info("   [num_of_outgoing_transition = {}]".format(len(state[STATE_TRANSITION_KEY])))
        else:
            break
        
    return Succes

def create_transition(transtition_dict: dict) -> Transition:
    transition_type = None
    
    if transtition_dict[TRANSITION_TYPE_KEY] == "reception":
        transition_type = TransitionType.RECEPTION
    elif transtition_dict[TRANSITION_TYPE_KEY] == "emission":
        transition_type = TransitionType.EMISSION
    else:
        #must not be here
        logger.error("unknown transition type")
    
    return Transition(name=transtition_dict[TRANSITION_NAME_KEY],
                        next_state= transtition_dict[TRANSITION_NEXT_STATE_KEY],
                        type= transition_type,
                        params=transtition_dict[TRANSITION_PARAM_KEY])


def add_incoming_transitions_to_states(states: list):
    for state in states:
        #get transition in state
        logger.debug("state = {}".format(state.get_name()))
        for transition in state.get_outgoing_transitions_list():
            logger.debug("adding transition = {}".format(transition.name))
            found_next_state = False
            for next_state in states:
                if transition.next_state == next_state.get_name():
                    next_state.add_incoming_transition(transition)
                    found_next_state = True
                    break
                
            if found_next_state == True:
                logger.info("add transition = {} type = {} to incoming transitsion of state = {}".format(
                    transition.name, transition.type, transition.next_state
                ))
            else:
                raise Exception("unknown next state = {}".format(transition.next_state))
            

def create_states(states: list) -> list:
    output_states =[]
    for state in states:
        logger.debug("creating [state = {}]...".format(state[STATE_NAME_KEY]))
        state_type = StateType.NORMAL
        if state[STATE_TYPE_KEY] == "initial":
            state_type = StateType.INIT
        elif state[STATE_TYPE_KEY] == "final":
            state_type = StateType.FINAL
        elif state[STATE_TYPE_KEY] == "normal":
            state_type = StateType.NORMAL
        else:
            logger.error("unknow state, must not be here")
            raise Exception("unknown state")

        new_state = State(name=state[STATE_NAME_KEY], type=state_type)
        
        for transition in state[STATE_TRANSITION_KEY]:
            if is_transaction_valid(transition) == False:
                raise Exception("Transition has wrong format")
            else:
                transition = create_transition(transition)
                if transition != None:
                    new_state.add_outgoing_transition(transition)
            
        logger.info("create [state = {}] success".format(state[STATE_NAME_KEY]))
        output_states.append(new_state)
            
    return output_states


def create_graph(input_path: str) -> Graph:
    ret_graph = None  
    if os.path.isfile(input_path) == False:
        logger.error("file does not exist")
        return

    with open(input_path, "r") as read_json_file:
        logger.debug("open [file = {}]".format(input_path))
        graph_dict = json.load(read_json_file)
        
        logger.debug("[type = {}]".format(type(graph_dict)))
        if logger.level == logging.DEBUG:
            logger.debug("here is your json file")
            print(json.dumps(graph_dict, indent=4))
            
        if GRAPH_NAME_KEY in graph_dict and STATES_KEY in graph_dict:
            if graph_dict[GRAPH_NAME_KEY] != "":
                logger.debug("[graph name = {}]".format(graph_dict[GRAPH_NAME_KEY]))
                
                if type(graph_dict[STATES_KEY]) == list and len(graph_dict[STATES_KEY]) > 1:
                    logger.debug("graph has [num of states = {}]".format(len(graph_dict[STATES_KEY])))
                    ret_graph = Graph(name=graph_dict[GRAPH_NAME_KEY])
                else:
                    raise Exception("graph does not have enough number of state")  
            else:
                raise Exception("graph name is empty")
        else:
            raise Exception("graph missing properties")
        
        if ret_graph != None:
            if is_state_format_valid(graph_dict[STATES_KEY]) == False:
                raise Exception("states are not valid")
            else:
                pass
            
            states = create_states(graph_dict[STATES_KEY])
            add_incoming_transitions_to_states(states)
            
            for state in states:
                state.print_state()
                ret_graph.add_state(state)
    
    logger.info("create graph = {} success".format(ret_graph._name))
    return ret_graph


if __name__ == '__main__':
    create_graph("test_data/test.json")