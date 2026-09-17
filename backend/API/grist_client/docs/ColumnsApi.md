# grist_client.ColumnsApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_columns**](ColumnsApi.md#add_columns) | **POST** /docs/{docId}/tables/{tableId}/columns | Add columns to a table
[**delete_column**](ColumnsApi.md#delete_column) | **DELETE** /docs/{docId}/tables/{tableId}/columns/{colId} | Delete a column of a table
[**list_columns**](ColumnsApi.md#list_columns) | **GET** /docs/{docId}/tables/{tableId}/columns | List columns in a table
[**modify_columns**](ColumnsApi.md#modify_columns) | **PATCH** /docs/{docId}/tables/{tableId}/columns | Modify columns of a table
[**replace_columns**](ColumnsApi.md#replace_columns) | **PUT** /docs/{docId}/tables/{tableId}/columns | Add or update columns of a table


# **add_columns**
> ColumnsWithoutFields add_columns(doc_id, table_id, create_columns)

Add columns to a table

### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.columns_without_fields import ColumnsWithoutFields
from grist_client.models.create_columns import CreateColumns
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
    api_instance = grist_client.ColumnsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    create_columns = grist_client.CreateColumns() # CreateColumns | the columns to add

    try:
        # Add columns to a table
        api_response = api_instance.add_columns(doc_id, table_id, create_columns)
        print("The response of ColumnsApi->add_columns:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ColumnsApi->add_columns: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**| normalized table name (see &#x60;TABLE ID&#x60; in Raw Data) or numeric row ID in &#x60;_grist_Tables&#x60; | 
 **create_columns** | [**CreateColumns**](CreateColumns.md)| the columns to add | 

### Return type

[**ColumnsWithoutFields**](ColumnsWithoutFields.md)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The columns created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_column**
> delete_column(doc_id, table_id, col_id)

Delete a column of a table

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
    api_instance = grist_client.ColumnsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    col_id = 'col_id_example' # str | The column id (without the starting `$`) as shown in the column configuration below the label

    try:
        # Delete a column of a table
        api_instance.delete_column(doc_id, table_id, col_id)
    except Exception as e:
        print("Exception when calling ColumnsApi->delete_column: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**| normalized table name (see &#x60;TABLE ID&#x60; in Raw Data) or numeric row ID in &#x60;_grist_Tables&#x60; | 
 **col_id** | **str**| The column id (without the starting &#x60;$&#x60;) as shown in the column configuration below the label | 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_columns**
> ColumnsList list_columns(doc_id, table_id, hidden=hidden)

List columns in a table

### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.columns_list import ColumnsList
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
    api_instance = grist_client.ColumnsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    hidden = True # bool | Set to true to include the hidden columns (like \"manualSort\") (optional)

    try:
        # List columns in a table
        api_response = api_instance.list_columns(doc_id, table_id, hidden=hidden)
        print("The response of ColumnsApi->list_columns:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ColumnsApi->list_columns: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**| normalized table name (see &#x60;TABLE ID&#x60; in Raw Data) or numeric row ID in &#x60;_grist_Tables&#x60; | 
 **hidden** | **bool**| Set to true to include the hidden columns (like \&quot;manualSort\&quot;) | [optional] 

### Return type

[**ColumnsList**](ColumnsList.md)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The columns in a table |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_columns**
> modify_columns(doc_id, table_id, update_columns)

Modify columns of a table

### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.update_columns import UpdateColumns
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
    api_instance = grist_client.ColumnsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    update_columns = grist_client.UpdateColumns() # UpdateColumns | the columns to change, with ids

    try:
        # Modify columns of a table
        api_instance.modify_columns(doc_id, table_id, update_columns)
    except Exception as e:
        print("Exception when calling ColumnsApi->modify_columns: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**| normalized table name (see &#x60;TABLE ID&#x60; in Raw Data) or numeric row ID in &#x60;_grist_Tables&#x60; | 
 **update_columns** | [**UpdateColumns**](UpdateColumns.md)| the columns to change, with ids | 

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

# **replace_columns**
> replace_columns(doc_id, table_id, update_columns, noadd=noadd, noupdate=noupdate, replaceall=replaceall)

Add or update columns of a table

### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.update_columns import UpdateColumns
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
    api_instance = grist_client.ColumnsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | normalized table name (see `TABLE ID` in Raw Data) or numeric row ID in `_grist_Tables`
    update_columns = grist_client.UpdateColumns() # UpdateColumns | The columns to add or update. We check whether the specified column ID exists: if so, the column is updated with the provided data, otherwise a new column is created. Also note that some query parameters alter this behavior. 
    noadd = True # bool |  (optional)
    noupdate = True # bool |  (optional)
    replaceall = True # bool |  (optional)

    try:
        # Add or update columns of a table
        api_instance.replace_columns(doc_id, table_id, update_columns, noadd=noadd, noupdate=noupdate, replaceall=replaceall)
    except Exception as e:
        print("Exception when calling ColumnsApi->replace_columns: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**| normalized table name (see &#x60;TABLE ID&#x60; in Raw Data) or numeric row ID in &#x60;_grist_Tables&#x60; | 
 **update_columns** | [**UpdateColumns**](UpdateColumns.md)| The columns to add or update. We check whether the specified column ID exists: if so, the column is updated with the provided data, otherwise a new column is created. Also note that some query parameters alter this behavior.  | 
 **noadd** | **bool**|  | [optional] 
 **noupdate** | **bool**|  | [optional] 
 **replaceall** | **bool**|  | [optional] 

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

