# grist_client.DataApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_rows**](DataApi.md#add_rows) | **POST** /docs/{docId}/tables/{tableId}/data | Add rows to a table
[**delete_rows**](DataApi.md#delete_rows) | **POST** /docs/{docId}/tables/{tableId}/data/delete | Delete rows of a table
[**get_table_data**](DataApi.md#get_table_data) | **GET** /docs/{docId}/tables/{tableId}/data | Fetch data from a table
[**modify_rows**](DataApi.md#modify_rows) | **PATCH** /docs/{docId}/tables/{tableId}/data | Modify rows of a table


# **add_rows**
> List[int] add_rows(doc_id, table_id, request_body, noparse=noparse)

Add rows to a table

Deprecated in favor of `records` endpoints. We have no immediate plans to remove these endpoints, but consider `records` a better starting point for new projects.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
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
    api_instance = grist_client.DataApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    request_body = None # Dict[str, List[object]] | the data to add
    noparse = True # bool | Set to true to prohibit parsing strings according to the column type. (optional)

    try:
        # Add rows to a table
        api_response = api_instance.add_rows(doc_id, table_id, request_body, noparse=noparse)
        print("The response of DataApi->add_rows:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->add_rows: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**| normalized table name (see &#x60;TABLE ID&#x60; in Raw Data) or numeric row ID in &#x60;_grist_Tables&#x60; | 
 **request_body** | [**Dict[str, List[object]]**](List.md)| the data to add | 
 **noparse** | **bool**| Set to true to prohibit parsing strings according to the column type. | [optional] 

### Return type

**List[int]**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | IDs of rows added |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_rows**
> delete_rows(doc_id, table_id, request_body)

Delete rows of a table

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
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
    api_instance = grist_client.DataApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    request_body = [56] # List[int] | the IDs of rows to remove

    try:
        # Delete rows of a table
        api_instance.delete_rows(doc_id, table_id, request_body)
    except Exception as e:
        print("Exception when calling DataApi->delete_rows: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**| normalized table name (see &#x60;TABLE ID&#x60; in Raw Data) or numeric row ID in &#x60;_grist_Tables&#x60; | 
 **request_body** | [**List[int]**](int.md)| the IDs of rows to remove | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Nothing returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_table_data**
> Data get_table_data(doc_id, table_id, filter=filter, sort=sort, limit=limit, x_sort=x_sort, x_limit=x_limit, cell_format=cell_format)

Fetch data from a table

Deprecated in favor of `records` endpoints. We have no immediate plans to remove these endpoints, but consider `records` a better starting point for new projects.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.data import Data
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
    api_instance = grist_client.DataApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    filter = '{\"pet\": [\"cat\", \"dog\"]}' # str | This is a JSON object mapping column names to arrays of allowed values.  For example, to filter column `pet` for values `cat` and `dog`, the filter would be `{\"pet\": [\"cat\", \"dog\"]}`. JSON contains characters that are not safe to place in a URL, so it is important to url-encode them.  For this example, the url-encoding is `%7B%22pet%22%3A%20%5B%22cat%22%2C%20%22dog%22%5D%7D`. See https://rosettacode.org/wiki/URL_encoding for how to url-encode a string, or https://www.urlencoder.org/ to try some examples. Multiple columns can be filtered. For example the filter for `pet` being either `cat` or `dog`, AND `size` being either `tiny` or `outrageously small`, would be `{\"pet\": [\"cat\", \"dog\"], \"size\": [\"tiny\", \"outrageously small\"]}`. (optional)
    sort = 'pet,-age' # str | Order in which to return results. If a single column name is given (e.g. `pet`), results are placed in ascending order of values in that column. To get results in an order that was previously prepared manually in Grist, use the special `manualSort` column name. Multiple columns can be specified, separated by commas (e.g. `pet,age`). For descending order, prefix a column name with a `-` character (e.g. `pet,-age`). To include additional sorting options append them after a colon (e.g. `pet,-age:naturalSort;emptyLast,owner`). Available options are: `orderByChoice`, `naturalSort`, `emptyLast`. Without the `sort` parameter, the order of results is unspecified. (optional)
    limit = 5 # float | Return at most this number of rows.  A value of 0 is equivalent to having no limit. (optional)
    x_sort = 'pet,-age' # str | Same as `sort` query parameter. (optional)
    x_limit = 5 # float | Same as `limit` query parameter. (optional)
    cell_format = 'cell_format_example' # str | With \"typed\", every cell value is returned in a self-describing typed form, e.g. a Date as `[\"d\", timestamp]` and a Reference as `[\"R\", tableId, rowId]`, and formula errors are returned inline as `[\"E\", ...]` values. The default \"normal\" format uses compact values whose interpretation depends on the column type. See [Grist data format](https://github.com/gristlabs/grist-core/blob/main/documentation/grist-data-format.md) for details. (optional)

    try:
        # Fetch data from a table
        api_response = api_instance.get_table_data(doc_id, table_id, filter=filter, sort=sort, limit=limit, x_sort=x_sort, x_limit=x_limit, cell_format=cell_format)
        print("The response of DataApi->get_table_data:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->get_table_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**| normalized table name (see &#x60;TABLE ID&#x60; in Raw Data) or numeric row ID in &#x60;_grist_Tables&#x60; | 
 **filter** | **str**| This is a JSON object mapping column names to arrays of allowed values.  For example, to filter column &#x60;pet&#x60; for values &#x60;cat&#x60; and &#x60;dog&#x60;, the filter would be &#x60;{\&quot;pet\&quot;: [\&quot;cat\&quot;, \&quot;dog\&quot;]}&#x60;. JSON contains characters that are not safe to place in a URL, so it is important to url-encode them.  For this example, the url-encoding is &#x60;%7B%22pet%22%3A%20%5B%22cat%22%2C%20%22dog%22%5D%7D&#x60;. See https://rosettacode.org/wiki/URL_encoding for how to url-encode a string, or https://www.urlencoder.org/ to try some examples. Multiple columns can be filtered. For example the filter for &#x60;pet&#x60; being either &#x60;cat&#x60; or &#x60;dog&#x60;, AND &#x60;size&#x60; being either &#x60;tiny&#x60; or &#x60;outrageously small&#x60;, would be &#x60;{\&quot;pet\&quot;: [\&quot;cat\&quot;, \&quot;dog\&quot;], \&quot;size\&quot;: [\&quot;tiny\&quot;, \&quot;outrageously small\&quot;]}&#x60;. | [optional] 
 **sort** | **str**| Order in which to return results. If a single column name is given (e.g. &#x60;pet&#x60;), results are placed in ascending order of values in that column. To get results in an order that was previously prepared manually in Grist, use the special &#x60;manualSort&#x60; column name. Multiple columns can be specified, separated by commas (e.g. &#x60;pet,age&#x60;). For descending order, prefix a column name with a &#x60;-&#x60; character (e.g. &#x60;pet,-age&#x60;). To include additional sorting options append them after a colon (e.g. &#x60;pet,-age:naturalSort;emptyLast,owner&#x60;). Available options are: &#x60;orderByChoice&#x60;, &#x60;naturalSort&#x60;, &#x60;emptyLast&#x60;. Without the &#x60;sort&#x60; parameter, the order of results is unspecified. | [optional] 
 **limit** | **float**| Return at most this number of rows.  A value of 0 is equivalent to having no limit. | [optional] 
 **x_sort** | **str**| Same as &#x60;sort&#x60; query parameter. | [optional] 
 **x_limit** | **float**| Same as &#x60;limit&#x60; query parameter. | [optional] 
 **cell_format** | **str**| With \&quot;typed\&quot;, every cell value is returned in a self-describing typed form, e.g. a Date as &#x60;[\&quot;d\&quot;, timestamp]&#x60; and a Reference as &#x60;[\&quot;R\&quot;, tableId, rowId]&#x60;, and formula errors are returned inline as &#x60;[\&quot;E\&quot;, ...]&#x60; values. The default \&quot;normal\&quot; format uses compact values whose interpretation depends on the column type. See [Grist data format](https://github.com/gristlabs/grist-core/blob/main/documentation/grist-data-format.md) for details. | [optional] 

### Return type

[**Data**](Data.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cells from the table |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_rows**
> List[int] modify_rows(doc_id, table_id, data, noparse=noparse)

Modify rows of a table

Deprecated in favor of `records` endpoints. We have no immediate plans to remove these endpoints, but consider `records` a better starting point for new projects.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.data import Data
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
    api_instance = grist_client.DataApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    data = grist_client.Data() # Data | the data to change, with ids
    noparse = True # bool | Set to true to prohibit parsing strings according to the column type. (optional)

    try:
        # Modify rows of a table
        api_response = api_instance.modify_rows(doc_id, table_id, data, noparse=noparse)
        print("The response of DataApi->modify_rows:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DataApi->modify_rows: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**| normalized table name (see &#x60;TABLE ID&#x60; in Raw Data) or numeric row ID in &#x60;_grist_Tables&#x60; | 
 **data** | [**Data**](Data.md)| the data to change, with ids | 
 **noparse** | **bool**| Set to true to prohibit parsing strings according to the column type. | [optional] 

### Return type

**List[int]**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | IDs of rows modified |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

