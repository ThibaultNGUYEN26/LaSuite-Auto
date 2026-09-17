# grist_client.RecordsApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_records**](RecordsApi.md#add_records) | **POST** /docs/{docId}/tables/{tableId}/records | Add records to a table
[**delete_records**](RecordsApi.md#delete_records) | **POST** /docs/{docId}/tables/{tableId}/records/delete | Delete records of a table
[**list_records**](RecordsApi.md#list_records) | **GET** /docs/{docId}/tables/{tableId}/records | Fetch records from a table
[**modify_records**](RecordsApi.md#modify_records) | **PATCH** /docs/{docId}/tables/{tableId}/records | Modify records of a table
[**replace_records**](RecordsApi.md#replace_records) | **PUT** /docs/{docId}/tables/{tableId}/records | Add or update records of a table


# **add_records**
> RecordsWithoutFields add_records(doc_id, table_id, records_without_id, noparse=noparse)

Add records to a table

### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.records_without_fields import RecordsWithoutFields
from grist_client.models.records_without_id import RecordsWithoutId
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
    api_instance = grist_client.RecordsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    records_without_id = grist_client.RecordsWithoutId() # RecordsWithoutId | the records to add
    noparse = True # bool | Set to true to prohibit parsing strings according to the column type. (optional)

    try:
        # Add records to a table
        api_response = api_instance.add_records(doc_id, table_id, records_without_id, noparse=noparse)
        print("The response of RecordsApi->add_records:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RecordsApi->add_records: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**| normalized table name (see &#x60;TABLE ID&#x60; in Raw Data) or numeric row ID in &#x60;_grist_Tables&#x60; | 
 **records_without_id** | [**RecordsWithoutId**](RecordsWithoutId.md)| the records to add | 
 **noparse** | **bool**| Set to true to prohibit parsing strings according to the column type. | [optional] 

### Return type

[**RecordsWithoutFields**](RecordsWithoutFields.md)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | IDs of records added |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_records**
> delete_records(doc_id, table_id, request_body)

Delete records of a table

### Example

* OAuth Authentication (OAuth2):
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

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Configure Bearer authorization (Authorization: Bearer XXXXXXXXXXX): ApiKey
configuration = grist_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)

# Enter a context with an instance of the API client
with grist_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = grist_client.RecordsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    request_body = [56] # List[int] | the IDs of records to remove

    try:
        # Delete records of a table
        api_instance.delete_records(doc_id, table_id, request_body)
    except Exception as e:
        print("Exception when calling RecordsApi->delete_records: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**| normalized table name (see &#x60;TABLE ID&#x60; in Raw Data) or numeric row ID in &#x60;_grist_Tables&#x60; | 
 **request_body** | [**List[int]**](int.md)| the IDs of records to remove | 

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
**200** | Nothing returned |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_records**
> RecordsList list_records(doc_id, table_id, filter=filter, sort=sort, limit=limit, x_sort=x_sort, x_limit=x_limit, hidden=hidden, cell_format=cell_format)

Fetch records from a table

### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.records_list import RecordsList
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
    api_instance = grist_client.RecordsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    filter = '{\"pet\": [\"cat\", \"dog\"]}' # str | This is a JSON object mapping column names to arrays of allowed values.  For example, to filter column `pet` for values `cat` and `dog`, the filter would be `{\"pet\": [\"cat\", \"dog\"]}`. JSON contains characters that are not safe to place in a URL, so it is important to url-encode them.  For this example, the url-encoding is `%7B%22pet%22%3A%20%5B%22cat%22%2C%20%22dog%22%5D%7D`. See https://rosettacode.org/wiki/URL_encoding for how to url-encode a string, or https://www.urlencoder.org/ to try some examples. Multiple columns can be filtered. For example the filter for `pet` being either `cat` or `dog`, AND `size` being either `tiny` or `outrageously small`, would be `{\"pet\": [\"cat\", \"dog\"], \"size\": [\"tiny\", \"outrageously small\"]}`. (optional)
    sort = 'pet,-age' # str | Order in which to return results. If a single column name is given (e.g. `pet`), results are placed in ascending order of values in that column. To get results in an order that was previously prepared manually in Grist, use the special `manualSort` column name. Multiple columns can be specified, separated by commas (e.g. `pet,age`). For descending order, prefix a column name with a `-` character (e.g. `pet,-age`). To include additional sorting options append them after a colon (e.g. `pet,-age:naturalSort;emptyLast,owner`). Available options are: `orderByChoice`, `naturalSort`, `emptyLast`. Without the `sort` parameter, the order of results is unspecified. (optional)
    limit = 5 # float | Return at most this number of rows.  A value of 0 is equivalent to having no limit. (optional)
    x_sort = 'pet,-age' # str | Same as `sort` query parameter. (optional)
    x_limit = 5 # float | Same as `limit` query parameter. (optional)
    hidden = True # bool | Set to true to include the hidden columns (like \"manualSort\") (optional)
    cell_format = 'cell_format_example' # str | With \"typed\", every cell value is returned in a self-describing typed form, e.g. a Date as `[\"d\", timestamp]` and a Reference as `[\"R\", tableId, rowId]`, and formula errors are returned inline as `[\"E\", ...]` values. The default \"normal\" format uses compact values whose interpretation depends on the column type. See [Grist data format](https://github.com/gristlabs/grist-core/blob/main/documentation/grist-data-format.md) for details. (optional)

    try:
        # Fetch records from a table
        api_response = api_instance.list_records(doc_id, table_id, filter=filter, sort=sort, limit=limit, x_sort=x_sort, x_limit=x_limit, hidden=hidden, cell_format=cell_format)
        print("The response of RecordsApi->list_records:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling RecordsApi->list_records: %s\n" % e)
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
 **hidden** | **bool**| Set to true to include the hidden columns (like \&quot;manualSort\&quot;) | [optional] 
 **cell_format** | **str**| With \&quot;typed\&quot;, every cell value is returned in a self-describing typed form, e.g. a Date as &#x60;[\&quot;d\&quot;, timestamp]&#x60; and a Reference as &#x60;[\&quot;R\&quot;, tableId, rowId]&#x60;, and formula errors are returned inline as &#x60;[\&quot;E\&quot;, ...]&#x60; values. The default \&quot;normal\&quot; format uses compact values whose interpretation depends on the column type. See [Grist data format](https://github.com/gristlabs/grist-core/blob/main/documentation/grist-data-format.md) for details. | [optional] 

### Return type

[**RecordsList**](RecordsList.md)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Records from the table |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_records**
> modify_records(doc_id, table_id, records_list, noparse=noparse)

Modify records of a table

### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.records_list import RecordsList
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
    api_instance = grist_client.RecordsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    records_list = grist_client.RecordsList() # RecordsList | the records to change, with ids
    noparse = True # bool | Set to true to prohibit parsing strings according to the column type. (optional)

    try:
        # Modify records of a table
        api_instance.modify_records(doc_id, table_id, records_list, noparse=noparse)
    except Exception as e:
        print("Exception when calling RecordsApi->modify_records: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**| normalized table name (see &#x60;TABLE ID&#x60; in Raw Data) or numeric row ID in &#x60;_grist_Tables&#x60; | 
 **records_list** | [**RecordsList**](RecordsList.md)| the records to change, with ids | 
 **noparse** | **bool**| Set to true to prohibit parsing strings according to the column type. | [optional] 

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

# **replace_records**
> replace_records(doc_id, table_id, records_with_require, noparse=noparse, onmany=onmany, noadd=noadd, noupdate=noupdate, allow_empty_require=allow_empty_require)

Add or update records of a table

### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.records_with_require import RecordsWithRequire
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
    api_instance = grist_client.RecordsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    records_with_require = grist_client.RecordsWithRequire() # RecordsWithRequire | The records to add or update. Instead of an id, a `require` object is provided, with the same structure as `fields`. If no query parameter options are set, then the operation is as follows. First, we check if a record exists matching the values specified for columns in `require`. If so, we update it by setting the values specified for columns in `fields`. If not, we create a new record with a combination of the values in `require` and `fields`, with `fields` taking priority if the same column is specified in both. The query parameters allow for variations on this behavior. 
    noparse = True # bool | Set to true to prohibit parsing strings according to the column type. (optional)
    onmany = 'onmany_example' # str |  (optional)
    noadd = True # bool |  (optional)
    noupdate = True # bool |  (optional)
    allow_empty_require = True # bool |  (optional)

    try:
        # Add or update records of a table
        api_instance.replace_records(doc_id, table_id, records_with_require, noparse=noparse, onmany=onmany, noadd=noadd, noupdate=noupdate, allow_empty_require=allow_empty_require)
    except Exception as e:
        print("Exception when calling RecordsApi->replace_records: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**| normalized table name (see &#x60;TABLE ID&#x60; in Raw Data) or numeric row ID in &#x60;_grist_Tables&#x60; | 
 **records_with_require** | [**RecordsWithRequire**](RecordsWithRequire.md)| The records to add or update. Instead of an id, a &#x60;require&#x60; object is provided, with the same structure as &#x60;fields&#x60;. If no query parameter options are set, then the operation is as follows. First, we check if a record exists matching the values specified for columns in &#x60;require&#x60;. If so, we update it by setting the values specified for columns in &#x60;fields&#x60;. If not, we create a new record with a combination of the values in &#x60;require&#x60; and &#x60;fields&#x60;, with &#x60;fields&#x60; taking priority if the same column is specified in both. The query parameters allow for variations on this behavior.  | 
 **noparse** | **bool**| Set to true to prohibit parsing strings according to the column type. | [optional] 
 **onmany** | **str**|  | [optional] 
 **noadd** | **bool**|  | [optional] 
 **noupdate** | **bool**|  | [optional] 
 **allow_empty_require** | **bool**|  | [optional] 

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

