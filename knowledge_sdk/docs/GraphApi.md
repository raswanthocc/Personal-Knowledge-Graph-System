# knowledge_sdk.GraphApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_graph_graph_get**](GraphApi.md#get_graph_graph_get) | **GET** /graph/ | Get note-link graph
[**traverse_graph_graph_traverse_note_id_get**](GraphApi.md#traverse_graph_graph_traverse_note_id_get) | **GET** /graph/traverse/{note_id} | BFS / DFS Graph Traversal


# **get_graph_graph_get**
> GraphResponse get_graph_graph_get()

Get note-link graph

Returns the full knowledge network as nodes and edges for Cytoscape, D3, or other graph visualizers.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.graph_response import GraphResponse
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
    api_instance = knowledge_sdk.GraphApi(api_client)

    try:
        # Get note-link graph
        api_response = api_instance.get_graph_graph_get()
        print("The response of GraphApi->get_graph_graph_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GraphApi->get_graph_graph_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GraphResponse**](GraphResponse.md)

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

# **traverse_graph_graph_traverse_note_id_get**
> TraversalResponse traverse_graph_graph_traverse_note_id_get(note_id, method=method, max_depth=max_depth, direction=direction)

BFS / DFS Graph Traversal

Performs Breadth-First Search (BFS) or Depth-First Search (DFS) starting from a specific note, tracking visited depth, traversed edges, and cycle prevention.

### Example


```python
import knowledge_sdk
from knowledge_sdk.models.traversal_response import TraversalResponse
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
    api_instance = knowledge_sdk.GraphApi(api_client)
    note_id = 56 # int | Root note ID to begin traversal from
    method = 'bfs' # str | Traversal algorithm: 'bfs' or 'dfs' (optional) (default to 'bfs')
    max_depth = 3 # int | Maximum traversal depth from starting note (optional) (default to 3)
    direction = 'outgoing' # str | Link direction: 'outgoing', 'incoming', or 'both' (optional) (default to 'outgoing')

    try:
        # BFS / DFS Graph Traversal
        api_response = api_instance.traverse_graph_graph_traverse_note_id_get(note_id, method=method, max_depth=max_depth, direction=direction)
        print("The response of GraphApi->traverse_graph_graph_traverse_note_id_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GraphApi->traverse_graph_graph_traverse_note_id_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **note_id** | **int**| Root note ID to begin traversal from | 
 **method** | **str**| Traversal algorithm: &#39;bfs&#39; or &#39;dfs&#39; | [optional] [default to &#39;bfs&#39;]
 **max_depth** | **int**| Maximum traversal depth from starting note | [optional] [default to 3]
 **direction** | **str**| Link direction: &#39;outgoing&#39;, &#39;incoming&#39;, or &#39;both&#39; | [optional] [default to &#39;outgoing&#39;]

### Return type

[**TraversalResponse**](TraversalResponse.md)

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

