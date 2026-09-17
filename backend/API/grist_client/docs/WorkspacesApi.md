# grist_client.WorkspacesApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_workspace**](WorkspacesApi.md#create_workspace) | **POST** /orgs/{orgId}/workspaces | Create an empty workspace
[**delete_workspace**](WorkspacesApi.md#delete_workspace) | **DELETE** /workspaces/{workspaceId} | Delete a workspace
[**describe_workspace**](WorkspacesApi.md#describe_workspace) | **GET** /workspaces/{workspaceId} | Describe a workspace
[**list_workspace_access**](WorkspacesApi.md#list_workspace_access) | **GET** /workspaces/{workspaceId}/access | List users with access to workspace
[**list_workspaces**](WorkspacesApi.md#list_workspaces) | **GET** /orgs/{orgId}/workspaces | List workspaces and documents within an org
[**modify_workspace**](WorkspacesApi.md#modify_workspace) | **PATCH** /workspaces/{workspaceId} | Modify a workspace
[**modify_workspace_access**](WorkspacesApi.md#modify_workspace_access) | **PATCH** /workspaces/{workspaceId}/access | Change who has access to workspace
[**remove_workspace**](WorkspacesApi.md#remove_workspace) | **POST** /workspaces/{workspaceId}/remove | Move workspace to trash
[**unremove_workspace**](WorkspacesApi.md#unremove_workspace) | **POST** /workspaces/{workspaceId}/unremove | Restore workspace from trash


# **create_workspace**
> int create_workspace(org_id, workspace_parameters)

Create an empty workspace

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.workspace_parameters import WorkspaceParameters
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
    api_instance = grist_client.WorkspacesApi(api_client)
    org_id = grist_client.DescribeOrgOrgIdParameter() # DescribeOrgOrgIdParameter | This can be an integer id, or a string subdomain (e.g. `gristlabs`), or `current` if the org is implied by the domain in the url
    workspace_parameters = grist_client.WorkspaceParameters() # WorkspaceParameters | settings for the workspace

    try:
        # Create an empty workspace
        api_response = api_instance.create_workspace(org_id, workspace_parameters)
        print("The response of WorkspacesApi->create_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->create_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | [**DescribeOrgOrgIdParameter**](.md)| This can be an integer id, or a string subdomain (e.g. &#x60;gristlabs&#x60;), or &#x60;current&#x60; if the org is implied by the domain in the url | 
 **workspace_parameters** | [**WorkspaceParameters**](WorkspaceParameters.md)| settings for the workspace | 

### Return type

**int**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The workspace id |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_workspace**
> delete_workspace(workspace_id)

Delete a workspace

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
    api_instance = grist_client.WorkspacesApi(api_client)
    workspace_id = 56 # int | An integer id

    try:
        # Delete a workspace
        api_instance.delete_workspace(workspace_id)
    except Exception as e:
        print("Exception when calling WorkspacesApi->delete_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **int**| An integer id | 

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

# **describe_workspace**
> WorkspaceWithDocsAndOrg describe_workspace(workspace_id)

Describe a workspace

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.workspace_with_docs_and_org import WorkspaceWithDocsAndOrg
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
    api_instance = grist_client.WorkspacesApi(api_client)
    workspace_id = 56 # int | An integer id

    try:
        # Describe a workspace
        api_response = api_instance.describe_workspace(workspace_id)
        print("The response of WorkspacesApi->describe_workspace:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->describe_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **int**| An integer id | 

### Return type

[**WorkspaceWithDocsAndOrg**](WorkspaceWithDocsAndOrg.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A workspace |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_workspace_access**
> WorkspaceAccessRead list_workspace_access(workspace_id)

List users with access to workspace

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
    api_instance = grist_client.WorkspacesApi(api_client)
    workspace_id = 56 # int | An integer id

    try:
        # List users with access to workspace
        api_response = api_instance.list_workspace_access(workspace_id)
        print("The response of WorkspacesApi->list_workspace_access:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->list_workspace_access: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **int**| An integer id | 

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
**200** | Users with access to workspace |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_workspaces**
> List[WorkspaceWithDocsAndDomain] list_workspaces(org_id)

List workspaces and documents within an org

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.workspace_with_docs_and_domain import WorkspaceWithDocsAndDomain
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
    api_instance = grist_client.WorkspacesApi(api_client)
    org_id = grist_client.DescribeOrgOrgIdParameter() # DescribeOrgOrgIdParameter | This can be an integer id, or a string subdomain (e.g. `gristlabs`), or `current` if the org is implied by the domain in the url

    try:
        # List workspaces and documents within an org
        api_response = api_instance.list_workspaces(org_id)
        print("The response of WorkspacesApi->list_workspaces:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->list_workspaces: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | [**DescribeOrgOrgIdParameter**](.md)| This can be an integer id, or a string subdomain (e.g. &#x60;gristlabs&#x60;), or &#x60;current&#x60; if the org is implied by the domain in the url | 

### Return type

[**List[WorkspaceWithDocsAndDomain]**](WorkspaceWithDocsAndDomain.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | An org&#39;s workspaces and documents |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_workspace**
> modify_workspace(workspace_id, workspace_parameters)

Modify a workspace

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.workspace_parameters import WorkspaceParameters
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
    api_instance = grist_client.WorkspacesApi(api_client)
    workspace_id = 56 # int | An integer id
    workspace_parameters = grist_client.WorkspaceParameters() # WorkspaceParameters | the changes to make

    try:
        # Modify a workspace
        api_instance.modify_workspace(workspace_id, workspace_parameters)
    except Exception as e:
        print("Exception when calling WorkspacesApi->modify_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **int**| An integer id | 
 **workspace_parameters** | [**WorkspaceParameters**](WorkspaceParameters.md)| the changes to make | 

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

# **modify_workspace_access**
> modify_workspace_access(workspace_id, modify_workspace_access_request)

Change who has access to workspace

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.modify_workspace_access_request import ModifyWorkspaceAccessRequest
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
    api_instance = grist_client.WorkspacesApi(api_client)
    workspace_id = 56 # int | An integer id
    modify_workspace_access_request = grist_client.ModifyWorkspaceAccessRequest() # ModifyWorkspaceAccessRequest | the changes to make

    try:
        # Change who has access to workspace
        api_instance.modify_workspace_access(workspace_id, modify_workspace_access_request)
    except Exception as e:
        print("Exception when calling WorkspacesApi->modify_workspace_access: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **int**| An integer id | 
 **modify_workspace_access_request** | [**ModifyWorkspaceAccessRequest**](ModifyWorkspaceAccessRequest.md)| the changes to make | 

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

# **remove_workspace**
> remove_workspace(workspace_id, permanent=permanent)

Move workspace to trash

Soft-delete the workspace by moving it to trash. The workspace can be
restored using the unremove endpoint. If the `permanent` query parameter
is set to true, the workspace is permanently deleted instead.


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
    api_instance = grist_client.WorkspacesApi(api_client)
    workspace_id = 56 # int | An integer id
    permanent = True # bool | If true, permanently delete instead of moving to trash (optional)

    try:
        # Move workspace to trash
        api_instance.remove_workspace(workspace_id, permanent=permanent)
    except Exception as e:
        print("Exception when calling WorkspacesApi->remove_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **int**| An integer id | 
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
**200** | Workspace moved to trash (or permanently deleted) |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unremove_workspace**
> unremove_workspace(workspace_id)

Restore workspace from trash

Recover a workspace that was previously soft-deleted. Only works if the
workspace is still in the trash.


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
    api_instance = grist_client.WorkspacesApi(api_client)
    workspace_id = 56 # int | An integer id

    try:
        # Restore workspace from trash
        api_instance.unremove_workspace(workspace_id)
    except Exception as e:
        print("Exception when calling WorkspacesApi->unremove_workspace: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **int**| An integer id | 

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
**200** | Workspace restored successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

