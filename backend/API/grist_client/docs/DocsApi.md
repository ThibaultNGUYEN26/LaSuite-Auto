# grist_client.DocsApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**apply_proposal**](DocsApi.md#apply_proposal) | **POST** /docs/{docId}/proposals/{proposalId}/apply | Apply a change proposal
[**apply_user_actions**](DocsApi.md#apply_user_actions) | **POST** /docs/{docId}/apply | Apply a list of user actions
[**assign_doc**](DocsApi.md#assign_doc) | **POST** /docs/{docId}/assign | Reassign document to appropriate worker
[**compare_documents**](DocsApi.md#compare_documents) | **GET** /docs/{docId}/compare/{docId2} | Compare two documents
[**compare_versions**](DocsApi.md#compare_versions) | **GET** /docs/{docId}/compare | Compare document versions
[**copy_doc**](DocsApi.md#copy_doc) | **POST** /docs/{docId}/copy | Copies a document to a workspace.
[**create_doc**](DocsApi.md#create_doc) | **POST** /workspaces/{workspaceId}/docs | Create an empty document
[**create_doc_unified**](DocsApi.md#create_doc_unified) | **POST** /docs | Create a document
[**create_proposal**](DocsApi.md#create_proposal) | **POST** /docs/{docId}/propose | Create a change proposal
[**delete_actions**](DocsApi.md#delete_actions) | **POST** /docs/{docId}/states/remove | Truncate the document&#39;s action history
[**delete_doc**](DocsApi.md#delete_doc) | **DELETE** /docs/{docId} | Delete a document
[**describe_doc**](DocsApi.md#describe_doc) | **GET** /docs/{docId} | Describe a document
[**disable_doc**](DocsApi.md#disable_doc) | **POST** /docs/{docId}/disable | Disable a document.
[**download_doc**](DocsApi.md#download_doc) | **GET** /docs/{docId}/download | Content of document, as an Sqlite file
[**download_doc_csv**](DocsApi.md#download_doc_csv) | **GET** /docs/{docId}/download/csv | Content of table, as a CSV file
[**download_doc_dsv**](DocsApi.md#download_doc_dsv) | **GET** /docs/{docId}/download/dsv | Content of table, as a DSV file
[**download_doc_tsv**](DocsApi.md#download_doc_tsv) | **GET** /docs/{docId}/download/tsv | Content of table, as a TSV file
[**download_doc_xlsx**](DocsApi.md#download_doc_xlsx) | **GET** /docs/{docId}/download/xlsx | Content of document, as an Excel file
[**download_table_schema**](DocsApi.md#download_table_schema) | **GET** /docs/{docId}/download/table-schema | The schema of a table
[**enable_doc**](DocsApi.md#enable_doc) | **POST** /docs/{docId}/enable | Enable a document.
[**flush_doc**](DocsApi.md#flush_doc) | **POST** /docs/{docId}/flush | Flush document to storage
[**force_reload**](DocsApi.md#force_reload) | **POST** /docs/{docId}/force-reload | Reload a document
[**fork_doc**](DocsApi.md#fork_doc) | **POST** /docs/{docId}/fork | Fork a document
[**get_states**](DocsApi.md#get_states) | **GET** /docs/{docId}/states | Get document action history states
[**get_timing_status**](DocsApi.md#get_timing_status) | **GET** /docs/{docId}/timing | Get formula timing status
[**get_users_for_view_as**](DocsApi.md#get_users_for_view_as) | **GET** /docs/{docId}/usersForViewAs | Get users for &#39;View As&#39; feature
[**import_doc**](DocsApi.md#import_doc) | **POST** /workspaces/{workspaceId}/import | Import an existing document
[**list_doc_access**](DocsApi.md#list_doc_access) | **GET** /docs/{docId}/access | List users with access to document
[**list_proposals**](DocsApi.md#list_proposals) | **GET** /docs/{docId}/proposals | List change proposals
[**list_snapshots**](DocsApi.md#list_snapshots) | **GET** /docs/{docId}/snapshots | List document snapshots
[**modify_doc**](DocsApi.md#modify_doc) | **PATCH** /docs/{docId} | Modify document metadata (but not its contents)
[**modify_doc_access**](DocsApi.md#modify_doc_access) | **PATCH** /docs/{docId}/access | Change who has access to document
[**move_doc**](DocsApi.md#move_doc) | **PATCH** /docs/{docId}/move | Move document to another workspace.
[**pin_doc**](DocsApi.md#pin_doc) | **PATCH** /docs/{docId}/pin | Pin a document
[**recover_doc**](DocsApi.md#recover_doc) | **POST** /docs/{docId}/recover | Set recovery mode for a document
[**remove_doc**](DocsApi.md#remove_doc) | **POST** /docs/{docId}/remove | Move document to trash
[**remove_snapshots**](DocsApi.md#remove_snapshots) | **POST** /docs/{docId}/snapshots/remove | Remove document snapshots
[**replace_doc**](DocsApi.md#replace_doc) | **POST** /docs/{docId}/replace | Replace document content
[**start_timing**](DocsApi.md#start_timing) | **POST** /docs/{docId}/timing/start | Start formula timing
[**stop_timing**](DocsApi.md#stop_timing) | **POST** /docs/{docId}/timing/stop | Stop formula timing
[**unpin_doc**](DocsApi.md#unpin_doc) | **PATCH** /docs/{docId}/unpin | Unpin a document
[**unremove_doc**](DocsApi.md#unremove_doc) | **POST** /docs/{docId}/unremove | Restore document from trash


# **apply_proposal**
> ApplyProposal200Response apply_proposal(doc_id, proposal_id)

Apply a change proposal

Apply a proposal's changes to the document. This merges the fork's
changes into the trunk document.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.apply_proposal200_response import ApplyProposal200Response
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    proposal_id = 56 # int | ID of the proposal to apply

    try:
        # Apply a change proposal
        api_response = api_instance.apply_proposal(doc_id, proposal_id)
        print("The response of DocsApi->apply_proposal:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->apply_proposal: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **proposal_id** | **int**| ID of the proposal to apply | 

### Return type

[**ApplyProposal200Response**](ApplyProposal200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Proposal applied successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **apply_user_actions**
> ApplyUserActions200Response apply_user_actions(doc_id, request_body, noparse=noparse)

Apply a list of user actions

Apply a sequence of user actions to a document. This is a low-level endpoint
for making batch changes using Grist's internal action format.

Each action is an array where the first element is the action type.
Common action types:
- `["AddRecord", tableId, rowId, {column: value}]` - Add a row (use null for auto-assigned rowId)
- `["UpdateRecord", tableId, rowId, {column: value}]` - Update a row
- `["RemoveRecord", tableId, rowId]` - Delete a row
- `["BulkAddRecord", tableId, [rowIds], {column: [values]}]` - Add multiple rows
- `["BulkUpdateRecord", tableId, [rowIds], {column: [values]}]` - Update multiple rows
- `["BulkRemoveRecord", tableId, [rowIds]]` - Delete multiple rows
- `["AddColumn", tableId, colId, {type, ...}]` - Add a column
- `["RemoveColumn", tableId, colId]` - Remove a column
- `["RenameColumn", tableId, oldColId, newColId]` - Rename a column
- `["AddTable", tableId, [{id, type, ...}]]` - Add a table
- `["RemoveTable", tableId]` - Remove a table


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.apply_user_actions200_response import ApplyUserActions200Response
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    request_body = None # List[List[object]] | An array of user actions to apply
    noparse = True # bool | If true, string values are stored as-is without parsing (e.g. dates won't be auto-converted) (optional)

    try:
        # Apply a list of user actions
        api_response = api_instance.apply_user_actions(doc_id, request_body, noparse=noparse)
        print("The response of DocsApi->apply_user_actions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->apply_user_actions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **request_body** | [**List[List[object]]**](List.md)| An array of user actions to apply | 
 **noparse** | **bool**| If true, string values are stored as-is without parsing (e.g. dates won&#39;t be auto-converted) | [optional] 

### Return type

[**ApplyUserActions200Response**](ApplyUserActions200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Actions applied successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **assign_doc**
> bool assign_doc(doc_id, group=group)

Reassign document to appropriate worker

Administrative endpoint that checks if a document is assigned to the expected
worker group and frees it for reassignment if not. Used for load balancing
and maintenance operations.


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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    group = 'group_example' # str | Update the document's worker group (requires special permit) (optional)

    try:
        # Reassign document to appropriate worker
        api_response = api_instance.assign_doc(doc_id, group=group)
        print("The response of DocsApi->assign_doc:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->assign_doc: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **group** | **str**| Update the document&#39;s worker group (requires special permit) | [optional] 

### Return type

**bool**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Assignment result |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **compare_documents**
> DocComparison compare_documents(doc_id, doc_id2, detail=detail, max_rows=max_rows)

Compare two documents

Compare this document with another document. Useful for comparing
a fork with its trunk document.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.doc_comparison import DocComparison
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    doc_id2 = 'doc_id2_example' # str | ID of the document to compare with
    detail = True # bool | If true, include detailed change information (optional)
    max_rows = 56 # int | Maximum number of row changes to include (optional)

    try:
        # Compare two documents
        api_response = api_instance.compare_documents(doc_id, doc_id2, detail=detail, max_rows=max_rows)
        print("The response of DocsApi->compare_documents:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->compare_documents: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **doc_id2** | **str**| ID of the document to compare with | 
 **detail** | **bool**| If true, include detailed change information | [optional] 
 **max_rows** | **int**| Maximum number of row changes to include | [optional] 

### Return type

[**DocComparison**](DocComparison.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Comparison result |  -  |
**403** | Insufficient access to compare documents |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **compare_versions**
> DocComparison compare_versions(doc_id, left=left, right=right, max_rows=max_rows)

Compare document versions

Compare two versions of the same document by their state hashes.
Returns details about what changed between the versions.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.doc_comparison import DocComparison
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    left = 'left_example' # str | Hash of the left version to compare (defaults to HEAD) (optional)
    right = 'right_example' # str | Hash of the right version to compare (defaults to HEAD) (optional)
    max_rows = 56 # int | Maximum number of row changes to include in details (optional)

    try:
        # Compare document versions
        api_response = api_instance.compare_versions(doc_id, left=left, right=right, max_rows=max_rows)
        print("The response of DocsApi->compare_versions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->compare_versions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **left** | **str**| Hash of the left version to compare (defaults to HEAD) | [optional] 
 **right** | **str**| Hash of the right version to compare (defaults to HEAD) | [optional] 
 **max_rows** | **int**| Maximum number of row changes to include in details | [optional] 

### Return type

[**DocComparison**](DocComparison.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Comparison result |  -  |
**403** | Insufficient access to compare documents |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **copy_doc**
> str copy_doc(doc_id, copy_doc_request=copy_doc_request)

Copies a document to a workspace.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.copy_doc_request import CopyDocRequest
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    copy_doc_request = grist_client.CopyDocRequest() # CopyDocRequest | the target workspace (optional)

    try:
        # Copies a document to a workspace.
        api_response = api_instance.copy_doc(doc_id, copy_doc_request=copy_doc_request)
        print("The response of DocsApi->copy_doc:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->copy_doc: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **copy_doc_request** | [**CopyDocRequest**](CopyDocRequest.md)| the target workspace | [optional] 

### Return type

**str**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The document id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_doc**
> str create_doc(workspace_id, doc_parameters)

Create an empty document

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.doc_parameters import DocParameters
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
    api_instance = grist_client.DocsApi(api_client)
    workspace_id = 56 # int | An integer id
    doc_parameters = grist_client.DocParameters() # DocParameters | settings for the document

    try:
        # Create an empty document
        api_response = api_instance.create_doc(workspace_id, doc_parameters)
        print("The response of DocsApi->create_doc:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->create_doc: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **int**| An integer id | 
 **doc_parameters** | [**DocParameters**](DocParameters.md)| settings for the document | 

### Return type

**str**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The document id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_doc_unified**
> str create_doc_unified(create_doc_unified_request=create_doc_unified_request)

Create a document

A unified endpoint for creating documents. Can create an empty document,
copy an existing document, or import a file.

- To create an empty unsaved document: provide no parameters
- To create an empty saved document: provide `workspaceId`
- To copy an existing document: provide `sourceDocumentId`, `workspaceId`, and `documentName`
- To import a file: use multipart/form-data with a file upload and optional `workspaceId`


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.create_doc_unified_request import CreateDocUnifiedRequest
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
    api_instance = grist_client.DocsApi(api_client)
    create_doc_unified_request = grist_client.CreateDocUnifiedRequest() # CreateDocUnifiedRequest | settings for the document (optional)

    try:
        # Create a document
        api_response = api_instance.create_doc_unified(create_doc_unified_request=create_doc_unified_request)
        print("The response of DocsApi->create_doc_unified:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->create_doc_unified: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_doc_unified_request** | [**CreateDocUnifiedRequest**](CreateDocUnifiedRequest.md)| settings for the document | [optional] 

### Return type

**str**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The document id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_proposal**
> CreateProposal200Response create_proposal(doc_id, create_proposal_request=create_proposal_request)

Create a change proposal

Create a proposal from a fork to its trunk document. The proposal contains
the comparison of changes between the fork and trunk.
This endpoint can only be called on a fork document.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.create_proposal200_response import CreateProposal200Response
from grist_client.models.create_proposal_request import CreateProposalRequest
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    create_proposal_request = grist_client.CreateProposalRequest() # CreateProposalRequest |  (optional)

    try:
        # Create a change proposal
        api_response = api_instance.create_proposal(doc_id, create_proposal_request=create_proposal_request)
        print("The response of DocsApi->create_proposal:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->create_proposal: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **create_proposal_request** | [**CreateProposalRequest**](CreateProposalRequest.md)|  | [optional] 

### Return type

[**CreateProposal200Response**](CreateProposal200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Proposal created |  -  |
**400** | Can only propose from a fork |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_actions**
> delete_actions(doc_id, delete_actions_request=delete_actions_request)

Truncate the document's action history

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.delete_actions_request import DeleteActionsRequest
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    delete_actions_request = grist_client.DeleteActionsRequest() # DeleteActionsRequest |  (optional)

    try:
        # Truncate the document's action history
        api_instance.delete_actions(doc_id, delete_actions_request=delete_actions_request)
    except Exception as e:
        print("Exception when calling DocsApi->delete_actions: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **delete_actions_request** | [**DeleteActionsRequest**](DeleteActionsRequest.md)|  | [optional] 

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
**0** | Response not specified in source documentation; inspect HTTP status and body. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_doc**
> delete_doc(doc_id)

Delete a document

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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Delete a document
        api_instance.delete_doc(doc_id)
    except Exception as e:
        print("Exception when calling DocsApi->delete_doc: %s\n" % e)
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

# **describe_doc**
> DocWithWorkspace describe_doc(doc_id)

Describe a document

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.doc_with_workspace import DocWithWorkspace
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Describe a document
        api_response = api_instance.describe_doc(doc_id)
        print("The response of DocsApi->describe_doc:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->describe_doc: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

[**DocWithWorkspace**](DocWithWorkspace.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A document&#39;s metadata |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **disable_doc**
> disable_doc(doc_id)

Disable a document.

Disabled documents cannot be accessed or modified. Moving and
renaming a disabled doc is also forbidden, as well as
accessing or submitting published forms associated to a
disabled document.

Disabled documents, however, can be moved to and restored from
the trash.

The operation is non-destructive. Disabled documents can be
re-enabled.

Only admin accounts can disable a document.


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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Disable a document.
        api_instance.disable_doc(doc_id)
    except Exception as e:
        print("Exception when calling DocsApi->disable_doc: %s\n" % e)
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
**200** | Document disabled successfully. Returns empty body. |  -  |
**403** | The caller is not allowed to disable this document |  -  |
**404** | The document is not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_doc**
> bytearray download_doc(doc_id, nohistory=nohistory, template=template)

Content of document, as an Sqlite file

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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    nohistory = True # bool |  (optional)
    template = True # bool |  (optional)

    try:
        # Content of document, as an Sqlite file
        api_response = api_instance.download_doc(doc_id, nohistory=nohistory, template=template)
        print("The response of DocsApi->download_doc:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->download_doc: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **nohistory** | **bool**|  | [optional] 
 **template** | **bool**|  | [optional] 

### Return type

**bytearray**

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/x-sqlite3

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A document&#39;s content in Sqlite form |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_doc_csv**
> str download_doc_csv(doc_id, table_id, header=header)

Content of table, as a CSV file

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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | 
    header = 'header_example' # str | Format for headers. Labels tend to be more human-friendly while colIds are more normalized. (optional)

    try:
        # Content of table, as a CSV file
        api_response = api_instance.download_doc_csv(doc_id, table_id, header=header)
        print("The response of DocsApi->download_doc_csv:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->download_doc_csv: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**|  | 
 **header** | **str**| Format for headers. Labels tend to be more human-friendly while colIds are more normalized. | [optional] 

### Return type

**str**

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/csv

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A table&#39;s content in CSV form |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_doc_dsv**
> str download_doc_dsv(doc_id, table_id, header=header)

Content of table, as a DSV file

Download table data using a custom delimiter (💩).

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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | 
    header = 'header_example' # str | Format for headers. Labels tend to be more human-friendly while colIds are more normalized. (optional)

    try:
        # Content of table, as a DSV file
        api_response = api_instance.download_doc_dsv(doc_id, table_id, header=header)
        print("The response of DocsApi->download_doc_dsv:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->download_doc_dsv: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**|  | 
 **header** | **str**| Format for headers. Labels tend to be more human-friendly while colIds are more normalized. | [optional] 

### Return type

**str**

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A table&#39;s content in DSV form |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_doc_tsv**
> str download_doc_tsv(doc_id, table_id, header=header)

Content of table, as a TSV file

Download table data as tab-separated values.

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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | 
    header = 'header_example' # str | Format for headers. Labels tend to be more human-friendly while colIds are more normalized. (optional)

    try:
        # Content of table, as a TSV file
        api_response = api_instance.download_doc_tsv(doc_id, table_id, header=header)
        print("The response of DocsApi->download_doc_tsv:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->download_doc_tsv: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**|  | 
 **header** | **str**| Format for headers. Labels tend to be more human-friendly while colIds are more normalized. | [optional] 

### Return type

**str**

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/tab-separated-values

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A table&#39;s content in TSV form |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_doc_xlsx**
> bytearray download_doc_xlsx(doc_id, header=header, table_id=table_id)

Content of document, as an Excel file

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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    header = 'header_example' # str | Format for headers. Labels tend to be more human-friendly while colIds are more normalized. (optional)
    table_id = 'table_id_example' # str |  (optional)

    try:
        # Content of document, as an Excel file
        api_response = api_instance.download_doc_xlsx(doc_id, header=header, table_id=table_id)
        print("The response of DocsApi->download_doc_xlsx:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->download_doc_xlsx: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **header** | **str**| Format for headers. Labels tend to be more human-friendly while colIds are more normalized. | [optional] 
 **table_id** | **str**|  | [optional] 

### Return type

**bytearray**

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A document&#39;s content in Excel form |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **download_table_schema**
> TableSchemaResult download_table_schema(doc_id, table_id, header=header)

The schema of a table

The schema follows [frictionlessdata's table-schema standard](https://specs.frictionlessdata.io/table-schema/).

### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.table_schema_result import TableSchemaResult
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    table_id = 'table_id_example' # str | 
    header = 'header_example' # str | Format for headers. Labels tend to be more human-friendly while colIds are more normalized. (optional)

    try:
        # The schema of a table
        api_response = api_instance.download_table_schema(doc_id, table_id, header=header)
        print("The response of DocsApi->download_table_schema:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->download_table_schema: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **table_id** | **str**|  | 
 **header** | **str**| Format for headers. Labels tend to be more human-friendly while colIds are more normalized. | [optional] 

### Return type

[**TableSchemaResult**](TableSchemaResult.md)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A table&#39;s table-schema in JSON format. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enable_doc**
> enable_doc(doc_id)

Enable a document.

If a document has been previously disabled, this will restore
all former access to a document, including access to its
associated published forms.

Only admin accounts can enable a document.


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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Enable a document.
        api_instance.enable_doc(doc_id)
    except Exception as e:
        print("Exception when calling DocsApi->enable_doc: %s\n" % e)
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
**200** | Document enabled successfully. Returns empty body. |  -  |
**403** | The caller is not allowed to enable this document |  -  |
**404** | The document is not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **flush_doc**
> bool flush_doc(doc_id)

Flush document to storage

Ensure all pending changes to the document are written to persistent storage.
Returns true if the document was flushed, false if the document was not open.


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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Flush document to storage
        api_response = api_instance.flush_doc(doc_id)
        print("The response of DocsApi->flush_doc:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->flush_doc: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

**bool**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Flush result |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **force_reload**
> force_reload(doc_id)

Reload a document

Closes and reopens the document, forcing the python engine to restart.

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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Reload a document
        api_instance.force_reload(doc_id)
    except Exception as e:
        print("Exception when calling DocsApi->force_reload: %s\n" % e)
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
**200** | Document reloaded successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **fork_doc**
> ForkDoc200Response fork_doc(doc_id)

Fork a document

Create a fork of a document. A fork is a personal copy that tracks its relationship
to the original document. Forks can be used to experiment with changes before
applying them to the original.

The fork will have a new docId and urlId that encode the relationship to the trunk
(original) document.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.fork_doc200_response import ForkDoc200Response
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Fork a document
        api_response = api_instance.fork_doc(doc_id)
        print("The response of DocsApi->fork_doc:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->fork_doc: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

[**ForkDoc200Response**](ForkDoc200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Fork created successfully |  -  |
**400** | Cannot fork a document that&#39;s already a fork |  -  |
**403** | Insufficient access to document to copy it entirely |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_states**
> GetStates200Response get_states(doc_id)

Get document action history states

Returns a list of document states representing the action history.
Each state has a sequential number (n) and a hash (h) that uniquely
identifies that point in history. Most recent state is first.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.get_states200_response import GetStates200Response
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Get document action history states
        api_response = api_instance.get_states(doc_id)
        print("The response of DocsApi->get_states:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->get_states: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

[**GetStates200Response**](GetStates200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of document states |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_timing_status**
> GetTimingStatus200Response get_timing_status(doc_id)

Get formula timing status

Check if formula timing is enabled for a document and retrieve timing data
if available. Only document owners can access timing information.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.get_timing_status200_response import GetTimingStatus200Response
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Get formula timing status
        api_response = api_instance.get_timing_status(doc_id)
        print("The response of DocsApi->get_timing_status:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->get_timing_status: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

[**GetTimingStatus200Response**](GetTimingStatus200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Timing status |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_users_for_view_as**
> GetUsersForViewAs200Response get_users_for_view_as(doc_id)

Get users for 'View As' feature

Get users that can be used with the "View As" feature for testing access rules.
Only document owners can call this endpoint.

Users are drawn from:
- Users the document is shared with
- Users mentioned in user attribute tables
- Predefined example users


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.get_users_for_view_as200_response import GetUsersForViewAs200Response
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Get users for 'View As' feature
        api_response = api_instance.get_users_for_view_as(doc_id)
        print("The response of DocsApi->get_users_for_view_as:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->get_users_for_view_as: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

[**GetUsersForViewAs200Response**](GetUsersForViewAs200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Users available for View As |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **import_doc**
> ImportDoc200Response import_doc(workspace_id, upload=upload, document_name=document_name)

Import an existing document

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.import_doc200_response import ImportDoc200Response
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
    api_instance = grist_client.DocsApi(api_client)
    workspace_id = 56 # int | An integer id
    upload = None # bytearray | Contents of a .grist file, as a standard multipart/form-data file entry (optional)
    document_name = 'document_name_example' # str |  (optional)

    try:
        # Import an existing document
        api_response = api_instance.import_doc(workspace_id, upload=upload, document_name=document_name)
        print("The response of DocsApi->import_doc:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->import_doc: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **int**| An integer id | 
 **upload** | **bytearray**| Contents of a .grist file, as a standard multipart/form-data file entry | [optional] 
 **document_name** | **str**|  | [optional] 

### Return type

[**ImportDoc200Response**](ImportDoc200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The document id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_doc_access**
> WorkspaceAccessRead list_doc_access(doc_id)

List users with access to document

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.workspace_access_read import WorkspaceAccessRead
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # List users with access to document
        api_response = api_instance.list_doc_access(doc_id)
        print("The response of DocsApi->list_doc_access:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->list_doc_access: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

[**WorkspaceAccessRead**](WorkspaceAccessRead.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Users with access to document |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_proposals**
> ListProposals200Response list_proposals(doc_id, outgoing=outgoing)

List change proposals

List proposals associated with a document. Proposals are suggested changes
from forks that can be reviewed and applied to the trunk document.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.list_proposals200_response import ListProposals200Response
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    outgoing = True # bool | If true, list proposals where this document is the source. Otherwise list proposals where this document is the destination. (optional)

    try:
        # List change proposals
        api_response = api_instance.list_proposals(doc_id, outgoing=outgoing)
        print("The response of DocsApi->list_proposals:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->list_proposals: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **outgoing** | **bool**| If true, list proposals where this document is the source. Otherwise list proposals where this document is the destination. | [optional] 

### Return type

[**ListProposals200Response**](ListProposals200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of proposals |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_snapshots**
> ListSnapshots200Response list_snapshots(doc_id, raw=raw)

List document snapshots

Returns a list of snapshots (backups) of the document. Snapshots are created
automatically as the document is edited. Most recent snapshots are listed first.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.list_snapshots200_response import ListSnapshots200Response
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    raw = True # bool | If true, returns all snapshots including those not in the snapshot inventory (optional)

    try:
        # List document snapshots
        api_response = api_instance.list_snapshots(doc_id, raw=raw)
        print("The response of DocsApi->list_snapshots:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->list_snapshots: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **raw** | **bool**| If true, returns all snapshots including those not in the snapshot inventory | [optional] 

### Return type

[**ListSnapshots200Response**](ListSnapshots200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of snapshots |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_doc**
> modify_doc(doc_id, doc_parameters)

Modify document metadata (but not its contents)

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.doc_parameters import DocParameters
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    doc_parameters = grist_client.DocParameters() # DocParameters | the changes to make

    try:
        # Modify document metadata (but not its contents)
        api_instance.modify_doc(doc_id, doc_parameters)
    except Exception as e:
        print("Exception when calling DocsApi->modify_doc: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **doc_parameters** | [**DocParameters**](DocParameters.md)| the changes to make | 

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
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_doc_access**
> modify_doc_access(doc_id, modify_doc_access_request)

Change who has access to document

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.modify_doc_access_request import ModifyDocAccessRequest
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    modify_doc_access_request = grist_client.ModifyDocAccessRequest() # ModifyDocAccessRequest | the changes to make

    try:
        # Change who has access to document
        api_instance.modify_doc_access(doc_id, modify_doc_access_request)
    except Exception as e:
        print("Exception when calling DocsApi->modify_doc_access: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **modify_doc_access_request** | [**ModifyDocAccessRequest**](ModifyDocAccessRequest.md)| the changes to make | 

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
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **move_doc**
> move_doc(doc_id, move_doc_request=move_doc_request)

Move document to another workspace.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.move_doc_request import MoveDocRequest
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    move_doc_request = grist_client.MoveDocRequest() # MoveDocRequest | the target workspace (optional)

    try:
        # Move document to another workspace.
        api_instance.move_doc(doc_id, move_doc_request=move_doc_request)
    except Exception as e:
        print("Exception when calling DocsApi->move_doc: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **move_doc_request** | [**MoveDocRequest**](MoveDocRequest.md)| the target workspace | [optional] 

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
**200** | Document moved successfully. Returns empty body. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pin_doc**
> pin_doc(doc_id)

Pin a document

Pin the document so it appears in a prominent location. Pinned documents
are displayed at the top of workspace listings for easy access.


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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Pin a document
        api_instance.pin_doc(doc_id)
    except Exception as e:
        print("Exception when calling DocsApi->pin_doc: %s\n" % e)
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
**200** | Document pinned successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **recover_doc**
> RecoverDoc200Response recover_doc(doc_id, recover_doc_request=recover_doc_request)

Set recovery mode for a document

Controls the recovery mode of a document. Recovery mode helps in recovering from errors or corrupted states. Only document owners can control recovery mode.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.recover_doc200_response import RecoverDoc200Response
from grist_client.models.recover_doc_request import RecoverDocRequest
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    recover_doc_request = grist_client.RecoverDocRequest() # RecoverDocRequest | Recovery mode settings (optional)

    try:
        # Set recovery mode for a document
        api_response = api_instance.recover_doc(doc_id, recover_doc_request=recover_doc_request)
        print("The response of DocsApi->recover_doc:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->recover_doc: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **recover_doc_request** | [**RecoverDocRequest**](RecoverDocRequest.md)| Recovery mode settings | [optional] 

### Return type

[**RecoverDoc200Response**](RecoverDoc200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Recovery mode set successfully |  -  |
**403** | Access denied - only owners can control recovery mode |  -  |
**404** | Document not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_doc**
> remove_doc(doc_id, permanent=permanent)

Move document to trash

Soft-delete the document by moving it to trash. The document can be
restored using the unremove endpoint. If the `permanent` query parameter
is set to true, the document is permanently deleted instead.


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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    permanent = True # bool | If true, permanently delete instead of moving to trash (optional)

    try:
        # Move document to trash
        api_instance.remove_doc(doc_id, permanent=permanent)
    except Exception as e:
        print("Exception when calling DocsApi->remove_doc: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **permanent** | **bool**| If true, permanently delete instead of moving to trash | [optional] 

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
**200** | Document moved to trash (or permanently deleted) |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_snapshots**
> RemoveSnapshots200Response remove_snapshots(doc_id, remove_snapshots_request=remove_snapshots_request)

Remove document snapshots

Remove specific snapshots from a document's backup history.
Only document owners can remove snapshots.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.remove_snapshots200_response import RemoveSnapshots200Response
from grist_client.models.remove_snapshots_request import RemoveSnapshotsRequest
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    remove_snapshots_request = grist_client.RemoveSnapshotsRequest() # RemoveSnapshotsRequest |  (optional)

    try:
        # Remove document snapshots
        api_response = api_instance.remove_snapshots(doc_id, remove_snapshots_request=remove_snapshots_request)
        print("The response of DocsApi->remove_snapshots:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->remove_snapshots: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **remove_snapshots_request** | [**RemoveSnapshotsRequest**](RemoveSnapshotsRequest.md)|  | [optional] 

### Return type

[**RemoveSnapshots200Response**](RemoveSnapshots200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Snapshots removed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **replace_doc**
> replace_doc(doc_id, replace_doc_request=replace_doc_request)

Replace document content

Replace the current document content with content from another source.
Can restore from a snapshot or copy from another document.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.replace_doc_request import ReplaceDocRequest
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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    replace_doc_request = grist_client.ReplaceDocRequest() # ReplaceDocRequest |  (optional)

    try:
        # Replace document content
        api_instance.replace_doc(doc_id, replace_doc_request=replace_doc_request)
    except Exception as e:
        print("Exception when calling DocsApi->replace_doc: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **replace_doc_request** | [**ReplaceDocRequest**](ReplaceDocRequest.md)|  | [optional] 

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
**200** | Document content replaced successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **start_timing**
> start_timing(doc_id)

Start formula timing

Start collecting timing information for formula calculations.
Only document owners can start timing.


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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Start formula timing
        api_instance.start_timing(doc_id)
    except Exception as e:
        print("Exception when calling DocsApi->start_timing: %s\n" % e)
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
**200** | Timing started successfully |  -  |
**400** | Timing already started for this document |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stop_timing**
> object stop_timing(doc_id)

Stop formula timing

Stop collecting timing information and return the collected data.
Only document owners can stop timing.


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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Stop formula timing
        api_response = api_instance.stop_timing(doc_id)
        print("The response of DocsApi->stop_timing:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DocsApi->stop_timing: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

**object**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Timing stopped and data returned |  -  |
**400** | Timing not started for this document |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unpin_doc**
> unpin_doc(doc_id)

Unpin a document

Remove the pinned status from a document.

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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Unpin a document
        api_instance.unpin_doc(doc_id)
    except Exception as e:
        print("Exception when calling DocsApi->unpin_doc: %s\n" % e)
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
**200** | Document unpinned successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unremove_doc**
> unremove_doc(doc_id)

Restore document from trash

Recover a document that was previously soft-deleted. Only works if the
document is still in the trash.


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
    api_instance = grist_client.DocsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Restore document from trash
        api_instance.unremove_doc(doc_id)
    except Exception as e:
        print("Exception when calling DocsApi->unremove_doc: %s\n" % e)
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
**200** | Document restored successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

