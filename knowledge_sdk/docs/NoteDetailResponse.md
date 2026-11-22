# NoteDetailResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**title** | **str** |  | 
**content** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**tags** | **List[str]** |  | [optional] [default to []]
**linked_notes** | [**List[NoteSummary]**](NoteSummary.md) | Outgoing notes linked from this note | [optional] 
**backlinks** | [**List[NoteSummary]**](NoteSummary.md) | Incoming notes linking to this note | [optional] 

## Example

```python
from knowledge_sdk.models.note_detail_response import NoteDetailResponse

# TODO update the JSON string below
json = "{}"
# create an instance of NoteDetailResponse from a JSON string
note_detail_response_instance = NoteDetailResponse.from_json(json)
# print the JSON string representation of the object
print(NoteDetailResponse.to_json())

# convert the object into a dict
note_detail_response_dict = note_detail_response_instance.to_dict()
# create an instance of NoteDetailResponse from a dict
note_detail_response_from_dict = NoteDetailResponse.from_dict(note_detail_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


