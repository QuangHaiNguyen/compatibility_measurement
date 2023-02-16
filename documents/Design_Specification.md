# Design specification

## Interface

The command line interface is use to start the analysis. The arguments for the
script are: graph - location to the file describing the graph. The application 
suuports only 2 graphs so it accept exactly 2 graphs.

## Input file to describe the state

The input file describing the graph is in json format. JSON format works in the
basis of 'property':'value', which is suitable for describing for the graph. JSON is
also suitable if an GUI will be built later.

The JSON file has the following template/format

```
{
    "graph_name":"NAME_OF_THE_GRAPH",
    "states":
    [
        {
            "state_name":"NAME_OF_STATE",
            "type":"STATE_TYPE"
            "transitions":
            [
                {
                    "transition_name":"NAME_OF_THE_TRANSITION"
                    "type":"TRANSITION_TYPE"
                    "params":["name:data_type", "name:data_type", "name:data_type"]
                    "next_state":"NAME_OF_STATE"
                }
            ]
        },
        {
            "state_name":"NAME_OF_STATE",
            "type":"STATE_TYPE"
            "transitions":
            [
                {
                    "transition_name":"NAME_OF_THE_TRANSITION"
                    "type":"TRANSITION_TYPE"
                    "params":["name:data_type", "name:data_type", "name:data_type"]
                    "next_state":"NAME_OF_STATE"
                }
            ]
        }
    ]
}
```

## Requirements of the input file

The inpu
