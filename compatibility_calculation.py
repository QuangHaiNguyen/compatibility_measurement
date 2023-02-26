#!/usr/bin/env python

__author__ = "Quang Hai, Nguyen"
__copyright__ = "Copyright 2023, Protocol Compatibility Measurement"
__credits__ = ["Quang Hai, Nguyen"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Quang Hai"
__email__ = "hai.nguyen.quang@outlook.com"
__status__ = "Prototype"

""" Calculate the compatibility between two graphs
"""

from compatibility_lib import Graph
from compatibility_lib import State, StateType
from compatibility_lib import Transition, TransitionType
from compatibility_lib import create_graph
import pandas as pd
import logging
import click
import os


graph_logger = logging.getLogger("GRAPH")
#graph_logger.setLevel(logging.DEBUG)
#graph_logger.setLevel(logging.INFO)
#graph_logger.setLevel(logging.WARNING)
#graph_logger.setLevel(logging.ERROR)
graph_logger.setLevel(logging.CRITICAL)

parser_logger = logging.getLogger("PARSER")
#parser_logger.setLevel(logging.DEBUG)
#parser_logger.setLevel(logging.INFO)
#parser_logger.setLevel(logging.WARNING)
#parser_logger.setLevel(logging.ERROR)
parser_logger.setLevel(logging.CRITICAL)

# create logger
logger = logging.getLogger("COMPATIBILITY")
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.INFO)
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

data_type_exception = {
    "base64Binary":"string"
}


def num_of_unshare(data_types1:list, data_types2:list):
    unshares = list(set(data_types1).symmetric_difference(set(data_types2)))
    logger.debug("list of unshare data type: {}".format(unshares))
    return len(unshares)


def calculate_lab_comp(transition1:Transition, transition2:Transition) -> float:
    logger.info("")
    logger.info("x-------------------------------------------------------------x")
    logger.info("calculate lab_comp({},{})".format(transition1.name, transition2.name))
    datatypes1 = transition1.get_data_types()
    datatypes2 = transition2.get_data_types()
    
    logger.debug("list of datatypes in message = {}: {}".format(transition1.name, datatypes1))
    logger.debug("list of datatypes in message = {}: {}".format(transition2.name,datatypes2))
    
    if transition1.name == transition2.name and transition1.type != transition2.type:
        num_of_unshare_type = num_of_unshare(datatypes1, datatypes2)
        logger.debug("lab_comp = 1 - ({}/6*({} + {}))".format(num_of_unshare_type,
                                                                    len(transition1.params),
                                                                    len(transition2.params)))
        
        if len(transition1.params) > 0 or len(transition2.params) > 0:
            lab_comp = 1 - (num_of_unshare_type/(6*(len(transition1.params) + len(transition2.params))))
        else:
            lab_comp = 1
    else:
        lab_comp = 0
    
    logger.info(" lab_comp = {}".format(lab_comp))
    logger.info("")
    return lab_comp

def calculate_best_sum_compatibility(emissions:list, receptions:list, last_comp_matrix:pd.DataFrame) -> float:
    sum = 0
    for emission in emissions:
        #0 is OK because we dont have negative value
        max = 0
        for recepition in receptions:
            lab_comp = calculate_lab_comp(emission, recepition)
            
            if recepition.next_state in last_comp_matrix.index:
                previous_comp = last_comp_matrix.loc[recepition.next_state, emission.next_state]
            else:
                previous_comp = last_comp_matrix.loc[emission.next_state, recepition.next_state]
            
            temp = lab_comp*previous_comp
            logger.debug("lab*comp({},{}) = {}".format(emission.name, recepition.name, temp))
            if temp > max:
                max = temp
                logger.debug("current max = {}".format(max))
            else:
                # do nothing
                pass
        sum += max

    logger.info("best sum = {}".format(sum))
    return sum


