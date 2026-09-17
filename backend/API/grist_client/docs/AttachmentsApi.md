# grist_client.AttachmentsApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**download_attachment**](AttachmentsApi.md#download_attachment) | **GET** /docs/{docId}/attachments/{attachmentId}/download | Download the contents of an attachment
[**download_attachments**](AttachmentsApi.md#download_attachments) | **GET** /docs/{docId}/attachments/archive | Download all attachments
[**get_attachment_metadata**](AttachmentsApi.md#get_attachment_metadata) | **GET** /docs/{docId}/attachments/{attachmentId} | Get the metadata for an attachment
[**get_attachment_transfer_status**](AttachmentsApi.md#get_attachment_transfer_status) | **GET** /docs/{docId}/attachments/transferStatus | Get attachment transfer status
[**get_document_attachment_store**](AttachmentsApi.md#get_document_attachment_store) | **GET** /docs/{docId}/attachments/store | Get external store
[**list_attachment_stores**](AttachmentsApi.md#list_attachment_stores) | **GET** /docs/{docId}/attachments/stores | List external attachment stores
[**list_attachments**](AttachmentsApi.md#list_attachments) | **GET** /docs/{docId}/attachments | List metadata of all attachments in a doc
[**remove_unused_attachments**](AttachmentsApi.md#remove_unused_attachments) | **POST** /docs/{docId}/attachments/removeUnused | Delete unused attachments from the document
[**set_document_attachment_store**](AttachmentsApi.md#set_document_attachment_store) | **POST** /docs/{docId}/attachments/store | Set external store
[**start_attachment_transfer**](AttachmentsApi.md#start_attachment_transfer) | **POST** /docs/{docId}/attachments/transferAll | Start transferring attachments
[**update_used_attachments**](AttachmentsApi.md#update_used_attachments) | **POST** /docs/{docId}/attachments/updateUsed | Update attachment usage tracking
[**upload_attachments**](AttachmentsApi.md#upload_attachments) | **POST** /docs/{docId}/attachments | Upload attachments to a doc
[**upload_missing_attachments**](AttachmentsApi.md#upload_missing_attachments) | **POST** /docs/{docId}/attachments/archive | Upload missing attachments
[**verify_attachment_files**](AttachmentsApi.md#verify_attachment_files) | **POST** /docs/{docId}/attachments/verifyFiles | Verify attachment file integrity


# **download_attachment**
> download_attachment(doc_id, attachment_id)

Download the contents of an attachment

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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    attachment_id = 3.4 # float | 

    try:
        # Download the contents of an attachment
        api_instance.download_attachment(doc_id, attachment_id)
    except Exception as e:
        print("Exception when calling AttachmentsApi->download_attachment: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **attachment_id** | **float**|  | 

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
**200** | Attachment contents, with suitable Content-Type. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_attachments**
> download_attachments(doc_id, format=format)

Download all attachments

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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    format = 'format_example' # str |  (optional)

    try:
        # Download all attachments
        api_instance.download_attachments(doc_id, format=format)
    except Exception as e:
        print("Exception when calling AttachmentsApi->download_attachments: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **format** | **str**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Archive of all attachments, in either .zip or .tar format. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_attachment_metadata**
> AttachmentMetadata get_attachment_metadata(doc_id, attachment_id)

Get the metadata for an attachment

### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.attachment_metadata import AttachmentMetadata
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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    attachment_id = 3.4 # float | 

    try:
        # Get the metadata for an attachment
        api_response = api_instance.get_attachment_metadata(doc_id, attachment_id)
        print("The response of AttachmentsApi->get_attachment_metadata:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AttachmentsApi->get_attachment_metadata: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **attachment_id** | **float**|  | 

### Return type

[**AttachmentMetadata**](AttachmentMetadata.md)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Attachment metadata |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_attachment_transfer_status**
> AttachmentsTransferStatus get_attachment_transfer_status(doc_id)

Get attachment transfer status

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.attachments_transfer_status import AttachmentsTransferStatus
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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Get attachment transfer status
        api_response = api_instance.get_attachment_transfer_status(doc_id)
        print("The response of AttachmentsApi->get_attachment_transfer_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AttachmentsApi->get_attachment_transfer_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

[**AttachmentsTransferStatus**](AttachmentsTransferStatus.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Transfer status |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_document_attachment_store**
> DocumentStoreSetting get_document_attachment_store(doc_id)

Get external store

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.document_store_setting import DocumentStoreSetting
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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Get external store
        api_response = api_instance.get_document_attachment_store(doc_id)
        print("The response of AttachmentsApi->get_document_attachment_store:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AttachmentsApi->get_document_attachment_store: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

[**DocumentStoreSetting**](DocumentStoreSetting.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Document&#39;s current external storage setting |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_attachment_stores**
> DocumentStoreSetting list_attachment_stores(doc_id)

List external attachment stores

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.document_store_setting import DocumentStoreSetting
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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # List external attachment stores
        api_response = api_instance.list_attachment_stores(doc_id)
        print("The response of AttachmentsApi->list_attachment_stores:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AttachmentsApi->list_attachment_stores: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

[**DocumentStoreSetting**](DocumentStoreSetting.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Document&#39;s current external storage setting |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_attachments**
> AttachmentMetadataList list_attachments(doc_id, filter=filter, sort=sort, limit=limit, x_sort=x_sort, x_limit=x_limit)

List metadata of all attachments in a doc

### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.attachment_metadata_list import AttachmentMetadataList
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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    filter = '{\"pet\": [\"cat\", \"dog\"]}' # str | This is a JSON object mapping column names to arrays of allowed values.  For example, to filter column `pet` for values `cat` and `dog`, the filter would be `{\"pet\": [\"cat\", \"dog\"]}`. JSON contains characters that are not safe to place in a URL, so it is important to url-encode them.  For this example, the url-encoding is `%7B%22pet%22%3A%20%5B%22cat%22%2C%20%22dog%22%5D%7D`. See https://rosettacode.org/wiki/URL_encoding for how to url-encode a string, or https://www.urlencoder.org/ to try some examples. Multiple columns can be filtered. For example the filter for `pet` being either `cat` or `dog`, AND `size` being either `tiny` or `outrageously small`, would be `{\"pet\": [\"cat\", \"dog\"], \"size\": [\"tiny\", \"outrageously small\"]}`. (optional)
    sort = 'pet,-age' # str | Order in which to return results. If a single column name is given (e.g. `pet`), results are placed in ascending order of values in that column. To get results in an order that was previously prepared manually in Grist, use the special `manualSort` column name. Multiple columns can be specified, separated by commas (e.g. `pet,age`). For descending order, prefix a column name with a `-` character (e.g. `pet,-age`). To include additional sorting options append them after a colon (e.g. `pet,-age:naturalSort;emptyLast,owner`). Available options are: `orderByChoice`, `naturalSort`, `emptyLast`. Without the `sort` parameter, the order of results is unspecified. (optional)
    limit = 5 # float | Return at most this number of rows.  A value of 0 is equivalent to having no limit. (optional)
    x_sort = 'pet,-age' # str | Same as `sort` query parameter. (optional)
    x_limit = 5 # float | Same as `limit` query parameter. (optional)

    try:
        # List metadata of all attachments in a doc
        api_response = api_instance.list_attachments(doc_id, filter=filter, sort=sort, limit=limit, x_sort=x_sort, x_limit=x_limit)
        print("The response of AttachmentsApi->list_attachments:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AttachmentsApi->list_attachments: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **filter** | **str**| This is a JSON object mapping column names to arrays of allowed values.  For example, to filter column &#x60;pet&#x60; for values &#x60;cat&#x60; and &#x60;dog&#x60;, the filter would be &#x60;{\&quot;pet\&quot;: [\&quot;cat\&quot;, \&quot;dog\&quot;]}&#x60;. JSON contains characters that are not safe to place in a URL, so it is important to url-encode them.  For this example, the url-encoding is &#x60;%7B%22pet%22%3A%20%5B%22cat%22%2C%20%22dog%22%5D%7D&#x60;. See https://rosettacode.org/wiki/URL_encoding for how to url-encode a string, or https://www.urlencoder.org/ to try some examples. Multiple columns can be filtered. For example the filter for &#x60;pet&#x60; being either &#x60;cat&#x60; or &#x60;dog&#x60;, AND &#x60;size&#x60; being either &#x60;tiny&#x60; or &#x60;outrageously small&#x60;, would be &#x60;{\&quot;pet\&quot;: [\&quot;cat\&quot;, \&quot;dog\&quot;], \&quot;size\&quot;: [\&quot;tiny\&quot;, \&quot;outrageously small\&quot;]}&#x60;. | [optional] 
 **sort** | **str**| Order in which to return results. If a single column name is given (e.g. &#x60;pet&#x60;), results are placed in ascending order of values in that column. To get results in an order that was previously prepared manually in Grist, use the special &#x60;manualSort&#x60; column name. Multiple columns can be specified, separated by commas (e.g. &#x60;pet,age&#x60;). For descending order, prefix a column name with a &#x60;-&#x60; character (e.g. &#x60;pet,-age&#x60;). To include additional sorting options append them after a colon (e.g. &#x60;pet,-age:naturalSort;emptyLast,owner&#x60;). Available options are: &#x60;orderByChoice&#x60;, &#x60;naturalSort&#x60;, &#x60;emptyLast&#x60;. Without the &#x60;sort&#x60; parameter, the order of results is unspecified. | [optional] 
 **limit** | **float**| Return at most this number of rows.  A value of 0 is equivalent to having no limit. | [optional] 
 **x_sort** | **str**| Same as &#x60;sort&#x60; query parameter. | [optional] 
 **x_limit** | **float**| Same as &#x60;limit&#x60; query parameter. | [optional] 

### Return type

[**AttachmentMetadataList**](AttachmentMetadataList.md)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of attachment metadata records. Note that the list may temporarily include records for attachments that are stored in the document but not referenced by any Attachments type cell. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_unused_attachments**
> remove_unused_attachments(doc_id, expired_only=expired_only)

Delete unused attachments from the document

When an uploaded attachment is no longer used in a Grist document,  it's retained for a period of time in case it's needed again (e.g. to facilitate an "undo").
This removes all of these retained attachments, reducing the amount of storage used. This is particularly useful if a document has hit its attachment storage limit.


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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    expired_only = True # bool |  (optional)

    try:
        # Delete unused attachments from the document
        api_instance.remove_unused_attachments(doc_id, expired_only=expired_only)
    except Exception as e:
        print("Exception when calling AttachmentsApi->remove_unused_attachments: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **expired_only** | **bool**|  | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_document_attachment_store**
> SetDocumentAttachmentStore200Response set_document_attachment_store(doc_id, document_store_setting=document_store_setting)

Set external store

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.document_store_setting import DocumentStoreSetting
from grist_client.models.set_document_attachment_store200_response import SetDocumentAttachmentStore200Response
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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    document_store_setting = grist_client.DocumentStoreSetting() # DocumentStoreSetting |  (optional)

    try:
        # Set external store
        api_response = api_instance.set_document_attachment_store(doc_id, document_store_setting=document_store_setting)
        print("The response of AttachmentsApi->set_document_attachment_store:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AttachmentsApi->set_document_attachment_store: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **document_store_setting** | [**DocumentStoreSetting**](DocumentStoreSetting.md)|  | [optional] 

### Return type

[**SetDocumentAttachmentStore200Response**](SetDocumentAttachmentStore200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The ID of the store the document&#39;s store |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_attachment_transfer**
> AttachmentsTransferStatus start_attachment_transfer(doc_id)

Start transferring attachments

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.attachments_transfer_status import AttachmentsTransferStatus
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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Start transferring attachments
        api_response = api_instance.start_attachment_transfer(doc_id)
        print("The response of AttachmentsApi->start_attachment_transfer:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AttachmentsApi->start_attachment_transfer: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

[**AttachmentsTransferStatus**](AttachmentsTransferStatus.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Transfer status |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_used_attachments**
> update_used_attachments(doc_id)

Update attachment usage tracking

Recalculate which attachments are in use by scanning the document.
This is mostly used for testing and maintenance.


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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Update attachment usage tracking
        api_instance.update_used_attachments(doc_id)
    except Exception as e:
        print("Exception when calling AttachmentsApi->update_used_attachments: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_attachments**
> List[int] upload_attachments(doc_id, upload=upload)

Upload attachments to a doc

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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    upload = None # List[bytearray] |  (optional)

    try:
        # Upload attachments to a doc
        api_response = api_instance.upload_attachments(doc_id, upload=upload)
        print("The response of AttachmentsApi->upload_attachments:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AttachmentsApi->upload_attachments: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **upload** | **List[bytearray]**|  | [optional] 

### Return type

**List[int]**

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | IDs of attachments added, one per file. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_missing_attachments**
> UploadMissingAttachments200Response upload_missing_attachments(doc_id, file=file)

Upload missing attachments

Restores attachments which are missing from external storage.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.upload_missing_attachments200_response import UploadMissingAttachments200Response
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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    file = None # bytearray | The .tar file. Must have `Content-Type=application/x-tar` set. (optional)

    try:
        # Upload missing attachments
        api_response = api_instance.upload_missing_attachments(doc_id, file=file)
        print("The response of AttachmentsApi->upload_missing_attachments:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AttachmentsApi->upload_missing_attachments: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **file** | **bytearray**| The .tar file. Must have &#x60;Content-Type&#x3D;application/x-tar&#x60; set. | [optional] 

### Return type

[**UploadMissingAttachments200Response**](UploadMissingAttachments200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Summary of attachments used |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **verify_attachment_files**
> verify_attachment_files(doc_id)

Verify attachment file integrity

Verify that attachment records match the actual stored files.
This is a maintenance endpoint to check for data consistency.
Only document owners can call this endpoint.


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
    api_instance = grist_client.AttachmentsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Verify attachment file integrity
        api_instance.verify_attachment_files(doc_id)
    except Exception as e:
        print("Exception when calling AttachmentsApi->verify_attachment_files: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Verification passed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

