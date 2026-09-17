# grist_client.ScimApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**bulk_operation**](ScimApi.md#bulk_operation) | **POST** /scim/v2/Bulk | Bulk operation
[**create_group**](ScimApi.md#create_group) | **POST** /scim/v2/Groups | Create a new group
[**create_user**](ScimApi.md#create_user) | **POST** /scim/v2/Users | Create a new user
[**delete_group_by_id**](ScimApi.md#delete_group_by_id) | **DELETE** /scim/v2/Groups/{groupId} | Delete a group by ID.
[**delete_user_by_id**](ScimApi.md#delete_user_by_id) | **DELETE** /scim/v2/Users/{userId} | Delete a user by ID.
[**get_group_by_id**](ScimApi.md#get_group_by_id) | **GET** /scim/v2/Groups/{groupId} | Retrieve group by ID
[**get_groups**](ScimApi.md#get_groups) | **GET** /scim/v2/Groups | Retrieve list of groups
[**get_me**](ScimApi.md#get_me) | **GET** /scim/v2/Me | Retrieve information about oneself
[**get_resource_types**](ScimApi.md#get_resource_types) | **GET** /scim/v2/ResourceTypes | Retrieve SCIM resource types
[**get_role_by_id**](ScimApi.md#get_role_by_id) | **GET** /scim/v2/Roles/{roleId} | Retrieve role by ID
[**get_roles**](ScimApi.md#get_roles) | **GET** /scim/v2/Roles | Retrieve list of roles.
[**get_schemas**](ScimApi.md#get_schemas) | **GET** /scim/v2/Schemas | Retrieve SCIM schemas
[**get_service_provider_config**](ScimApi.md#get_service_provider_config) | **GET** /scim/v2/ServiceProviderConfig | Retrieve service provider configuration
[**get_user_by_id**](ScimApi.md#get_user_by_id) | **GET** /scim/v2/Users/{userId} | Retrieve user by ID
[**get_users**](ScimApi.md#get_users) | **GET** /scim/v2/Users | Retrieve list of users
[**patch_group_by_id**](ScimApi.md#patch_group_by_id) | **PATCH** /scim/v2/Groups/{groupId} | Partially update a group by ID
[**patch_role_by_id**](ScimApi.md#patch_role_by_id) | **PATCH** /scim/v2/Roles/{roleId} | Partially update a role by ID
[**patch_user_by_id**](ScimApi.md#patch_user_by_id) | **PATCH** /scim/v2/Users/{userId} | Partially update a user by ID
[**search_groups**](ScimApi.md#search_groups) | **POST** /scim/v2/Groups/.search | Search groups
[**search_users**](ScimApi.md#search_users) | **POST** /scim/v2/Users/.search | Search users
[**update_group_by_id**](ScimApi.md#update_group_by_id) | **PUT** /scim/v2/Groups/{groupId} | Update a group by ID
[**update_role_by_id**](ScimApi.md#update_role_by_id) | **PUT** /scim/v2/Roles/{roleId} | Update a role by ID
[**update_user_by_id**](ScimApi.md#update_user_by_id) | **PUT** /scim/v2/Users/{userId} | Update a user by ID


# **bulk_operation**
> bulk_operation(bulk_operation_request)

Bulk operation

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.bulk_operation_request import BulkOperationRequest
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
    api_instance = grist_client.ScimApi(api_client)
    bulk_operation_request = grist_client.BulkOperationRequest() # BulkOperationRequest | Operations to be performed in bulk.

    try:
        # Bulk operation
        api_instance.bulk_operation(bulk_operation_request)
    except Exception as e:
        print("Exception when calling ScimApi->bulk_operation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **bulk_operation_request** | [**BulkOperationRequest**](BulkOperationRequest.md)| Operations to be performed in bulk. | 

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/scim+json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Bulk operations executed successfully. |  -  |
**400** | Bad request. |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_group**
> GroupInResponse create_group(group_in_request)

Create a new group

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.group_in_request import GroupInRequest
from grist_client.models.group_in_response import GroupInResponse
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
    api_instance = grist_client.ScimApi(api_client)
    group_in_request = grist_client.GroupInRequest() # GroupInRequest | Data for the group to be created.

    try:
        # Create a new group
        api_response = api_instance.create_group(group_in_request)
        print("The response of ScimApi->create_group:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->create_group: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_in_request** | [**GroupInRequest**](GroupInRequest.md)| Data for the group to be created. | 

### Return type

[**GroupInResponse**](GroupInResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/scim+json
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Group created successfully. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**409** | Conflict on resource (like displayName). |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user**
> UserInResponse create_user(user_in_request)

Create a new user

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.user_in_request import UserInRequest
from grist_client.models.user_in_response import UserInResponse
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
    api_instance = grist_client.ScimApi(api_client)
    user_in_request = grist_client.UserInRequest() # UserInRequest | Data for the user to be created.

    try:
        # Create a new user
        api_response = api_instance.create_user(user_in_request)
        print("The response of ScimApi->create_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->create_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_in_request** | [**UserInRequest**](UserInRequest.md)| Data for the user to be created. | 

### Return type

[**UserInResponse**](UserInResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/scim+json
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | User created successfully. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**409** | Conflict on resource (like email). |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_group_by_id**
> delete_group_by_id(group_id)

Delete a group by ID.

⚠️ **This action cannot be undone, please be cautious when using this endpoint** ⚠️

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
    api_instance = grist_client.ScimApi(api_client)
    group_id = 56 # int | A group id

    try:
        # Delete a group by ID.
        api_instance.delete_group_by_id(group_id)
    except Exception as e:
        print("Exception when calling ScimApi->delete_group_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **int**| A group id | 

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
**204** | Group deleted successfully. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**404** | Group not found. |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_by_id**
> delete_user_by_id(user_id)

Delete a user by ID.

⚠️ **This action cannot be undone, please be cautious when using this endpoint** ⚠️

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
    api_instance = grist_client.ScimApi(api_client)
    user_id = 56 # int | A user id

    try:
        # Delete a user by ID.
        api_instance.delete_user_by_id(user_id)
    except Exception as e:
        print("Exception when calling ScimApi->delete_user_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**| A user id | 

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
**204** | User deleted successfully. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**404** | User not found. |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_group_by_id**
> GroupInResponse get_group_by_id(group_id)

Retrieve group by ID

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.group_in_response import GroupInResponse
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
    api_instance = grist_client.ScimApi(api_client)
    group_id = 56 # int | A group id

    try:
        # Retrieve group by ID
        api_response = api_instance.get_group_by_id(group_id)
        print("The response of ScimApi->get_group_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->get_group_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **int**| A group id | 

### Return type

[**GroupInResponse**](GroupInResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved group details. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**404** | Group not found. |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_groups**
> GroupsListResponse get_groups(start_index=start_index, count=count, filter=filter)

Retrieve list of groups

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.groups_list_response import GroupsListResponse
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
    api_instance = grist_client.ScimApi(api_client)
    start_index = 1 # int | The starting index for pagination. (optional)
    count = 10 # int | The number of resources to retrieve. (optional)
    filter = 'displayName pr' # str | Filter resources based on specific criteria. (optional)

    try:
        # Retrieve list of groups
        api_response = api_instance.get_groups(start_index=start_index, count=count, filter=filter)
        print("The response of ScimApi->get_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->get_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_index** | **int**| The starting index for pagination. | [optional] 
 **count** | **int**| The number of resources to retrieve. | [optional] 
 **filter** | **str**| Filter resources based on specific criteria. | [optional] 

### Return type

[**GroupsListResponse**](GroupsListResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved list of groups. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_me**
> UserInResponse get_me()

Retrieve information about oneself

When SCIM is enabled, this endpoint is accessible by anyone authentified in Grist.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.user_in_response import UserInResponse
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
    api_instance = grist_client.ScimApi(api_client)

    try:
        # Retrieve information about oneself
        api_response = api_instance.get_me()
        print("The response of ScimApi->get_me:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->get_me: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UserInResponse**](UserInResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved user details. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**404** | User not found. |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_resource_types**
> get_resource_types()

Retrieve SCIM resource types

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
    api_instance = grist_client.ScimApi(api_client)

    try:
        # Retrieve SCIM resource types
        api_instance.get_resource_types()
    except Exception as e:
        print("Exception when calling ScimApi->get_resource_types: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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
**200** | Successfully retrieved resource types. |  -  |
**401** | Unauthenticated |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_role_by_id**
> RoleInGetResponse get_role_by_id(role_id)

Retrieve role by ID

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.role_in_get_response import RoleInGetResponse
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
    api_instance = grist_client.ScimApi(api_client)
    role_id = 56 # int | A role id

    try:
        # Retrieve role by ID
        api_response = api_instance.get_role_by_id(role_id)
        print("The response of ScimApi->get_role_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->get_role_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **int**| A role id | 

### Return type

[**RoleInGetResponse**](RoleInGetResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved role details. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**404** | Role not found. |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_roles**
> RolesListResponse get_roles(start_index=start_index, count=count, filter=filter)

Retrieve list of roles.

Roles are system-defined entities giving particular permissions to a given resource (document, workspace or organization).
This API returns by default all these roles associated to all the resources.
You may use the parameters to filter the results.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.roles_list_response import RolesListResponse
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
    api_instance = grist_client.ScimApi(api_client)
    start_index = 1 # int | The starting index for pagination. (optional)
    count = 10 # int | The number of resources to retrieve. (optional)
    filter = 'displayName pr' # str | Filter resources based on specific criteria. (optional)

    try:
        # Retrieve list of roles.
        api_response = api_instance.get_roles(start_index=start_index, count=count, filter=filter)
        print("The response of ScimApi->get_roles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->get_roles: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_index** | **int**| The starting index for pagination. | [optional] 
 **count** | **int**| The number of resources to retrieve. | [optional] 
 **filter** | **str**| Filter resources based on specific criteria. | [optional] 

### Return type

[**RolesListResponse**](RolesListResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved list of roles. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_schemas**
> get_schemas()

Retrieve SCIM schemas

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
    api_instance = grist_client.ScimApi(api_client)

    try:
        # Retrieve SCIM schemas
        api_instance.get_schemas()
    except Exception as e:
        print("Exception when calling ScimApi->get_schemas: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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
**200** | Successfully retrieved schemas. |  -  |
**401** | Unauthenticated |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_service_provider_config**
> get_service_provider_config()

Retrieve service provider configuration

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
    api_instance = grist_client.ScimApi(api_client)

    try:
        # Retrieve service provider configuration
        api_instance.get_service_provider_config()
    except Exception as e:
        print("Exception when calling ScimApi->get_service_provider_config: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

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
**200** | Successfully retrieved service provider configuration. |  -  |
**401** | Unauthenticated |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_user_by_id**
> UserInResponse get_user_by_id(user_id)

Retrieve user by ID

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.user_in_response import UserInResponse
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
    api_instance = grist_client.ScimApi(api_client)
    user_id = 56 # int | A user id

    try:
        # Retrieve user by ID
        api_response = api_instance.get_user_by_id(user_id)
        print("The response of ScimApi->get_user_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->get_user_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**| A user id | 

### Return type

[**UserInResponse**](UserInResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved user details. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**404** | User not found. |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_users**
> UsersListResponse get_users(start_index=start_index, count=count, filter=filter)

Retrieve list of users

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.users_list_response import UsersListResponse
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
    api_instance = grist_client.ScimApi(api_client)
    start_index = 1 # int | The starting index for pagination. (optional)
    count = 10 # int | The number of resources to retrieve. (optional)
    filter = 'displayName pr' # str | Filter resources based on specific criteria. (optional)

    try:
        # Retrieve list of users
        api_response = api_instance.get_users(start_index=start_index, count=count, filter=filter)
        print("The response of ScimApi->get_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->get_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **start_index** | **int**| The starting index for pagination. | [optional] 
 **count** | **int**| The number of resources to retrieve. | [optional] 
 **filter** | **str**| Filter resources based on specific criteria. | [optional] 

### Return type

[**UsersListResponse**](UsersListResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successfully retrieved list of users. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_group_by_id**
> GroupInResponse patch_group_by_id(group_id, patch_group_by_id_request)

Partially update a group by ID

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.group_in_response import GroupInResponse
from grist_client.models.patch_group_by_id_request import PatchGroupByIdRequest
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
    api_instance = grist_client.ScimApi(api_client)
    group_id = 56 # int | A group id
    patch_group_by_id_request = grist_client.PatchGroupByIdRequest() # PatchGroupByIdRequest | Data for the partial update of the group.

    try:
        # Partially update a group by ID
        api_response = api_instance.patch_group_by_id(group_id, patch_group_by_id_request)
        print("The response of ScimApi->patch_group_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->patch_group_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **int**| A group id | 
 **patch_group_by_id_request** | [**PatchGroupByIdRequest**](PatchGroupByIdRequest.md)| Data for the partial update of the group. | 

### Return type

[**GroupInResponse**](GroupInResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/scim+json
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Group partially updated successfully. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**404** | Group not found. |  -  |
**409** | Conflict on resource (like displayName). |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_role_by_id**
> RoleInResponse patch_role_by_id(role_id, patch_group_by_id_request)

Partially update a role by ID

Only the memberships are authorized to be modified through this endpoint, other properties will be ignored.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.patch_group_by_id_request import PatchGroupByIdRequest
from grist_client.models.role_in_response import RoleInResponse
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
    api_instance = grist_client.ScimApi(api_client)
    role_id = 56 # int | A role id
    patch_group_by_id_request = grist_client.PatchGroupByIdRequest() # PatchGroupByIdRequest | Data for the partial update of the role.

    try:
        # Partially update a role by ID
        api_response = api_instance.patch_role_by_id(role_id, patch_group_by_id_request)
        print("The response of ScimApi->patch_role_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->patch_role_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **int**| A role id | 
 **patch_group_by_id_request** | [**PatchGroupByIdRequest**](PatchGroupByIdRequest.md)| Data for the partial update of the role. | 

### Return type

[**RoleInResponse**](RoleInResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/scim+json
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Role partially updated successfully. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**404** | Role not found. |  -  |
**409** | Conflict on resource (like displayName). |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_user_by_id**
> UserInResponse patch_user_by_id(user_id, patch_user_by_id_request)

Partially update a user by ID

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.patch_user_by_id_request import PatchUserByIdRequest
from grist_client.models.user_in_response import UserInResponse
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
    api_instance = grist_client.ScimApi(api_client)
    user_id = 56 # int | A user id
    patch_user_by_id_request = grist_client.PatchUserByIdRequest() # PatchUserByIdRequest | Data for the partial update of the user.

    try:
        # Partially update a user by ID
        api_response = api_instance.patch_user_by_id(user_id, patch_user_by_id_request)
        print("The response of ScimApi->patch_user_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->patch_user_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**| A user id | 
 **patch_user_by_id_request** | [**PatchUserByIdRequest**](PatchUserByIdRequest.md)| Data for the partial update of the user. | 

### Return type

[**UserInResponse**](UserInResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/scim+json
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User partially updated successfully. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**404** | User not found. |  -  |
**409** | Conflict on resource (like email). |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_groups**
> SearchGroups200Response search_groups(search_groups_request)

Search groups

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.search_groups200_response import SearchGroups200Response
from grist_client.models.search_groups_request import SearchGroupsRequest
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
    api_instance = grist_client.ScimApi(api_client)
    search_groups_request = grist_client.SearchGroupsRequest() # SearchGroupsRequest | Search criteria.

    try:
        # Search groups
        api_response = api_instance.search_groups(search_groups_request)
        print("The response of ScimApi->search_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->search_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search_groups_request** | [**SearchGroupsRequest**](SearchGroupsRequest.md)| Search criteria. | 

### Return type

[**SearchGroups200Response**](SearchGroups200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/scim+json
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Groups retrieved based on search criteria. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_users**
> SearchUsers200Response search_users(search_users_request)

Search users

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.search_users200_response import SearchUsers200Response
from grist_client.models.search_users_request import SearchUsersRequest
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
    api_instance = grist_client.ScimApi(api_client)
    search_users_request = grist_client.SearchUsersRequest() # SearchUsersRequest | Search criteria.

    try:
        # Search users
        api_response = api_instance.search_users(search_users_request)
        print("The response of ScimApi->search_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->search_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search_users_request** | [**SearchUsersRequest**](SearchUsersRequest.md)| Search criteria. | 

### Return type

[**SearchUsers200Response**](SearchUsers200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/scim+json
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Users retrieved based on search criteria. |  -  |
**400** | Bad request. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_group_by_id**
> GroupInResponse update_group_by_id(group_id, group_in_request)

Update a group by ID

⚠️ This operation overwrites all the group's information. In order to pass only some properties to update, please use [PATCH](#tag/scim/operation/patchGroupById) instead.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.group_in_request import GroupInRequest
from grist_client.models.group_in_response import GroupInResponse
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
    api_instance = grist_client.ScimApi(api_client)
    group_id = 56 # int | A group id
    group_in_request = grist_client.GroupInRequest() # GroupInRequest | Updated data for the group.

    try:
        # Update a group by ID
        api_response = api_instance.update_group_by_id(group_id, group_in_request)
        print("The response of ScimApi->update_group_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->update_group_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **group_id** | **int**| A group id | 
 **group_in_request** | [**GroupInRequest**](GroupInRequest.md)| Updated data for the group. | 

### Return type

[**GroupInResponse**](GroupInResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/scim+json
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Group updated successfully. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**404** | Group not found. |  -  |
**409** | Conflict on resource (like displayName). |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_role_by_id**
> RoleInResponse update_role_by_id(role_id, role_in_request)

Update a role by ID

⚠️ This operation overwrites all the memberships (the "members" property). In order to update part of the membership, please use [PATCH](#tag/scim/operation/patchRoleById) instead.
Only the memberships are authorized to be modified through this endpoint, other properties will be ignored.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.role_in_request import RoleInRequest
from grist_client.models.role_in_response import RoleInResponse
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
    api_instance = grist_client.ScimApi(api_client)
    role_id = 56 # int | A role id
    role_in_request = grist_client.RoleInRequest() # RoleInRequest | Updated data for the role.

    try:
        # Update a role by ID
        api_response = api_instance.update_role_by_id(role_id, role_in_request)
        print("The response of ScimApi->update_role_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->update_role_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **role_id** | **int**| A role id | 
 **role_in_request** | [**RoleInRequest**](RoleInRequest.md)| Updated data for the role. | 

### Return type

[**RoleInResponse**](RoleInResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/scim+json
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Role updated successfully. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**404** | Role not found. |  -  |
**409** | Conflict on resource (like displayName). |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_by_id**
> UserInResponse update_user_by_id(user_id, user_in_request)

Update a user by ID

⚠️  This operation overwrites all the user's information. In order to pass only some properties to update, please use [PATCH](#tag/scim/operation/patchUserById) instead.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.user_in_request import UserInRequest
from grist_client.models.user_in_response import UserInResponse
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
    api_instance = grist_client.ScimApi(api_client)
    user_id = 56 # int | A user id
    user_in_request = grist_client.UserInRequest() # UserInRequest | Updated data for the user.

    try:
        # Update a user by ID
        api_response = api_instance.update_user_by_id(user_id, user_in_request)
        print("The response of ScimApi->update_user_by_id:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ScimApi->update_user_by_id: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**| A user id | 
 **user_in_request** | [**UserInRequest**](UserInRequest.md)| Updated data for the user. | 

### Return type

[**UserInResponse**](UserInResponse.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/scim+json
 - **Accept**: application/scim+json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User updated successfully. |  -  |
**401** | Unauthenticated |  -  |
**403** | Unauthorized |  -  |
**404** | User not found. |  -  |
**409** | Conflict on resource (like email). |  -  |
**500** | Internal server error. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