def calculate_fw_propation(state1: State,
                           state2: State, 
                           obs_comp_state1_state2: float, 
                           graph1:Graph,
                           graph2:Graph,  
                           last_comp_matrix:pd.DataFrame)-> float:
    logger.info("")
    logger.info("x-------------------------------------------------------------x")
    d_fw_1 = 0
    d_fw_2 = 0
    if state1.get_outgoing_tau_list() == []:
        logger.info("state = {} has no tau".format(state1.get_name()))
        d_fw_1 = obs_comp_state1_state2
    else:
        raise Exception("tau calculation is not yet supported")
    
    if state2.get_outgoing_tau_list() == []:
        logger.info("state = {} has no tau".format(state2.get_name()))
        d_fw_2 = obs_comp_state1_state2
    else:
        raise Exception("tau calculation is not yet supported")
    
    fw_propagation = (d_fw_1 + d_fw_2)/2
    logger.info("fw_propation({},{}) = {}".format(state1.get_name(), state2.get_name(), fw_propagation))
    
    return fw_propagation
    
    
def calculate_bw_propation(state1: State,
                           state2: State, 
                           obs_comp_state1_state2: float, 
                           graph1:Graph,
                           graph2:Graph,  
                           last_comp_matrix:pd.DataFrame)-> float:
    logger.info("")
    logger.info("x-------------------------------------------------------------x")
    d_bw_1 = 0
    d_bw_2 = 0
    if state1.get_imcoming_tau_list() == []:
        logger.info("state = {} has no tau".format(state1.get_name()))
        d_bw_1 = obs_comp_state1_state2
    else:
        raise Exception("tau calculation is not yet supported")
    
    if state2.get_imcoming_tau_list() == []:
        logger.info("state = {} has no tau".format(state2.get_name()))
        d_bw_2 = obs_comp_state1_state2
    else:
        raise Exception("tau calculation is not yet supported")
    
    bw_propagation = (d_bw_1 + d_bw_2)/2
    logger.info("bw_propation({},{}) = {}".format(state1.get_name(), state2.get_name(), bw_propagation))
    
    return bw_propagation


def calculate_obs_comp(state1:State, state2:State, last_comp_matrix:pd.DataFrame) -> float:
    logger.info("obs_comp({},{})".format(state1.get_name(), state2.get_name()))
    sum1 = 0
    sum2 = 0
    if len(state1.get_outgoing_emission_list()) and len(state2.get_outgoing_reception_list()) > 0:   
        sum1 = calculate_best_sum_compatibility(state1.get_outgoing_emission_list(),
                                                state2.get_outgoing_reception_list(),
                                                last_comp_matrix)
    else:
        logger.debug("{} has no emission".format(state1.get_name()))
    
    if len(state2.get_outgoing_emission_list()) and len(state1.get_outgoing_reception_list()) > 0:   
        sum2 = calculate_best_sum_compatibility(state2.get_outgoing_emission_list(),
                                                state1.get_outgoing_reception_list(),
                                                last_comp_matrix)
    else:
        logger.debug("{} has no emission".format(state2.get_name()))
        
    if len(state1.get_outgoing_emission_list()) > 0 or len(state2.get_outgoing_emission_list()) > 0:
        obs_comp = (sum1 + sum2)/(len(state1.get_outgoing_emission_list()) + len(state2.get_outgoing_emission_list()))
        logger.debug("obs_comp = ({} + {}) / ({} + {})".format(sum1,
                                                sum2,
                                                len(state1.get_outgoing_emission_list()),
                                                len(state2.get_outgoing_emission_list())))
        
    elif (state1._type == StateType.FINAL) and (state2._type == StateType.FINAL):
        obs_comp = 1
        logger.info("Final state -> obs_comp = {}".format(obs_comp))
    else:
        obs_comp = 0
        logger.info("both states have no emission transition => obs_comp = {}".format(obs_comp))

    logger.info("obs_comp = {}".format(obs_comp))
    
    return obs_comp
    

def calculate_state_nature(state1:State, state2:State) -> float:
    if state1._type == state2._type:
        return 1
    else:
        return 0

