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

### Transition class

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

### State class
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


### Graph class

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