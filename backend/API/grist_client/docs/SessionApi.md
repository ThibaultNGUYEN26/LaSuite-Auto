# grist_client.SessionApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_active_session**](SessionApi.md#get_active_session) | **GET** /session/access/active | Get active session information
[**get_all_sessions**](SessionApi.md#get_all_sessions) | **GET** /session/access/all | Get all session users and organizations
[**set_active_user**](SessionApi.md#set_active_user) | **POST** /session/access/active | Set active user for organization


# **get_active_session**
> GetActiveSession200Response get_active_session()

Get active session information

Returns information about the active user and organization for the current session.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.get_active_session200_response import GetActiveSession200Response
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
    api_instance = grist_client.SessionApi(api_client)

    try:
        # Get active session information
        api_response = api_instance.get_active_session()
        print("The response of SessionApi->get_active_session:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SessionApi->get_active_session: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetActiveSession200Response**](GetActiveSession200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Active session info |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_sessions**
> GetAllSessions200Response get_all_sessions()

Get all session users and organizations

Returns all user profiles logged into the current session and all
organizations they can access.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.get_all_sessions200_response import GetAllSessions200Response
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
    api_instance = grist_client.SessionApi(api_client)

    try:
        # Get all session users and organizations
        api_response = api_instance.get_all_sessions()
        print("The response of SessionApi->get_all_sessions:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SessionApi->get_all_sessions: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**GetAllSessions200Response**](GetAllSessions200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | All session info |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_active_user**
> SetActiveUser200Response set_active_user(set_active_user_request=set_active_user_request)

Set active user for organization

Switch which user account is active for a given organization.
Useful when a user has multiple accounts logged in.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.set_active_user200_response import SetActiveUser200Response
from grist_client.models.set_active_user_request import SetActiveUserRequest
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
    api_instance = grist_client.SessionApi(api_client)
    set_active_user_request = grist_client.SetActiveUserRequest() # SetActiveUserRequest |  (optional)

    try:
        # Set active user for organization
        api_response = api_instance.set_active_user(set_active_user_request=set_active_user_request)
        print("The response of SessionApi->set_active_user:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SessionApi->set_active_user: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **set_active_user_request** | [**SetActiveUserRequest**](SetActiveUserRequest.md)|  | [optional] 

### Return type

[**SetActiveUser200Response**](SetActiveUser200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Active user changed |  -  |
**403** | Email not available for this session |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