def calculate_w1_w2_w3(state1:State, state2:State) -> tuple:
    w1 = 0
    w2 = 0
    w3 = 0
    
    if (state1.get_imcoming_tau_list() == [] and state2.get_imcoming_tau_list() == [] and
        state1.get_outgoing_tau_list() == [] and state2.get_outgoing_tau_list() == []):
        w3 = 1
    else:
        raise Exception("tau is not supported")
 
    w1 = len(state1.get_outgoing_transitions_list()) + len(state2.get_outgoing_transitions_list())
    w2 = len(state1.get_incoming_transitions_list()) + len(state2.get_incoming_transitions_list())
    
    logger.info("w1 = {}, w2 = {}, w3 = {}".format(w1, w2, w3))
    
    return (w1, w2, w3)

def calculate_w1_w2_w3_ver2(state1:State, state2:State) -> tuple:
    num_of_best_matching_outgoing = 0
    num_of_best_matching_incomming = 0
    w3 = 0
    logger.info("calculate_w1_w2_w3_ver2({},{})".format(state1.get_name(),state2.get_name() ))
    
    for incoming1 in state1.get_incoming_transitions_list():
        for incoming2 in state2.get_incoming_transitions_list():
            logger.debug("    Checking({}-{},{}-{})".format(incoming1.name,
                                                            incoming1.type,
                                                            incoming2.name,
                                                            incoming2.type))
            
            if incoming1.name == incoming2.name and incoming1.type != incoming2.type:
                logger.debug("    -->best matching incoming found({},{})".format(incoming1.name,incoming2.name ))
                num_of_best_matching_incomming += 1
            
    for outgoing1 in state1.get_outgoing_transitions_list():
        for outgoing2 in state2.get_outgoing_transitions_list():
            logger.debug("    Checking({}-{},{}-{})".format(outgoing1.name,
                                                            outgoing1.type,
                                                            outgoing2.name,
                                                            outgoing2.type))
            if outgoing1.name == outgoing2.name and outgoing1.type != outgoing2.type:
                logger.debug("    -->best matching outgoing found({},{})".format(outgoing1.name,outgoing2.name ))
                num_of_best_matching_outgoing += 1

    if (state1.get_imcoming_tau_list() == [] and state2.get_imcoming_tau_list() == [] and
        state1.get_outgoing_tau_list() == [] and state2.get_outgoing_tau_list() == []):
        w3 = 1
    else:
        raise Exception("tau is not supported")
    
    logger.info("w1 = {}, w2 = {}, w3 = {}".format(num_of_best_matching_outgoing, num_of_best_matching_incomming, w3))
    return(num_of_best_matching_outgoing,num_of_best_matching_incomming, w3)
                
                

def create_default_comp_matrix(graph1:Graph, graph2:Graph):
    data = {}
    index = []
    num_of_colunm = len(graph1.get_states_list())
    num_of_rows = len(graph2.get_states_list())
    
    logger.info("matrix has the size = {}x{}".format(num_of_rows, num_of_colunm))
    
    #Build the data
    for state in graph1.get_states_list():
        data.update({state.get_name():[1] * num_of_rows})
    
    #build the row name
    for state in graph2.get_states_list():
        index.append(state.get_name())
    
    comp_matrix = pd.DataFrame(data, index=index)
    return comp_matrix


