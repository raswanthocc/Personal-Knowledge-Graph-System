# TagSuggestionResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tags** | **List[str]** |  | 

## Example

```python
from knowledge_sdk.models.tag_suggestion_response import TagSuggestionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TagSuggestionResponse from a JSON string
tag_suggestion_response_instance = TagSuggestionResponse.from_json(json)
# print the JSON string representation of the object
print(TagSuggestionResponse.to_json())

# convert the object into a dict
tag_suggestion_response_dict = tag_suggestion_response_instance.to_dict()
# create an instance of TagSuggestionResponse from a dict
tag_suggestion_response_from_dict = TagSuggestionResponse.from_dict(tag_suggestion_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


