# TraversalResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**start_note_id** | **int** |  | 
**start_note_title** | **str** |  | 
**method** | **str** |  | 
**direction** | **str** |  | 
**max_depth** | **int** |  | 
**total_nodes_visited** | **int** |  | 
**visited_nodes** | [**List[TraversalNode]**](TraversalNode.md) |  | 
**edges** | [**List[TraversalEdge]**](TraversalEdge.md) |  | 
**traversal_order** | **List[int]** |  | 

## Example

```python
from knowledge_sdk.models.traversal_response import TraversalResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TraversalResponse from a JSON string
traversal_response_instance = TraversalResponse.from_json(json)
# print the JSON string representation of the object
print(TraversalResponse.to_json())

# convert the object into a dict
traversal_response_dict = traversal_response_instance.to_dict()
# create an instance of TraversalResponse from a dict
traversal_response_from_dict = TraversalResponse.from_dict(traversal_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