def calculate_compatibility(graph1:Graph, graph2:Graph, last_comp_matrix:pd.DataFrame = None) ->pd.DataFrame:
    if last_comp_matrix is None:
        logger.info("Initial data matrix, set everything to 1")
        return create_default_comp_matrix(graph1, graph2)
    else:
        starting_matrix = create_default_comp_matrix(graph1, graph2)
        for state1 in graph1.get_states_list():
            for state2 in graph2.get_states_list():
                logger.info("")
                logger.info("####################################################################")
                logger.info("#")
                logger.info("# Compatibillity ({},{})".format(state1.get_name(), state2.get_name()))
                logger.info("#")
                logger.info("####################################################################")
                logger.info("")
                
                obs_comp = calculate_obs_comp(state1, state2, last_comp_matrix)
                fw_propagation = calculate_fw_propation(state1, state2, obs_comp, graph1, graph2, last_comp_matrix)
                bw_propagation = calculate_bw_propation(state1, state2, obs_comp, graph1, graph2, last_comp_matrix)

                w1,w2,w3 = calculate_w1_w2_w3(state1, state2)
                
                #below calculation is unused
                #w1,w2,w3 = calculate_w1_w2_w3_ver2(state1, state2)

                logger.info("")
                logger.info("=== CONCLUCSION ===")
                state_comp = (w1*fw_propagation + w2*bw_propagation + w3*calculate_state_nature(state1, state2))/(w1 + w2 + w3)
                logger.info("state_comp({},{}) = {}".format(state1.get_name(), state2.get_name(), state_comp))
                
                compatibility = (last_comp_matrix.loc[state2.get_name(), state1.get_name()] + state_comp)/2
                logger.info("comp({},{}) = {}".format(state1.get_name(), state2.get_name(), compatibility))
                
                starting_matrix.loc[state2.get_name(), state1.get_name()] = round(compatibility,3)
                
        return starting_matrix


def main():
    ocpp_graph = create_graph("ocpp.json")
    iso15118_graph = create_graph("iso_15118.json")
    
    iso15118_graph.print_graph()
    ocpp_graph.print_graph()
    
    comp_maxtrix_1 = calculate_compatibility(iso15118_graph, ocpp_graph, None)
    
    logger.info("compatibility matrix at iteration 0: ")
    print(comp_maxtrix_1.to_string())
    
    comp_maxtrix_2 = calculate_compatibility(iso15118_graph, ocpp_graph, comp_maxtrix_1)
    print(comp_maxtrix_2.to_string())
    
@click.command()
@click.option("--graph", nargs = 2, help="path to the json file containing the graph")
@click.option("--iterate", help="number of iteration", default = 1)
@click.option("--output", help="file to store the calculation", default = "result.txt")
@click.option("--log_level", help="logging level: info, debug, or none", default = "none")
def compatibility_calculation(graph, iterate, output, log_level):
    if log_level == "none":
        logger.setLevel(logging.CRITICAL)
    elif log_level == "info":
        logger.setLevel(logging.INFO)
    elif log_level == "debug":
        logger.setLevel(logging.DEBUG)
    else:
        pass
      
    if(len(graph) != 2):
        logger.error("Invalid number of graph. Must be 2")
    else:
        path1, path2 = graph
        
        graph1 = create_graph(path1)
        graph2 = create_graph(path2)
        
        #Fancy banner
        print("")
        print("")
        print("#################################################################")
        print("#")
        print("# Compatibility Calculation")
        print("# Author: {}".format(__author__))
        print("# Version: {}".format(__version__))
        print("# Status: {}".format(__status__))
        print("#")
        print("#################################################################")
        
        print("")
        print("GRAPHS GENERATION REPORT")
        print("")
        graph1.print_graph()
        print("")
        graph2.print_graph()
        print("")
        
        compatible_matrices = []
        
        for i in range(iterate + 1):
            if i == 0:
                compatible_matrices.append(calculate_compatibility(graph1, graph2, None))
            else:
                compatible_matrices.append(calculate_compatibility(graph1, graph2, compatible_matrices[i - 1]))

        if os.path.isfile(output) == True:
            os.remove(output)
            
        
        print("Compatibility calculation is complete. The result is exported to {}".format)
        print("Results:")
        with open(output, "a") as file:
            for i in range(len(compatible_matrices)):
                print("For iterate = {}\n".format(i))
                print(compatible_matrices[i].to_string())
                print("")
                print("")
                
                file.write("For iterate = {}\n".format(i))
                file.write(compatible_matrices[i].to_string())
                file.write("\n\n")
                
        
        
        
if __name__ == "__main__":
    compatibility_calculation()

                
                    