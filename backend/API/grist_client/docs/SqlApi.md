# grist_client.SqlApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**run_sql**](SqlApi.md#run_sql) | **POST** /docs/{docId}/sql | Run an SQL query against a document, with options or parameters
[**run_sql_get**](SqlApi.md#run_sql_get) | **GET** /docs/{docId}/sql | Run an SQL query against a document


# **run_sql**
> SqlResultSet run_sql(doc_id, run_sql_request=run_sql_request)

Run an SQL query against a document, with options or parameters

Execute a read-only SQL SELECT query with support for parameterized queries
and custom timeouts. All Grist documents are SQLite databases, and queries
are executed directly against SQLite with security restrictions.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.run_sql_request import RunSqlRequest
from grist_client.models.sql_result_set import SqlResultSet
from grist_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://10.19.22.91:8484/api
# See configuration.py for a list of all supported configuration parameters.
configuration = grist_client.Configuration(
    host = "http://10.19.22.91:8484/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (Authorization: Bearer XXXXXXXXXXX): ApiKey
configuration = grist_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with grist_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = grist_client.SqlApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    run_sql_request = grist_client.RunSqlRequest() # RunSqlRequest | Query options (optional)

    try:
        # Run an SQL query against a document, with options or parameters
        api_response = api_instance.run_sql(doc_id, run_sql_request=run_sql_request)
        print("The response of SqlApi->run_sql:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SqlApi->run_sql: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **run_sql_request** | [**RunSqlRequest**](RunSqlRequest.md)| Query options | [optional] 

### Return type

[**SqlResultSet**](SqlResultSet.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result set for the query. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **run_sql_get**
> SqlResultSet run_sql_get(doc_id, q=q)

Run an SQL query against a document

Execute a read-only SQL SELECT query against the document's SQLite database.
This is a simplified endpoint for basic queries. For queries with parameters
or custom timeouts, use the POST endpoint instead.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.sql_result_set import SqlResultSet
from grist_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://10.19.22.91:8484/api
# See configuration.py for a list of all supported configuration parameters.
configuration = grist_client.Configuration(
    host = "http://10.19.22.91:8484/api"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization (Authorization: Bearer XXXXXXXXXXX): ApiKey
configuration = grist_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with grist_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = grist_client.SqlApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    q = 'q_example' # str |  (optional)

    try:
        # Run an SQL query against a document
        api_response = api_instance.run_sql_get(doc_id, q=q)
        print("The response of SqlApi->run_sql_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SqlApi->run_sql_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **q** | **str**|  | [optional] 

### Return type

[**SqlResultSet**](SqlResultSet.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result set for the query. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

