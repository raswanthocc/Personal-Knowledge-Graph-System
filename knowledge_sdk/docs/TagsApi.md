# knowledge_sdk.TagsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_domain_areas_tags_areas_get**](TagsApi.md#get_domain_areas_tags_areas_get) | **GET** /tags/areas/ | Get core domain areas
[**tag_suggestions_tags_suggestions_get**](TagsApi.md#tag_suggestions_tags_suggestions_get) | **GET** /tags/suggestions/ | Get tag suggestions


# **get_domain_areas_tags_areas_get**
> TagSuggestionResponse get_domain_areas_tags_areas_get()

Get core domain areas

Returns list of main topical areas for selective coverage dropdown.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.tag_suggestion_response import TagSuggestionResponse
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
    api_instance = knowledge_sdk.TagsApi(api_client)

    try:
        # Get core domain areas
        api_response = api_instance.get_domain_areas_tags_areas_get()
        print("The response of TagsApi->get_domain_areas_tags_areas_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TagsApi->get_domain_areas_tags_areas_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**TagSuggestionResponse**](TagSuggestionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tag_suggestions_tags_suggestions_get**
> TagSuggestionResponse tag_suggestions_tags_suggestions_get(query=query)

Get tag suggestions

Provides autocomplete suggestions from existing normalized tags.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.tag_suggestion_response import TagSuggestionResponse
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
    api_instance = knowledge_sdk.TagsApi(api_client)
    query = 'query_example' # str | Prefix or search query for tag (optional)

    try:
        # Get tag suggestions
        api_response = api_instance.tag_suggestions_tags_suggestions_get(query=query)
        print("The response of TagsApi->tag_suggestions_tags_suggestions_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TagsApi->tag_suggestions_tags_suggestions_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **query** | **str**| Prefix or search query for tag | [optional] 

### Return type

[**TagSuggestionResponse**](TagSuggestionResponse.md)

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

