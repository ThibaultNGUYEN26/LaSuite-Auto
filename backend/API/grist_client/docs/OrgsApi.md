# grist_client.OrgsApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**delete_org**](OrgsApi.md#delete_org) | **DELETE** /orgs/{orgId}/{name} | Delete an org
[**describe_org**](OrgsApi.md#describe_org) | **GET** /orgs/{orgId} | Describe an org
[**get_org_usage**](OrgsApi.md#get_org_usage) | **GET** /orgs/{orgId}/usage | Get organization usage summary
[**list_org_access**](OrgsApi.md#list_org_access) | **GET** /orgs/{orgId}/access | List users with access to org
[**list_orgs**](OrgsApi.md#list_orgs) | **GET** /orgs | List the orgs you have access to
[**modify_org**](OrgsApi.md#modify_org) | **PATCH** /orgs/{orgId} | Modify an org
[**modify_org_access**](OrgsApi.md#modify_org_access) | **PATCH** /orgs/{orgId}/access | Change who has access to org


# **delete_org**
> delete_org(org_id, name)

Delete an org

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
    api_instance = grist_client.OrgsApi(api_client)
    org_id = grist_client.DescribeOrgOrgIdParameter() # DescribeOrgOrgIdParameter | This can be an integer id, or a string subdomain (e.g. `gristlabs`), or `current` if the org is implied by the domain in the url
    name = 'name_example' # str | The organization name

    try:
        # Delete an org
        api_instance.delete_org(org_id, name)
    except Exception as e:
        print("Exception when calling OrgsApi->delete_org: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | [**DescribeOrgOrgIdParameter**](.md)| This can be an integer id, or a string subdomain (e.g. &#x60;gristlabs&#x60;), or &#x60;current&#x60; if the org is implied by the domain in the url | 
 **name** | **str**| The organization name | 

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
**403** | Access denied |  -  |
**404** | Not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **describe_org**
> Org describe_org(org_id)

Describe an org

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.org import Org
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
    api_instance = grist_client.OrgsApi(api_client)
    org_id = grist_client.DescribeOrgOrgIdParameter() # DescribeOrgOrgIdParameter | This can be an integer id, or a string subdomain (e.g. `gristlabs`), or `current` if the org is implied by the domain in the url

    try:
        # Describe an org
        api_response = api_instance.describe_org(org_id)
        print("The response of OrgsApi->describe_org:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrgsApi->describe_org: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | [**DescribeOrgOrgIdParameter**](.md)| This can be an integer id, or a string subdomain (e.g. &#x60;gristlabs&#x60;), or &#x60;current&#x60; if the org is implied by the domain in the url | 

### Return type

[**Org**](Org.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | An organization |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_org_usage**
> GetOrgUsage200Response get_org_usage(org_id)

Get organization usage summary

Get usage statistics for all non-deleted documents in the organization.
Only accessible to organization owners.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.get_org_usage200_response import GetOrgUsage200Response
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
    api_instance = grist_client.OrgsApi(api_client)
    org_id = grist_client.DescribeOrgOrgIdParameter() # DescribeOrgOrgIdParameter | This can be an integer id, or a string subdomain (e.g. `gristlabs`), or `current` if the org is implied by the domain in the url

    try:
        # Get organization usage summary
        api_response = api_instance.get_org_usage(org_id)
        print("The response of OrgsApi->get_org_usage:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrgsApi->get_org_usage: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | [**DescribeOrgOrgIdParameter**](.md)| This can be an integer id, or a string subdomain (e.g. &#x60;gristlabs&#x60;), or &#x60;current&#x60; if the org is implied by the domain in the url | 

### Return type

[**GetOrgUsage200Response**](GetOrgUsage200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Usage summary |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_org_access**
> OrgAccessRead list_org_access(org_id)

List users with access to org

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.org_access_read import OrgAccessRead
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
    api_instance = grist_client.OrgsApi(api_client)
    org_id = grist_client.DescribeOrgOrgIdParameter() # DescribeOrgOrgIdParameter | This can be an integer id, or a string subdomain (e.g. `gristlabs`), or `current` if the org is implied by the domain in the url

    try:
        # List users with access to org
        api_response = api_instance.list_org_access(org_id)
        print("The response of OrgsApi->list_org_access:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrgsApi->list_org_access: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | [**DescribeOrgOrgIdParameter**](.md)| This can be an integer id, or a string subdomain (e.g. &#x60;gristlabs&#x60;), or &#x60;current&#x60; if the org is implied by the domain in the url | 

### Return type

[**OrgAccessRead**](OrgAccessRead.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Users with access to org |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_orgs**
> List[Org] list_orgs()

List the orgs you have access to

This enumerates all the team sites or personal areas available.

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.org import Org
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
    api_instance = grist_client.OrgsApi(api_client)

    try:
        # List the orgs you have access to
        api_response = api_instance.list_orgs()
        print("The response of OrgsApi->list_orgs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrgsApi->list_orgs: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[Org]**](Org.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | An array of organizations |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_org**
> modify_org(org_id, org_parameters)

Modify an org

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.org_parameters import OrgParameters
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
    api_instance = grist_client.OrgsApi(api_client)
    org_id = grist_client.DescribeOrgOrgIdParameter() # DescribeOrgOrgIdParameter | This can be an integer id, or a string subdomain (e.g. `gristlabs`), or `current` if the org is implied by the domain in the url
    org_parameters = grist_client.OrgParameters() # OrgParameters | the changes to make

    try:
        # Modify an org
        api_instance.modify_org(org_id, org_parameters)
    except Exception as e:
        print("Exception when calling OrgsApi->modify_org: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | [**DescribeOrgOrgIdParameter**](.md)| This can be an integer id, or a string subdomain (e.g. &#x60;gristlabs&#x60;), or &#x60;current&#x60; if the org is implied by the domain in the url | 
 **org_parameters** | [**OrgParameters**](OrgParameters.md)| the changes to make | 

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

# **modify_org_access**
> modify_org_access(org_id, modify_org_access_request)

Change who has access to org

### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.modify_org_access_request import ModifyOrgAccessRequest
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
    api_instance = grist_client.OrgsApi(api_client)
    org_id = grist_client.DescribeOrgOrgIdParameter() # DescribeOrgOrgIdParameter | This can be an integer id, or a string subdomain (e.g. `gristlabs`), or `current` if the org is implied by the domain in the url
    modify_org_access_request = grist_client.ModifyOrgAccessRequest() # ModifyOrgAccessRequest | the changes to make

    try:
        # Change who has access to org
        api_instance.modify_org_access(org_id, modify_org_access_request)
    except Exception as e:
        print("Exception when calling OrgsApi->modify_org_access: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **org_id** | [**DescribeOrgOrgIdParameter**](.md)| This can be an integer id, or a string subdomain (e.g. &#x60;gristlabs&#x60;), or &#x60;current&#x60; if the org is implied by the domain in the url | 
 **modify_org_access_request** | [**ModifyOrgAccessRequest**](ModifyOrgAccessRequest.md)| the changes to make | 

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

