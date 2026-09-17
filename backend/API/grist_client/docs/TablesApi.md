# grist_client.TablesApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_tables**](TablesApi.md#add_tables) | **POST** /docs/{docId}/tables | Add tables to a document
[**list_tables**](TablesApi.md#list_tables) | **GET** /docs/{docId}/tables | List tables in a document
[**modify_tables**](TablesApi.md#modify_tables) | **PATCH** /docs/{docId}/tables | Modify tables of a document


# **add_tables**
> TablesWithoutFields add_tables(doc_id, create_tables)

Add tables to a document

### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.create_tables import CreateTables
from grist_client.models.tables_without_fields import TablesWithoutFields
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

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Configure Bearer authorization (Authorization: Bearer XXXXXXXXXXX): ApiKey
configuration = grist_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with grist_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = grist_client.TablesApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    create_tables = grist_client.CreateTables() # CreateTables | the tables to add

    try:
        # Add tables to a document
        api_response = api_instance.add_tables(doc_id, create_tables)
        print("The response of TablesApi->add_tables:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TablesApi->add_tables: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **create_tables** | [**CreateTables**](CreateTables.md)| the tables to add | 

### Return type

[**TablesWithoutFields**](TablesWithoutFields.md)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The table created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_tables**
> TablesList list_tables(doc_id, expand=expand)

List tables in a document

### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.tables_list import TablesList
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

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Configure Bearer authorization (Authorization: Bearer XXXXXXXXXXX): ApiKey
configuration = grist_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with grist_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = grist_client.TablesApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    expand = 'expand_example' # str | Set to \"column\" to include column metadata for each table in the response. (optional)

    try:
        # List tables in a document
        api_response = api_instance.list_tables(doc_id, expand=expand)
        print("The response of TablesApi->list_tables:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TablesApi->list_tables: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **expand** | **str**| Set to \&quot;column\&quot; to include column metadata for each table in the response. | [optional] 

### Return type

[**TablesList**](TablesList.md)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The tables in a document |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_tables**
> modify_tables(doc_id, update_tables)

Modify tables of a document

Modify metadata for existing tables. This endpoint is primarily useful for:
- Renaming tables (via the `tableId` field)
- Setting on-demand loading (via the `onDemand` field)


### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.update_tables import UpdateTables
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

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Configure Bearer authorization (Authorization: Bearer XXXXXXXXXXX): ApiKey
configuration = grist_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with grist_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = grist_client.TablesApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    update_tables = grist_client.UpdateTables() # UpdateTables | the tables to modify, identified by their current id

    try:
        # Modify tables of a document
        api_instance.modify_tables(doc_id, update_tables)
    except Exception as e:
        print("Exception when calling TablesApi->modify_tables: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **update_tables** | [**UpdateTables**](UpdateTables.md)| the tables to modify, identified by their current id | 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

