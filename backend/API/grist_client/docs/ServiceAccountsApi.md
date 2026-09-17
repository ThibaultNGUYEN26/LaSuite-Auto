# grist_client.ServiceAccountsApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_service_account**](ServiceAccountsApi.md#create_service_account) | **POST** /service-accounts | Create a service account
[**delete_service_account**](ServiceAccountsApi.md#delete_service_account) | **DELETE** /service-accounts/{saId} | Delete a service account
[**delete_service_account_api_key**](ServiceAccountsApi.md#delete_service_account_api_key) | **DELETE** /service-accounts/{saId}/apikey | Delete a service account&#39;s api key
[**get_service_account**](ServiceAccountsApi.md#get_service_account) | **GET** /service-accounts/{saId} | Get a service account&#39;s details
[**list_service_accounts**](ServiceAccountsApi.md#list_service_accounts) | **GET** /service-accounts | Get all your service accounts
[**modify_service_account**](ServiceAccountsApi.md#modify_service_account) | **PATCH** /service-accounts/{saId} | Modify a service account
[**regenerate_service_account_api_key**](ServiceAccountsApi.md#regenerate_service_account_api_key) | **POST** /service-accounts/{saId}/apikey | Generate a new service account&#39;s api key


# **create_service_account**
> ServiceAccountResultWithApiKey create_service_account(create_service_account=create_service_account)

Create a service account

This creates a new service account with a new API key.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.create_service_account import CreateServiceAccount
from grist_client.models.service_account_result_with_api_key import ServiceAccountResultWithApiKey
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
    api_instance = grist_client.ServiceAccountsApi(api_client)
    create_service_account = grist_client.CreateServiceAccount() # CreateServiceAccount |  (optional)

    try:
        # Create a service account
        api_response = api_instance.create_service_account(create_service_account=create_service_account)
        print("The response of ServiceAccountsApi->create_service_account:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceAccountsApi->create_service_account: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_service_account** | [**CreateServiceAccount**](CreateServiceAccount.md)|  | [optional] 

### Return type

[**ServiceAccountResultWithApiKey**](ServiceAccountResultWithApiKey.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The service account created |  -  |
**403** | The caller is not allowed to create service accounts |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_service_account**
> delete_service_account(sa_id)

Delete a service account

This deletes a given service account.


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
    api_instance = grist_client.ServiceAccountsApi(api_client)
    sa_id = 56 # int | A service account id

    try:
        # Delete a service account
        api_instance.delete_service_account(sa_id)
    except Exception as e:
        print("Exception when calling ServiceAccountsApi->delete_service_account: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sa_id** | **int**| A service account id | 

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
**200** | Service account deleted successfully. Returns empty body. |  -  |
**403** | The caller is not allowed to delete this service account |  -  |
**404** | Service account not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_service_account_api_key**
> delete_service_account_api_key(sa_id)

Delete a service account's api key

Deletes the API key for a service account. The service account will
no longer be able to authenticate until a new key is generated.


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
    api_instance = grist_client.ServiceAccountsApi(api_client)
    sa_id = 56 # int | A service account id

    try:
        # Delete a service account's api key
        api_instance.delete_service_account_api_key(sa_id)
    except Exception as e:
        print("Exception when calling ServiceAccountsApi->delete_service_account_api_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sa_id** | **int**| A service account id | 

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
**200** | API key deleted successfully. Returns empty body. |  -  |
**403** | The caller is not allowed to delete this api key |  -  |
**404** | Service account not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_service_account**
> ServiceAccountResult get_service_account(sa_id)

Get a service account's details

This reports the details of a service account.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.service_account_result import ServiceAccountResult
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
    api_instance = grist_client.ServiceAccountsApi(api_client)
    sa_id = 56 # int | A service account id

    try:
        # Get a service account's details
        api_response = api_instance.get_service_account(sa_id)
        print("The response of ServiceAccountsApi->get_service_account:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceAccountsApi->get_service_account: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sa_id** | **int**| A service account id | 

### Return type

[**ServiceAccountResult**](ServiceAccountResult.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Details of the service account |  -  |
**403** | Access denied |  -  |
**404** | Service account not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_service_accounts**
> List[ServiceAccountResult] list_service_accounts()

Get all your service accounts

This lists all your service accounts with their details.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.service_account_result import ServiceAccountResult
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
    api_instance = grist_client.ServiceAccountsApi(api_client)

    try:
        # Get all your service accounts
        api_response = api_instance.list_service_accounts()
        print("The response of ServiceAccountsApi->list_service_accounts:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceAccountsApi->list_service_accounts: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[ServiceAccountResult]**](ServiceAccountResult.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Array of your service accounts |  -  |
**403** | The caller is not allowed to access this resource |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_service_account**
> modify_service_account(sa_id, service_account_body=service_account_body)

Modify a service account

This updates a service account's label, description or expiration date.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.service_account_body import ServiceAccountBody
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
    api_instance = grist_client.ServiceAccountsApi(api_client)
    sa_id = 56 # int | A service account id
    service_account_body = grist_client.ServiceAccountBody() # ServiceAccountBody |  (optional)

    try:
        # Modify a service account
        api_instance.modify_service_account(sa_id, service_account_body=service_account_body)
    except Exception as e:
        print("Exception when calling ServiceAccountsApi->modify_service_account: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sa_id** | **int**| A service account id | 
 **service_account_body** | [**ServiceAccountBody**](ServiceAccountBody.md)|  | [optional] 

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
**200** | Success (empty body) |  -  |
**403** | The caller is not allowed to modify this service account |  -  |
**404** | Service account not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **regenerate_service_account_api_key**
> ServiceAccountResultWithApiKey regenerate_service_account_api_key(sa_id)

Generate a new service account's api key

This renews an api key of a given service account.
Useful especially to change the API key when it has been leaked.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.service_account_result_with_api_key import ServiceAccountResultWithApiKey
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
    api_instance = grist_client.ServiceAccountsApi(api_client)
    sa_id = 56 # int | A service account id

    try:
        # Generate a new service account's api key
        api_response = api_instance.regenerate_service_account_api_key(sa_id)
        print("The response of ServiceAccountsApi->regenerate_service_account_api_key:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ServiceAccountsApi->regenerate_service_account_api_key: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **sa_id** | **int**| A service account id | 

### Return type

[**ServiceAccountResultWithApiKey**](ServiceAccountResultWithApiKey.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The service account with the new API key |  -  |
**403** | The caller is not allowed to regenerate this api key |  -  |
**404** | Service account not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

