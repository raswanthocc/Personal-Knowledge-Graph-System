# LinkResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_id** | **int** |  | 
**target_id** | **int** |  | 
**message** | **str** |  | [optional] [default to 'Link established successfully']

## Example

```python
from knowledge_sdk.models.link_response import LinkResponse

# TODO update the JSON string below
json = "{}"
# create an instance of LinkResponse from a JSON string
link_response_instance = LinkResponse.from_json(json)
# print the JSON string representation of the object
print(LinkResponse.to_json())

# convert the object into a dict
link_response_dict = link_response_instance.to_dict()
# create an instance of LinkResponse from a dict
link_response_from_dict = LinkResponse.from_dict(link_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


