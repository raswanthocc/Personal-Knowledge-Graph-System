# TraversalEdge


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source** | **int** |  | 
**target** | **int** |  | 
**depth** | **int** |  | 

## Example

```python
from knowledge_sdk.models.traversal_edge import TraversalEdge

# TODO update the JSON string below
json = "{}"
# create an instance of TraversalEdge from a JSON string
traversal_edge_instance = TraversalEdge.from_json(json)
# print the JSON string representation of the object
print(TraversalEdge.to_json())

# convert the object into a dict
traversal_edge_dict = traversal_edge_instance.to_dict()
# create an instance of TraversalEdge from a dict
traversal_edge_from_dict = TraversalEdge.from_dict(traversal_edge_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


