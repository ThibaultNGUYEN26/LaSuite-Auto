# grist_client.ProfileApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_api_key**](ProfileApi.md#create_api_key) | **POST** /profile/apikey | Create or regenerate API key
[**delete_api_key**](ProfileApi.md#delete_api_key) | **DELETE** /profile/apikey | Delete user&#39;s API key
[**get_api_key**](ProfileApi.md#get_api_key) | **GET** /profile/apikey | Get user&#39;s API key
[**get_profile**](ProfileApi.md#get_profile) | **GET** /profile/user | Get current user&#39;s profile
[**update_user_locale**](ProfileApi.md#update_user_locale) | **POST** /profile/user/locale | Update user&#39;s locale
[**update_user_name**](ProfileApi.md#update_user_name) | **POST** /profile/user/name | Update user&#39;s name


# **create_api_key**
> str create_api_key(create_api_key_request=create_api_key_request)

Create or regenerate API key

Create a new API key or regenerate an existing one.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.create_api_key_request import CreateApiKeyRequest
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
    api_instance = grist_client.ProfileApi(api_client)
    create_api_key_request = grist_client.CreateApiKeyRequest() # CreateApiKeyRequest |  (optional)

    try:
        # Create or regenerate API key
        api_response = api_instance.create_api_key(create_api_key_request=create_api_key_request)
        print("The response of ProfileApi->create_api_key:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->create_api_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_api_key_request** | [**CreateApiKeyRequest**](CreateApiKeyRequest.md)|  | [optional] 

### Return type

**str**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | New API key |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_api_key**
> delete_api_key()

Delete user's API key

Delete the current user's API key.

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
    api_instance = grist_client.ProfileApi(api_client)

    try:
        # Delete user's API key
        api_instance.delete_api_key()
    except Exception as e:
        print("Exception when calling ProfileApi->delete_api_key: %s\n" % e)
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
**200** | API key deleted successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_api_key**
> str get_api_key()

Get user's API key

Returns the current user's API key if one exists.

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
    api_instance = grist_client.ProfileApi(api_client)

    try:
        # Get user's API key
        api_response = api_instance.get_api_key()
        print("The response of ProfileApi->get_api_key:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->get_api_key: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**str**

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | API key |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_profile**
> User get_profile()

Get current user's profile

Returns the profile information of the currently authenticated user.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.user import User
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
    api_instance = grist_client.ProfileApi(api_client)

    try:
        # Get current user's profile
        api_response = api_instance.get_profile()
        print("The response of ProfileApi->get_profile:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ProfileApi->get_profile: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**User**](User.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | User profile |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_locale**
> update_user_locale(update_user_locale_request=update_user_locale_request)

Update user's locale

Update the locale preference for the current user.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.update_user_locale_request import UpdateUserLocaleRequest
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
    api_instance = grist_client.ProfileApi(api_client)
    update_user_locale_request = grist_client.UpdateUserLocaleRequest() # UpdateUserLocaleRequest |  (optional)

    try:
        # Update user's locale
        api_instance.update_user_locale(update_user_locale_request=update_user_locale_request)
    except Exception as e:
        print("Exception when calling ProfileApi->update_user_locale: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_user_locale_request** | [**UpdateUserLocaleRequest**](UpdateUserLocaleRequest.md)|  | [optional] 

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
**200** | Locale updated successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_name**
> update_user_name(update_user_name_request=update_user_name_request)

Update user's name

Update the display name for the current user.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.update_user_name_request import UpdateUserNameRequest
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
    api_instance = grist_client.ProfileApi(api_client)
    update_user_name_request = grist_client.UpdateUserNameRequest() # UpdateUserNameRequest |  (optional)

    try:
        # Update user's name
        api_instance.update_user_name(update_user_name_request=update_user_name_request)
    except Exception as e:
        print("Exception when calling ProfileApi->update_user_name: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **update_user_name_request** | [**UpdateUserNameRequest**](UpdateUserNameRequest.md)|  | [optional] 

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
**200** | Name updated successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

