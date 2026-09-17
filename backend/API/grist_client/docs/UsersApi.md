# grist_client.UsersApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_user**](UsersApi.md#delete_user) | **DELETE** /users/{userId} | Delete a user from Grist
[**disable_user**](UsersApi.md#disable_user) | **POST** /users/{userId}/disable | Disable a user
[**enable_user**](UsersApi.md#enable_user) | **POST** /users/{userId}/enable | Enable a user


# **delete_user**
> delete_user(user_id, delete_user_request=delete_user_request)

Delete a user from Grist

This action also deletes the user's personal organisation and all the workspaces and documents it contains.
Currently, only the users themselves are allowed to delete their own accounts.

⚠️ **This action cannot be undone, please be cautious when using this endpoint** ⚠️


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.delete_user_request import DeleteUserRequest
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
    api_instance = grist_client.UsersApi(api_client)
    user_id = 56 # int | A user id
    delete_user_request = grist_client.DeleteUserRequest() # DeleteUserRequest |  (optional)

    try:
        # Delete a user from Grist
        api_instance.delete_user(user_id, delete_user_request=delete_user_request)
    except Exception as e:
        print("Exception when calling UsersApi->delete_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_id** | **int**| A user id | 
 **delete_user_request** | [**DeleteUserRequest**](DeleteUserRequest.md)|  | [optional] 

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
**200** | The account has been deleted successfully |  -  |
**400** | The passed user name does not match the one retrieved from the database given the passed user id |  -  |
**403** | The caller is not allowed to delete this account |  -  |
**404** | The user is not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **disable_user**
> disable_user(user_id)

Disable a user

A disabled user can not log in and loses access to all pages,
including public ones, as well as API access. The operation is
non-destructive. Disabled users can be re-enabled.

Only admin accounts can disable a user.


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
    api_instance = grist_client.UsersApi(api_client)
    user_id = 56 # int | A user id

    try:
        # Disable a user
        api_instance.disable_user(user_id)
    except Exception as e:
        print("Exception when calling UsersApi->disable_user: %s\n" % e)
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
**200** | The account has been disabled successfully |  -  |
**403** | The caller is not allowed to disable this account |  -  |
**404** | The user is not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **enable_user**
> enable_user(user_id)

Enable a user

If a user has been disabled, this will restore their access, including API access.

Only admin accounts can enable a user.


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
    api_instance = grist_client.UsersApi(api_client)
    user_id = 56 # int | A user id

    try:
        # Enable a user
        api_instance.enable_user(user_id)
    except Exception as e:
        print("Exception when calling UsersApi->enable_user: %s\n" % e)
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
**200** | The account has been enabled successfully |  -  |
**403** | The caller is not allowed to enable this account |  -  |
**404** | The user is not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

