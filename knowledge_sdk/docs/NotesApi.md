# knowledge_sdk.NotesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_note_notes_post**](NotesApi.md#create_note_notes_post) | **POST** /notes/ | Create a new note
[**get_note_by_id_notes_note_id_get**](NotesApi.md#get_note_by_id_notes_note_id_get) | **GET** /notes/{note_id} | Get note details
[**get_notes_notes_get**](NotesApi.md#get_notes_notes_get) | **GET** /notes/ | Get all notes
[**link_note_notes_note_id_link_patch**](NotesApi.md#link_note_notes_note_id_link_patch) | **PATCH** /notes/{note_id}/link | Create a link from one note to another


# **create_note_notes_post**
> NoteDetailResponse create_note_notes_post(note_create)

Create a new note

Creates a note with title, markdown content, and tags. Resolves [[Wiki Links]] and tags automatically.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_create import NoteCreate
from knowledge_sdk.models.note_detail_response import NoteDetailResponse
from knowledge_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = knowledge_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with knowledge_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_create = knowledge_sdk.NoteCreate() # NoteCreate | 

    try:
        # Create a new note
        api_response = api_instance.create_note_notes_post(note_create)
        print("The response of NotesApi->create_note_notes_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->create_note_notes_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_create** | [**NoteCreate**](NoteCreate.md)|  | 

### Return type

[**NoteDetailResponse**](NoteDetailResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_note_by_id_notes_note_id_get**
> NoteDetailResponse get_note_by_id_notes_note_id_get(note_id)

Get note details

Retrieve detailed information about a note, including outgoing linked notes and incoming backlinks.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_detail_response import NoteDetailResponse
from knowledge_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = knowledge_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with knowledge_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_id = 56 # int | 

    try:
        # Get note details
        api_response = api_instance.get_note_by_id_notes_note_id_get(note_id)
        print("The response of NotesApi->get_note_by_id_notes_note_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->get_note_by_id_notes_note_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**|  | 

### Return type

[**NoteDetailResponse**](NoteDetailResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_notes_notes_get**
> List[NoteListItem] get_notes_notes_get(tag=tag, keyword=keyword)

Get all notes

Retrieve all notes, with optional filtering by tag or keyword search in title/content.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.note_list_item import NoteListItem
from knowledge_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = knowledge_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with knowledge_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = knowledge_sdk.NotesApi(api_client)
    tag = 'tag_example' # str | Filter by tag name (e.g. 'productivity') (optional)
    keyword = 'keyword_example' # str | Search keyword in title or content (optional)

    try:
        # Get all notes
        api_response = api_instance.get_notes_notes_get(tag=tag, keyword=keyword)
        print("The response of NotesApi->get_notes_notes_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->get_notes_notes_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tag** | **str**| Filter by tag name (e.g. &#39;productivity&#39;) | [optional] 
 **keyword** | **str**| Search keyword in title or content | [optional] 

### Return type

[**List[NoteListItem]**](NoteListItem.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **link_note_notes_note_id_link_patch**
> LinkResponse link_note_notes_note_id_link_patch(note_id, link_create)

Create a link from one note to another

Creates a directed link from note_id (source) to target_id (target). Rejects self-loops and duplicates.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.link_create import LinkCreate
from knowledge_sdk.models.link_response import LinkResponse
from knowledge_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = knowledge_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with knowledge_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = knowledge_sdk.NotesApi(api_client)
    note_id = 56 # int | 
    link_create = knowledge_sdk.LinkCreate() # LinkCreate | 

    try:
        # Create a link from one note to another
        api_response = api_instance.link_note_notes_note_id_link_patch(note_id, link_create)
        print("The response of NotesApi->link_note_notes_note_id_link_patch:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling NotesApi->link_note_notes_note_id_link_patch: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**|  | 
 **link_create** | [**LinkCreate**](LinkCreate.md)|  | 

### Return type

[**LinkResponse**](LinkResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

