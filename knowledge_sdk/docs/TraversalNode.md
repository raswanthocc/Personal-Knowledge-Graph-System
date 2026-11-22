# TraversalNode


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 
**depth** | **int** |  | 
**tags** | **List[str]** |  | [optional] [default to []]

## Example

```python
from knowledge_sdk.models.traversal_node import TraversalNode

# TODO update the JSON string below
json = "{}"
# create an instance of TraversalNode from a JSON string
traversal_node_instance = TraversalNode.from_json(json)
# print the JSON string representation of the object
print(TraversalNode.to_json())

# convert the object into a dict
traversal_node_dict = traversal_node_instance.to_dict()
# create an instance of TraversalNode from a dict
traversal_node_from_dict = TraversalNode.from_dict(traversal_node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


