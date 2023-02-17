# Design specification

## Interface

The command line interface is use to start the analysis. The arguments for the
script are: graph - location to the file describing the graph and number of
iteration. The application supports only 2 graphs so it accept exactly 2 graphs.

## Input file to describe the state

The input file describing the graph is in json format. JSON format works in the
basis of 'property':'value', which is suitable for describing for the graph.
JSON is also suitable if an GUI will be built later.

The JSON file has the following template/format

```
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
```

### STATE_TYPE data type
The value STATE_TYPE is an enumeration string having the value "init", "final", or "normal".

### TRANSITION_TYPE data types
The value  TRANSITION_TYPE is an enumeration string having the value "emission", "reception", or "tau".


## Requirements of the input file
| ID           | Description                                                                               |Impl |
|--------------|-------------------------------------------------------------------------------------------|-----|
|INPUT_0001    |The property of the input file MUST be written in snake_case.                              |     |
|INPUT_0002    |The input file MUST have property "graph_name".                                            |     |
|INPUT_0003    |The property "states" MUST have MINIMUM one state.                                         |     |
|INPUT_0004    |Each state MUST have the property "state_name".                                            |     |
|INPUT_0004    |Value of the property "state_name" MUST be unique among the states                         |     |
|INPUT_0005    |Each state MUST have property "type"                                                       |     |
|INPUT_0006    |Property "stat_type" MUST have data type enumeration                                       |     |
|INPUT_0007    |the property "transition" MUST have MINIMUM one transition                                 |     |
|INPUT_0008    |Each transition MUST have the properties "transition_name", "transition_type", "next_state"|     |
|INPUT_0009    |The property "params" MAY be empty                                                         |     |
|INPUT_0010    |The value of the property "transition_name" MUST be unique among the transitions           |     |
|INPUT_0011    |The value of the property "next_state" MUST be the value of the property "state_name"      |     |
|INPUT_0012    |The value of the property "params" MUST have the format param_name:data_type               |     |
|INPUT_0014    |WHEN the property "transition_type" is tau, params" MUST be empty                          |     |

## Data validation and covert to python data type.

The application uses json module tp decode the data from json to dictinary. To
make it easier to work with, instead of using directly dictionary data type, the
application validates if the input data is correct according to the requirements
INPUT_XXXX, the convert the keys of the dictionaty to corresponding classes.


### Data type

#### Transition class

The Transition class has the following properties:

```
transition_name:string
transtion_type:enum
params:list(string)
next_state:string
```

The Transition class has the following methods:

```
get_param_name(param_str)
get_param_data_type(param_str)
```

#### State class
The State class has the following properties:

```
state_name:string
state_type:enum
incoming_transition:list(Transition)
outgoing_Transition:list(Transition)
```

The State class has the following methods:

```
add_incoming_transition(Transition)
add_outgoing_transition(Transition)
get_incoming_transition(name:string or index:int) -> Transition
get_outgoing_transition(name:string or index:int) -> Transition
get_incoming_transition_list() -> list(string)
get_outgoing_transition_list() -> list(string)
is_state_final() -> bool
is_state_int() -> bool
```


#### Graph class

The Graph class has the following properties:

```
graph_name:string
graph_state:list(State)
```

The Graph class has the following methods:

```
add_state(State)
get_state(name:string or index:int) -> State
get_state_list() -> list(string)
```

### Validation

For each graph, the following conditions must be check:

* graph_name is existing. If not, raise error.
* states is existing. If not raise error.
* states has type list and number of element is more than 0. If not, raise error.

If the above conditions are OK, a graph object is created

For each state, the following conditions must be check:

* state_name is existing. If not, raise error.
* state_type is existing. The value of state_type is the defined enum string. If
not, raise error.
* transition is existing. If not raise error.
* transition is a list and has more than 0 element. If not raise error.

If the above conditions are satisfied, a state object is created.

For each transitions, the following conditions must be check:

* transition_name is existing. If not, raise error.
* params is existing and is a list. If not raise error.
* transition_type is existing. The value of transition_type is the defined enum string. If
not, raise error.
* If transition_type is tau, the params must by empty.
* transition is existing. If not raise error.
* next_state is existing. If not raise error.
* The value of next_state must be in the list of states. If not, raise error. 

If the above conditions are satisfied, a transition object is created. This 
object is added to the outgoing transtion list of the state it belongs to and 
added to the incoming transitions list of the state defined in next_state.

## Compatibility calculation

The compatibility calculation can be carried out only if the validation phase 
has been passed. Number of calculation iteration is based on the input from the 
CLI.

The result of the calulation is a list of compatibility matrix with the size of
the number of iteration + 1.

Each compatibility matrix is an object based on DataMatrix class. The DataMatrix
class is defined as follows:

```
matrix:list(list(DataElement))
------------------------------------------------------------
get_element_value_by_name(row_name, column_name) -> float
get_element_value_by_index(row_index, column_index) ->float
```