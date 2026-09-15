# openapi_client.ApiApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_v1_0_config_retrieve**](ApiApi.md#api_v1_0_config_retrieve) | **GET** /api/v1.0/config/ | 
[**api_v1_0_entitlements_retrieve**](ApiApi.md#api_v1_0_entitlements_retrieve) | **GET** /api/v1.0/entitlements/ | 
[**api_v1_0_items_accesses_create**](ApiApi.md#api_v1_0_items_accesses_create) | **POST** /api/v1.0/items/{resource_id}/accesses/ | 
[**api_v1_0_items_accesses_destroy**](ApiApi.md#api_v1_0_items_accesses_destroy) | **DELETE** /api/v1.0/items/{resource_id}/accesses/{id}/ | 
[**api_v1_0_items_accesses_list**](ApiApi.md#api_v1_0_items_accesses_list) | **GET** /api/v1.0/items/{resource_id}/accesses/ | 
[**api_v1_0_items_accesses_partial_update**](ApiApi.md#api_v1_0_items_accesses_partial_update) | **PATCH** /api/v1.0/items/{resource_id}/accesses/{id}/ | 
[**api_v1_0_items_accesses_retrieve**](ApiApi.md#api_v1_0_items_accesses_retrieve) | **GET** /api/v1.0/items/{resource_id}/accesses/{id}/ | 
[**api_v1_0_items_accesses_update**](ApiApi.md#api_v1_0_items_accesses_update) | **PUT** /api/v1.0/items/{resource_id}/accesses/{id}/ | 
[**api_v1_0_items_batch_share_create**](ApiApi.md#api_v1_0_items_batch_share_create) | **POST** /api/v1.0/items/{id}/batch-share/ | 
[**api_v1_0_items_breadcrumb_retrieve**](ApiApi.md#api_v1_0_items_breadcrumb_retrieve) | **GET** /api/v1.0/items/{id}/breadcrumb/ | 
[**api_v1_0_items_children_create**](ApiApi.md#api_v1_0_items_children_create) | **POST** /api/v1.0/items/{id}/children/ | 
[**api_v1_0_items_children_retrieve**](ApiApi.md#api_v1_0_items_children_retrieve) | **GET** /api/v1.0/items/{id}/children/ | 
[**api_v1_0_items_convert_create**](ApiApi.md#api_v1_0_items_convert_create) | **POST** /api/v1.0/items/{id}/convert/ | 
[**api_v1_0_items_create**](ApiApi.md#api_v1_0_items_create) | **POST** /api/v1.0/items/ | 
[**api_v1_0_items_destroy**](ApiApi.md#api_v1_0_items_destroy) | **DELETE** /api/v1.0/items/{id}/ | 
[**api_v1_0_items_download_retrieve**](ApiApi.md#api_v1_0_items_download_retrieve) | **GET** /api/v1.0/items/{id}/download/ | 
[**api_v1_0_items_duplicate_create**](ApiApi.md#api_v1_0_items_duplicate_create) | **POST** /api/v1.0/items/{id}/duplicate/ | 
[**api_v1_0_items_export_retrieve**](ApiApi.md#api_v1_0_items_export_retrieve) | **GET** /api/v1.0/items/{id}/export/ | 
[**api_v1_0_items_favorite_create**](ApiApi.md#api_v1_0_items_favorite_create) | **POST** /api/v1.0/items/{id}/favorite/ | 
[**api_v1_0_items_favorite_destroy**](ApiApi.md#api_v1_0_items_favorite_destroy) | **DELETE** /api/v1.0/items/{id}/favorite/ | 
[**api_v1_0_items_favorites_retrieve**](ApiApi.md#api_v1_0_items_favorites_retrieve) | **GET** /api/v1.0/items/favorites/ | 
[**api_v1_0_items_hard_delete_destroy**](ApiApi.md#api_v1_0_items_hard_delete_destroy) | **DELETE** /api/v1.0/items/{id}/hard-delete/ | 
[**api_v1_0_items_invitations_create**](ApiApi.md#api_v1_0_items_invitations_create) | **POST** /api/v1.0/items/{resource_id}/invitations/ | 
[**api_v1_0_items_invitations_destroy**](ApiApi.md#api_v1_0_items_invitations_destroy) | **DELETE** /api/v1.0/items/{resource_id}/invitations/{id}/ | 
[**api_v1_0_items_invitations_list**](ApiApi.md#api_v1_0_items_invitations_list) | **GET** /api/v1.0/items/{resource_id}/invitations/ | 
[**api_v1_0_items_invitations_partial_update**](ApiApi.md#api_v1_0_items_invitations_partial_update) | **PATCH** /api/v1.0/items/{resource_id}/invitations/{id}/ | 
[**api_v1_0_items_invitations_retrieve**](ApiApi.md#api_v1_0_items_invitations_retrieve) | **GET** /api/v1.0/items/{resource_id}/invitations/{id}/ | 
[**api_v1_0_items_invitations_update**](ApiApi.md#api_v1_0_items_invitations_update) | **PUT** /api/v1.0/items/{resource_id}/invitations/{id}/ | 
[**api_v1_0_items_link_configuration_update**](ApiApi.md#api_v1_0_items_link_configuration_update) | **PUT** /api/v1.0/items/{id}/link-configuration/ | 
[**api_v1_0_items_list**](ApiApi.md#api_v1_0_items_list) | **GET** /api/v1.0/items/ | 
[**api_v1_0_items_media_auth_retrieve**](ApiApi.md#api_v1_0_items_media_auth_retrieve) | **GET** /api/v1.0/items/media-auth/ | 
[**api_v1_0_items_move_create**](ApiApi.md#api_v1_0_items_move_create) | **POST** /api/v1.0/items/{id}/move/ | 
[**api_v1_0_items_partial_update**](ApiApi.md#api_v1_0_items_partial_update) | **PATCH** /api/v1.0/items/{id}/ | 
[**api_v1_0_items_recents_retrieve**](ApiApi.md#api_v1_0_items_recents_retrieve) | **GET** /api/v1.0/items/recents/ | 
[**api_v1_0_items_restore_create**](ApiApi.md#api_v1_0_items_restore_create) | **POST** /api/v1.0/items/{id}/restore/ | 
[**api_v1_0_items_restrict_create**](ApiApi.md#api_v1_0_items_restrict_create) | **POST** /api/v1.0/items/{id}/restrict/ | 
[**api_v1_0_items_restrict_destroy**](ApiApi.md#api_v1_0_items_restrict_destroy) | **DELETE** /api/v1.0/items/{id}/restrict/ | 
[**api_v1_0_items_retrieve**](ApiApi.md#api_v1_0_items_retrieve) | **GET** /api/v1.0/items/{id}/ | 
[**api_v1_0_items_search_retrieve**](ApiApi.md#api_v1_0_items_search_retrieve) | **GET** /api/v1.0/items/search/ | 
[**api_v1_0_items_trashbin_retrieve**](ApiApi.md#api_v1_0_items_trashbin_retrieve) | **GET** /api/v1.0/items/trashbin/ | 
[**api_v1_0_items_tree_retrieve**](ApiApi.md#api_v1_0_items_tree_retrieve) | **GET** /api/v1.0/items/{id}/tree/ | 
[**api_v1_0_items_update**](ApiApi.md#api_v1_0_items_update) | **PUT** /api/v1.0/items/{id}/ | 
[**api_v1_0_items_upload_ended_create**](ApiApi.md#api_v1_0_items_upload_ended_create) | **POST** /api/v1.0/items/{id}/upload-ended/ | 
[**api_v1_0_items_wopi_retrieve**](ApiApi.md#api_v1_0_items_wopi_retrieve) | **GET** /api/v1.0/items/{id}/wopi/ | 
[**api_v1_0_sdk_relay_events_create**](ApiApi.md#api_v1_0_sdk_relay_events_create) | **POST** /api/v1.0/sdk-relay/events/ | 
[**api_v1_0_sdk_relay_events_retrieve**](ApiApi.md#api_v1_0_sdk_relay_events_retrieve) | **GET** /api/v1.0/sdk-relay/events/{id}/ | 
[**api_v1_0_user_reconciliations_retrieve**](ApiApi.md#api_v1_0_user_reconciliations_retrieve) | **GET** /api/v1.0/user-reconciliations/{user_type}/{confirmation_id}/ | 
[**api_v1_0_users_contacts_retrieve**](ApiApi.md#api_v1_0_users_contacts_retrieve) | **GET** /api/v1.0/users/contacts/ | 
[**api_v1_0_users_list**](ApiApi.md#api_v1_0_users_list) | **GET** /api/v1.0/users/ | 
[**api_v1_0_users_me_retrieve**](ApiApi.md#api_v1_0_users_me_retrieve) | **GET** /api/v1.0/users/me/ | 
[**api_v1_0_users_partial_update**](ApiApi.md#api_v1_0_users_partial_update) | **PATCH** /api/v1.0/users/{id}/ | 
[**api_v1_0_users_update**](ApiApi.md#api_v1_0_users_update) | **PUT** /api/v1.0/users/{id}/ | 


# **api_v1_0_config_retrieve**
> api_v1_0_config_retrieve()

GET /api/v1.0/config/
    Return a dictionary of public settings.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)

    try:
        api_instance.api_v1_0_config_retrieve()
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_config_retrieve: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_entitlements_retrieve**
> api_v1_0_entitlements_retrieve()

GET /api/v1.0/entitlements/

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)

    try:
        api_instance.api_v1_0_entitlements_retrieve()
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_entitlements_retrieve: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_accesses_create**
> ItemAccess api_v1_0_items_accesses_create(resource_id, item_access_request=item_access_request)

API ViewSet for all interactions with item accesses.

GET /api/v1.0/items/<resource_id>/accesses/:<item_access_id>
    Return list of all item accesses related to the logged-in user or one
    item access if an id is provided.

POST /api/v1.0/items/<resource_id>/accesses/ with expected data:
    - user: str
    - role: str [administrator|editor|reader]
    Return newly created item access

PUT /api/v1.0/items/<resource_id>/accesses/<item_access_id>/ with expected data:
    - role: str [owner|admin|editor|reader]
    Return updated item access

PATCH /api/v1.0/items/<resource_id>/accesses/<item_access_id>/ with expected data:
    - role: str [owner|admin|editor|reader]
    Return partially updated item access

DELETE /api/v1.0/items/<resource_id>/accesses/<item_access_id>/
    Delete targeted item access

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item_access import ItemAccess
from openapi_client.models.item_access_request import ItemAccessRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    resource_id = 'resource_id_example' # str | 
    item_access_request = openapi_client.ItemAccessRequest() # ItemAccessRequest |  (optional)

    try:
        api_response = api_instance.api_v1_0_items_accesses_create(resource_id, item_access_request=item_access_request)
        print("The response of ApiApi->api_v1_0_items_accesses_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_accesses_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **str**|  | 
 **item_access_request** | [**ItemAccessRequest**](ItemAccessRequest.md)|  | [optional] 

### Return type

[**ItemAccess**](ItemAccess.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_accesses_destroy**
> api_v1_0_items_accesses_destroy(id, resource_id)

API ViewSet for all interactions with item accesses.

GET /api/v1.0/items/<resource_id>/accesses/:<item_access_id>
    Return list of all item accesses related to the logged-in user or one
    item access if an id is provided.

POST /api/v1.0/items/<resource_id>/accesses/ with expected data:
    - user: str
    - role: str [administrator|editor|reader]
    Return newly created item access

PUT /api/v1.0/items/<resource_id>/accesses/<item_access_id>/ with expected data:
    - role: str [owner|admin|editor|reader]
    Return updated item access

PATCH /api/v1.0/items/<resource_id>/accesses/<item_access_id>/ with expected data:
    - role: str [owner|admin|editor|reader]
    Return partially updated item access

DELETE /api/v1.0/items/<resource_id>/accesses/<item_access_id>/
    Delete targeted item access

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    resource_id = 'resource_id_example' # str | 

    try:
        api_instance.api_v1_0_items_accesses_destroy(id, resource_id)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_accesses_destroy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **resource_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_accesses_list**
> List[ItemAccess] api_v1_0_items_accesses_list(resource_id)

List item accesses for an item and its ancestors.

Returns the deepest access per target (user/team) with computed max_ancestors_role.
For inherited accesses (not on current item), max_ancestors_role equals the access's role.

Non-privileged users only see privileged roles to prevent information leakage.
Results are ordered by item depth and creation date.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item_access import ItemAccess
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    resource_id = 'resource_id_example' # str | 

    try:
        api_response = api_instance.api_v1_0_items_accesses_list(resource_id)
        print("The response of ApiApi->api_v1_0_items_accesses_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_accesses_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **str**|  | 

### Return type

[**List[ItemAccess]**](ItemAccess.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_accesses_partial_update**
> ItemAccess api_v1_0_items_accesses_partial_update(id, resource_id, patched_item_access_request=patched_item_access_request)

Partial update the item access.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item_access import ItemAccess
from openapi_client.models.patched_item_access_request import PatchedItemAccessRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    resource_id = 'resource_id_example' # str | 
    patched_item_access_request = openapi_client.PatchedItemAccessRequest() # PatchedItemAccessRequest |  (optional)

    try:
        api_response = api_instance.api_v1_0_items_accesses_partial_update(id, resource_id, patched_item_access_request=patched_item_access_request)
        print("The response of ApiApi->api_v1_0_items_accesses_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_accesses_partial_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **resource_id** | **str**|  | 
 **patched_item_access_request** | [**PatchedItemAccessRequest**](PatchedItemAccessRequest.md)|  | [optional] 

### Return type

[**ItemAccess**](ItemAccess.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_accesses_retrieve**
> ItemAccess api_v1_0_items_accesses_retrieve(id, resource_id)

API ViewSet for all interactions with item accesses.

GET /api/v1.0/items/<resource_id>/accesses/:<item_access_id>
    Return list of all item accesses related to the logged-in user or one
    item access if an id is provided.

POST /api/v1.0/items/<resource_id>/accesses/ with expected data:
    - user: str
    - role: str [administrator|editor|reader]
    Return newly created item access

PUT /api/v1.0/items/<resource_id>/accesses/<item_access_id>/ with expected data:
    - role: str [owner|admin|editor|reader]
    Return updated item access

PATCH /api/v1.0/items/<resource_id>/accesses/<item_access_id>/ with expected data:
    - role: str [owner|admin|editor|reader]
    Return partially updated item access

DELETE /api/v1.0/items/<resource_id>/accesses/<item_access_id>/
    Delete targeted item access

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item_access import ItemAccess
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    resource_id = 'resource_id_example' # str | 

    try:
        api_response = api_instance.api_v1_0_items_accesses_retrieve(id, resource_id)
        print("The response of ApiApi->api_v1_0_items_accesses_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_accesses_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **resource_id** | **str**|  | 

### Return type

[**ItemAccess**](ItemAccess.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_accesses_update**
> ItemAccess api_v1_0_items_accesses_update(id, resource_id, item_access_request=item_access_request)

We not use the update mixin to apply a specific behavior we can't implement using
perform_update method.

If the role is updated and is the same role as the max ancestors role,
we don't want to have two consecutive explicit accesses with the same role.
We have to delete the current access, this item will have an inherited access
with the correct role.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item_access import ItemAccess
from openapi_client.models.item_access_request import ItemAccessRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    resource_id = 'resource_id_example' # str | 
    item_access_request = openapi_client.ItemAccessRequest() # ItemAccessRequest |  (optional)

    try:
        api_response = api_instance.api_v1_0_items_accesses_update(id, resource_id, item_access_request=item_access_request)
        print("The response of ApiApi->api_v1_0_items_accesses_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_accesses_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **resource_id** | **str**|  | 
 **item_access_request** | [**ItemAccessRequest**](ItemAccessRequest.md)|  | [optional] 

### Return type

[**ItemAccess**](ItemAccess.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_batch_share_create**
> BatchShareResponse api_v1_0_items_batch_share_create(id, batch_share_request)

Share an item with a list of contacts in a single request.

Emails matching an existing user get an access, unknown emails get an
invitation. All rows are validated before any database write so a
rejected batch never creates a partial share state.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.batch_share_request import BatchShareRequest
from openapi_client.models.batch_share_response import BatchShareResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    batch_share_request = openapi_client.BatchShareRequest() # BatchShareRequest | 

    try:
        api_response = api_instance.api_v1_0_items_batch_share_create(id, batch_share_request)
        print("The response of ApiApi->api_v1_0_items_batch_share_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_batch_share_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **batch_share_request** | [**BatchShareRequest**](BatchShareRequest.md)|  | 

### Return type

[**BatchShareResponse**](BatchShareResponse.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_breadcrumb_retrieve**
> BreadcrumbItem api_v1_0_items_breadcrumb_retrieve(id)

List the breadcrumb for an item

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.breadcrumb_item import BreadcrumbItem
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        api_response = api_instance.api_v1_0_items_breadcrumb_retrieve(id)
        print("The response of ApiApi->api_v1_0_items_breadcrumb_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_breadcrumb_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

[**BreadcrumbItem**](BreadcrumbItem.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_children_create**
> ListItem api_v1_0_items_children_create(id, list_item_request)

Handle listing and creating children of a item

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.list_item import ListItem
from openapi_client.models.list_item_request import ListItemRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    list_item_request = openapi_client.ListItemRequest() # ListItemRequest | 

    try:
        api_response = api_instance.api_v1_0_items_children_create(id, list_item_request)
        print("The response of ApiApi->api_v1_0_items_children_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_children_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **list_item_request** | [**ListItemRequest**](ListItemRequest.md)|  | 

### Return type

[**ListItem**](ListItem.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_children_retrieve**
> ListItem api_v1_0_items_children_retrieve(id)

Handle listing and creating children of a item

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.list_item import ListItem
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        api_response = api_instance.api_v1_0_items_children_retrieve(id)
        print("The response of ApiApi->api_v1_0_items_children_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_children_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

[**ListItem**](ListItem.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_convert_create**
> Item api_v1_0_items_convert_create(id, item_request)

Queue a legacy Office file conversion.

Creates a placeholder Item in CONVERTING state in the destination folder
and dispatches the celery task that will attach the converted bytes.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.models.item_request import ItemRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    item_request = openapi_client.ItemRequest() # ItemRequest | 

    try:
        api_response = api_instance.api_v1_0_items_convert_create(id, item_request)
        print("The response of ApiApi->api_v1_0_items_convert_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_convert_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **item_request** | [**ItemRequest**](ItemRequest.md)|  | 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_create**
> CreateItem api_v1_0_items_create(create_item_request=create_item_request)

ItemViewSet API.

This view set provides CRUD operations and additional actions for managing items.
Supports filtering, ordering, and annotations for enhanced querying capabilities.

### API Endpoints:
1. **List**: Retrieve a paginated list of items.
   Example: GET /items/?page=2
2. **Retrieve**: Get a specific item by its ID.
   Example: GET /items/{id}/
3. **Create**: Create a new item.
   Example: POST /items/
4. **Update**: Update a item by its ID.
   Example: PUT /items/{id}/
5. **Delete**: Soft delete a item by its ID.
   Example: DELETE /items/{id}/

### Additional Actions:
1. **Trashbin**: List soft deleted items for an items owner
    Example: GET /items/trashbin/

2. **Children**: List or create child items.
    Example: GET, POST /items/{id}/children/

3. **Favorite**: Get list of favorite items for a user. Mark or unmark
    a item as favorite.
    Examples:
    - GET /items/favorites/
    - POST, DELETE /items/{id}/favorite/

4. **Link Configuration**: Update item link configuration.
    Example: PUT /items/{id}/link-configuration/

5. **Media Auth**: Authorize access to item media.
    Example: GET /items/media-auth/

6. **Duplicate**: Duplicate an item of type file.
    Example:

### Ordering: created_at, updated_at, is_favorite, title

    Example:
    - Ascending: GET /api/v1.0/items/?ordering=created_at
    - Desceding: GET /api/v1.0/items/?ordering=-title

### Filtering:
    - `is_creator_me=true`: Returns items created by the current user.
    - `is_creator_me=false`: Returns items created by other users.
    - `is_favorite=true`: Returns items marked as favorite by the current user
    - `is_favorite=false`: Returns items not marked as favorite by the current user
    - `title=hello`: Returns items which title contains the "hello" string

    Example:
    - GET /api/v1.0/items/?is_creator_me=true&is_favorite=true
    - GET /api/v1.0/items/?is_creator_me=false&title=hello

### Annotations:
1. **is_favorite**: Indicates whether the item is marked as favorite by the current user.
2. *`*user_roles**: Roles the current user has on the item or its ancestors.

### Notes:
- Only the highest ancestor in a item hierarchy is shown in list views.
- Implements soft delete logic to retain item tree structures.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.create_item import CreateItem
from openapi_client.models.create_item_request import CreateItemRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    create_item_request = openapi_client.CreateItemRequest() # CreateItemRequest |  (optional)

    try:
        api_response = api_instance.api_v1_0_items_create(create_item_request=create_item_request)
        print("The response of ApiApi->api_v1_0_items_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **create_item_request** | [**CreateItemRequest**](CreateItemRequest.md)|  | [optional] 

### Return type

[**CreateItem**](CreateItem.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_destroy**
> api_v1_0_items_destroy(id)

ItemViewSet API.

This view set provides CRUD operations and additional actions for managing items.
Supports filtering, ordering, and annotations for enhanced querying capabilities.

### API Endpoints:
1. **List**: Retrieve a paginated list of items.
   Example: GET /items/?page=2
2. **Retrieve**: Get a specific item by its ID.
   Example: GET /items/{id}/
3. **Create**: Create a new item.
   Example: POST /items/
4. **Update**: Update a item by its ID.
   Example: PUT /items/{id}/
5. **Delete**: Soft delete a item by its ID.
   Example: DELETE /items/{id}/

### Additional Actions:
1. **Trashbin**: List soft deleted items for an items owner
    Example: GET /items/trashbin/

2. **Children**: List or create child items.
    Example: GET, POST /items/{id}/children/

3. **Favorite**: Get list of favorite items for a user. Mark or unmark
    a item as favorite.
    Examples:
    - GET /items/favorites/
    - POST, DELETE /items/{id}/favorite/

4. **Link Configuration**: Update item link configuration.
    Example: PUT /items/{id}/link-configuration/

5. **Media Auth**: Authorize access to item media.
    Example: GET /items/media-auth/

6. **Duplicate**: Duplicate an item of type file.
    Example:

### Ordering: created_at, updated_at, is_favorite, title

    Example:
    - Ascending: GET /api/v1.0/items/?ordering=created_at
    - Desceding: GET /api/v1.0/items/?ordering=-title

### Filtering:
    - `is_creator_me=true`: Returns items created by the current user.
    - `is_creator_me=false`: Returns items created by other users.
    - `is_favorite=true`: Returns items marked as favorite by the current user
    - `is_favorite=false`: Returns items not marked as favorite by the current user
    - `title=hello`: Returns items which title contains the "hello" string

    Example:
    - GET /api/v1.0/items/?is_creator_me=true&is_favorite=true
    - GET /api/v1.0/items/?is_creator_me=false&title=hello

### Annotations:
1. **is_favorite**: Indicates whether the item is marked as favorite by the current user.
2. *`*user_roles**: Roles the current user has on the item or its ancestors.

### Notes:
- Only the highest ancestor in a item hierarchy is shown in list views.
- Implements soft delete logic to retain item tree structures.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        api_instance.api_v1_0_items_destroy(id)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_destroy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_download_retrieve**
> Item api_v1_0_items_download_retrieve(id)

Permalink endpoint for downloading an item's file.

Returns a redirect to the current media URL for the item, so this link
remains valid even after the item is renamed. Authentication is still
enforced by the existing media-auth mechanism on the redirected URL.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        api_response = api_instance.api_v1_0_items_download_retrieve(id)
        print("The response of ApiApi->api_v1_0_items_download_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_download_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_duplicate_create**
> Item api_v1_0_items_duplicate_create(id, item_request)

Duplicate an item of type File. The item is duplicated in the folder where the original
item is.
The user who duplicates becomes the creator of the duplicate

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.models.item_request import ItemRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    item_request = openapi_client.ItemRequest() # ItemRequest | 

    try:
        api_response = api_instance.api_v1_0_items_duplicate_create(id, item_request)
        print("The response of ApiApi->api_v1_0_items_duplicate_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_duplicate_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **item_request** | [**ItemRequest**](ItemRequest.md)|  | 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_export_retrieve**
> Item api_v1_0_items_export_retrieve(id)

Stream a recursive ZIP archive of a folder's content.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        api_response = api_instance.api_v1_0_items_export_retrieve(id)
        print("The response of ApiApi->api_v1_0_items_export_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_export_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_favorite_create**
> Item api_v1_0_items_favorite_create(id, item_request)

Mark or unmark the item as a favorite for the logged-in user based on the HTTP method.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.models.item_request import ItemRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    item_request = openapi_client.ItemRequest() # ItemRequest | 

    try:
        api_response = api_instance.api_v1_0_items_favorite_create(id, item_request)
        print("The response of ApiApi->api_v1_0_items_favorite_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_favorite_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **item_request** | [**ItemRequest**](ItemRequest.md)|  | 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_favorite_destroy**
> api_v1_0_items_favorite_destroy(id)

Mark or unmark the item as a favorite for the logged-in user based on the HTTP method.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        api_instance.api_v1_0_items_favorite_destroy(id)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_favorite_destroy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_favorites_retrieve**
> ListItemLight api_v1_0_items_favorites_retrieve()

Get list of favorite items for the current user.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.list_item_light import ListItemLight
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)

    try:
        api_response = api_instance.api_v1_0_items_favorites_retrieve()
        print("The response of ApiApi->api_v1_0_items_favorites_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_favorites_retrieve: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListItemLight**](ListItemLight.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_hard_delete_destroy**
> api_v1_0_items_hard_delete_destroy(id)

Hard delete an item.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        api_instance.api_v1_0_items_hard_delete_destroy(id)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_hard_delete_destroy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_invitations_create**
> Invitation api_v1_0_items_invitations_create(resource_id, invitation_request)

API ViewSet for user invitations to item.

GET /api/v1.0/items/<item_id>/invitations/:<invitation_id>/
    Return list of invitations related to that item or one
    item access if an id is provided.

POST /api/v1.0/items/<item_id>/invitations/ with expected data:
    - email: str
    - role: str [administrator|editor|reader]
    Return newly created invitation (issuer and item are automatically set)

PATCH /api/v1.0/items/<item_id>/invitations/:<invitation_id>/ with expected data:
    - role: str [owner|admin|editor|reader]
    Return partially updated item invitation

DELETE  /api/v1.0/items/<item_id>/invitations/<invitation_id>/
    Delete targeted invitation

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.invitation import Invitation
from openapi_client.models.invitation_request import InvitationRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    resource_id = 'resource_id_example' # str | 
    invitation_request = openapi_client.InvitationRequest() # InvitationRequest | 

    try:
        api_response = api_instance.api_v1_0_items_invitations_create(resource_id, invitation_request)
        print("The response of ApiApi->api_v1_0_items_invitations_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_invitations_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **str**|  | 
 **invitation_request** | [**InvitationRequest**](InvitationRequest.md)|  | 

### Return type

[**Invitation**](Invitation.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_invitations_destroy**
> api_v1_0_items_invitations_destroy(id, resource_id)

API ViewSet for user invitations to item.

GET /api/v1.0/items/<item_id>/invitations/:<invitation_id>/
    Return list of invitations related to that item or one
    item access if an id is provided.

POST /api/v1.0/items/<item_id>/invitations/ with expected data:
    - email: str
    - role: str [administrator|editor|reader]
    Return newly created invitation (issuer and item are automatically set)

PATCH /api/v1.0/items/<item_id>/invitations/:<invitation_id>/ with expected data:
    - role: str [owner|admin|editor|reader]
    Return partially updated item invitation

DELETE  /api/v1.0/items/<item_id>/invitations/<invitation_id>/
    Delete targeted invitation

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    resource_id = 'resource_id_example' # str | 

    try:
        api_instance.api_v1_0_items_invitations_destroy(id, resource_id)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_invitations_destroy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **resource_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_invitations_list**
> PaginatedInvitationList api_v1_0_items_invitations_list(resource_id, page=page, page_size=page_size)

API ViewSet for user invitations to item.

GET /api/v1.0/items/<item_id>/invitations/:<invitation_id>/
    Return list of invitations related to that item or one
    item access if an id is provided.

POST /api/v1.0/items/<item_id>/invitations/ with expected data:
    - email: str
    - role: str [administrator|editor|reader]
    Return newly created invitation (issuer and item are automatically set)

PATCH /api/v1.0/items/<item_id>/invitations/:<invitation_id>/ with expected data:
    - role: str [owner|admin|editor|reader]
    Return partially updated item invitation

DELETE  /api/v1.0/items/<item_id>/invitations/<invitation_id>/
    Delete targeted invitation

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.paginated_invitation_list import PaginatedInvitationList
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    resource_id = 'resource_id_example' # str | 
    page = 56 # int | A page number within the paginated result set. (optional)
    page_size = 56 # int | Number of results to return per page. (optional)

    try:
        api_response = api_instance.api_v1_0_items_invitations_list(resource_id, page=page, page_size=page_size)
        print("The response of ApiApi->api_v1_0_items_invitations_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_invitations_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resource_id** | **str**|  | 
 **page** | **int**| A page number within the paginated result set. | [optional] 
 **page_size** | **int**| Number of results to return per page. | [optional] 

### Return type

[**PaginatedInvitationList**](PaginatedInvitationList.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_invitations_partial_update**
> Invitation api_v1_0_items_invitations_partial_update(id, resource_id, patched_invitation_request=patched_invitation_request)

API ViewSet for user invitations to item.

GET /api/v1.0/items/<item_id>/invitations/:<invitation_id>/
    Return list of invitations related to that item or one
    item access if an id is provided.

POST /api/v1.0/items/<item_id>/invitations/ with expected data:
    - email: str
    - role: str [administrator|editor|reader]
    Return newly created invitation (issuer and item are automatically set)

PATCH /api/v1.0/items/<item_id>/invitations/:<invitation_id>/ with expected data:
    - role: str [owner|admin|editor|reader]
    Return partially updated item invitation

DELETE  /api/v1.0/items/<item_id>/invitations/<invitation_id>/
    Delete targeted invitation

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.invitation import Invitation
from openapi_client.models.patched_invitation_request import PatchedInvitationRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    resource_id = 'resource_id_example' # str | 
    patched_invitation_request = openapi_client.PatchedInvitationRequest() # PatchedInvitationRequest |  (optional)

    try:
        api_response = api_instance.api_v1_0_items_invitations_partial_update(id, resource_id, patched_invitation_request=patched_invitation_request)
        print("The response of ApiApi->api_v1_0_items_invitations_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_invitations_partial_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **resource_id** | **str**|  | 
 **patched_invitation_request** | [**PatchedInvitationRequest**](PatchedInvitationRequest.md)|  | [optional] 

### Return type

[**Invitation**](Invitation.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_invitations_retrieve**
> Invitation api_v1_0_items_invitations_retrieve(id, resource_id)

API ViewSet for user invitations to item.

GET /api/v1.0/items/<item_id>/invitations/:<invitation_id>/
    Return list of invitations related to that item or one
    item access if an id is provided.

POST /api/v1.0/items/<item_id>/invitations/ with expected data:
    - email: str
    - role: str [administrator|editor|reader]
    Return newly created invitation (issuer and item are automatically set)

PATCH /api/v1.0/items/<item_id>/invitations/:<invitation_id>/ with expected data:
    - role: str [owner|admin|editor|reader]
    Return partially updated item invitation

DELETE  /api/v1.0/items/<item_id>/invitations/<invitation_id>/
    Delete targeted invitation

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.invitation import Invitation
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    resource_id = 'resource_id_example' # str | 

    try:
        api_response = api_instance.api_v1_0_items_invitations_retrieve(id, resource_id)
        print("The response of ApiApi->api_v1_0_items_invitations_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_invitations_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **resource_id** | **str**|  | 

### Return type

[**Invitation**](Invitation.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_invitations_update**
> Invitation api_v1_0_items_invitations_update(id, resource_id, invitation_request)

API ViewSet for user invitations to item.

GET /api/v1.0/items/<item_id>/invitations/:<invitation_id>/
    Return list of invitations related to that item or one
    item access if an id is provided.

POST /api/v1.0/items/<item_id>/invitations/ with expected data:
    - email: str
    - role: str [administrator|editor|reader]
    Return newly created invitation (issuer and item are automatically set)

PATCH /api/v1.0/items/<item_id>/invitations/:<invitation_id>/ with expected data:
    - role: str [owner|admin|editor|reader]
    Return partially updated item invitation

DELETE  /api/v1.0/items/<item_id>/invitations/<invitation_id>/
    Delete targeted invitation

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.invitation import Invitation
from openapi_client.models.invitation_request import InvitationRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    resource_id = 'resource_id_example' # str | 
    invitation_request = openapi_client.InvitationRequest() # InvitationRequest | 

    try:
        api_response = api_instance.api_v1_0_items_invitations_update(id, resource_id, invitation_request)
        print("The response of ApiApi->api_v1_0_items_invitations_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_invitations_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **resource_id** | **str**|  | 
 **invitation_request** | [**InvitationRequest**](InvitationRequest.md)|  | 

### Return type

[**Invitation**](Invitation.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_link_configuration_update**
> Item api_v1_0_items_link_configuration_update(id, item_request)

Update link configuration with specific rights (cf get_abilities).

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.models.item_request import ItemRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    item_request = openapi_client.ItemRequest() # ItemRequest | 

    try:
        api_response = api_instance.api_v1_0_items_link_configuration_update(id, item_request)
        print("The response of ApiApi->api_v1_0_items_link_configuration_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_link_configuration_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **item_request** | [**ItemRequest**](ItemRequest.md)|  | 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_list**
> PaginatedListItemList api_v1_0_items_list(page=page, page_size=page_size)

List top level items with pagination and filtering.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.paginated_list_item_list import PaginatedListItemList
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    page = 56 # int | A page number within the paginated result set. (optional)
    page_size = 56 # int | Number of results to return per page. (optional)

    try:
        api_response = api_instance.api_v1_0_items_list(page=page, page_size=page_size)
        print("The response of ApiApi->api_v1_0_items_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_list: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **page** | **int**| A page number within the paginated result set. | [optional] 
 **page_size** | **int**| Number of results to return per page. | [optional] 

### Return type

[**PaginatedListItemList**](PaginatedListItemList.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_media_auth_retrieve**
> Item api_v1_0_items_media_auth_retrieve()

This view is used by an Nginx subrequest to control access to an item's
attachment file.

When we let the request go through, we compute authorization headers that will be added to
the request going through thanks to the nginx.ingress.kubernetes.io/auth-response-headers
annotation. The request will then be proxied to the object storage backend who will
respond with the file after checking the signature included in headers.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)

    try:
        api_response = api_instance.api_v1_0_items_media_auth_retrieve()
        print("The response of ApiApi->api_v1_0_items_media_auth_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_media_auth_retrieve: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_move_create**
> Item api_v1_0_items_move_create(id, item_request)

Move an item to another location within the item tree.

The user must be an administrator or owner of both the item being moved
and the target parent item.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.models.item_request import ItemRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    item_request = openapi_client.ItemRequest() # ItemRequest | 

    try:
        api_response = api_instance.api_v1_0_items_move_create(id, item_request)
        print("The response of ApiApi->api_v1_0_items_move_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_move_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **item_request** | [**ItemRequest**](ItemRequest.md)|  | 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_partial_update**
> Item api_v1_0_items_partial_update(id, patched_item_request=patched_item_request)

ItemViewSet API.

This view set provides CRUD operations and additional actions for managing items.
Supports filtering, ordering, and annotations for enhanced querying capabilities.

### API Endpoints:
1. **List**: Retrieve a paginated list of items.
   Example: GET /items/?page=2
2. **Retrieve**: Get a specific item by its ID.
   Example: GET /items/{id}/
3. **Create**: Create a new item.
   Example: POST /items/
4. **Update**: Update a item by its ID.
   Example: PUT /items/{id}/
5. **Delete**: Soft delete a item by its ID.
   Example: DELETE /items/{id}/

### Additional Actions:
1. **Trashbin**: List soft deleted items for an items owner
    Example: GET /items/trashbin/

2. **Children**: List or create child items.
    Example: GET, POST /items/{id}/children/

3. **Favorite**: Get list of favorite items for a user. Mark or unmark
    a item as favorite.
    Examples:
    - GET /items/favorites/
    - POST, DELETE /items/{id}/favorite/

4. **Link Configuration**: Update item link configuration.
    Example: PUT /items/{id}/link-configuration/

5. **Media Auth**: Authorize access to item media.
    Example: GET /items/media-auth/

6. **Duplicate**: Duplicate an item of type file.
    Example:

### Ordering: created_at, updated_at, is_favorite, title

    Example:
    - Ascending: GET /api/v1.0/items/?ordering=created_at
    - Desceding: GET /api/v1.0/items/?ordering=-title

### Filtering:
    - `is_creator_me=true`: Returns items created by the current user.
    - `is_creator_me=false`: Returns items created by other users.
    - `is_favorite=true`: Returns items marked as favorite by the current user
    - `is_favorite=false`: Returns items not marked as favorite by the current user
    - `title=hello`: Returns items which title contains the "hello" string

    Example:
    - GET /api/v1.0/items/?is_creator_me=true&is_favorite=true
    - GET /api/v1.0/items/?is_creator_me=false&title=hello

### Annotations:
1. **is_favorite**: Indicates whether the item is marked as favorite by the current user.
2. *`*user_roles**: Roles the current user has on the item or its ancestors.

### Notes:
- Only the highest ancestor in a item hierarchy is shown in list views.
- Implements soft delete logic to retain item tree structures.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.models.patched_item_request import PatchedItemRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    patched_item_request = openapi_client.PatchedItemRequest() # PatchedItemRequest |  (optional)

    try:
        api_response = api_instance.api_v1_0_items_partial_update(id, patched_item_request=patched_item_request)
        print("The response of ApiApi->api_v1_0_items_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_partial_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **patched_item_request** | [**PatchedItemRequest**](PatchedItemRequest.md)|  | [optional] 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_recents_retrieve**
> ListItemLight api_v1_0_items_recents_retrieve()

Get list of recents items for the current user.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.list_item_light import ListItemLight
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)

    try:
        api_response = api_instance.api_v1_0_items_recents_retrieve()
        print("The response of ApiApi->api_v1_0_items_recents_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_recents_retrieve: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListItemLight**](ListItemLight.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_restore_create**
> Item api_v1_0_items_restore_create(id, item_request)

Restore a soft-deleted item if it was deleted less than x days ago.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.models.item_request import ItemRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    item_request = openapi_client.ItemRequest() # ItemRequest | 

    try:
        api_response = api_instance.api_v1_0_items_restore_create(id, item_request)
        print("The response of ApiApi->api_v1_0_items_restore_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_restore_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **item_request** | [**ItemRequest**](ItemRequest.md)|  | 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_restrict_create**
> Item api_v1_0_items_restrict_create(id, item_request)

Activate or deactivate restriction on the folder based on the HTTP method.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.models.item_request import ItemRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    item_request = openapi_client.ItemRequest() # ItemRequest | 

    try:
        api_response = api_instance.api_v1_0_items_restrict_create(id, item_request)
        print("The response of ApiApi->api_v1_0_items_restrict_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_restrict_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **item_request** | [**ItemRequest**](ItemRequest.md)|  | 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_restrict_destroy**
> api_v1_0_items_restrict_destroy(id)

Activate or deactivate restriction on the folder based on the HTTP method.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        api_instance.api_v1_0_items_restrict_destroy(id)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_restrict_destroy: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_retrieve**
> Item api_v1_0_items_retrieve(id)

Add a trace that the item was accessed by a user. This is used to list items
on a user's list view even though the user has no specific role in the item (link
access when the link reach configuration of the item allows it).

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        api_response = api_instance.api_v1_0_items_retrieve(id)
        print("The response of ApiApi->api_v1_0_items_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_search_retrieve**
> SearchItem api_v1_0_items_search_retrieve()

Returns a DRF response containing the filtered, annotated and ordered items.

Applies filtering based on request parameter 'q' from `SearchItemFilter`.
Depending of the configuration it can be:
 - A fulltext search through the opensearch indexation app "find" if the backend is
   enabled (see SEARCH_INDEXER_CLASS) and the feature flag INDEXED_SEARCH_ENABLED is True
 - A filtering by the model fields 'title' & 'type'.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.search_item import SearchItem
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)

    try:
        api_response = api_instance.api_v1_0_items_search_retrieve()
        print("The response of ApiApi->api_v1_0_items_search_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_search_retrieve: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**SearchItem**](SearchItem.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_trashbin_retrieve**
> ListItem api_v1_0_items_trashbin_retrieve()

Retrieve soft-deleted items for which the current user has the owner role.

The selected items are those deleted within the cutoff period defined in the
settings (see TRASHBIN_CUTOFF_DAYS), before they are considered permanently deleted.

Optimized version that uses EXISTS instead of expensive subqueries to check
owner access on items or their ancestors.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.list_item import ListItem
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)

    try:
        api_response = api_instance.api_v1_0_items_trashbin_retrieve()
        print("The response of ApiApi->api_v1_0_items_trashbin_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_trashbin_retrieve: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**ListItem**](ListItem.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_tree_retrieve**
> ListItem api_v1_0_items_tree_retrieve(id)

List ancestors tree above the item
What we need to display is the tree structure opened for the current document.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.list_item import ListItem
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        api_response = api_instance.api_v1_0_items_tree_retrieve(id)
        print("The response of ApiApi->api_v1_0_items_tree_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_tree_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

[**ListItem**](ListItem.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_update**
> Item api_v1_0_items_update(id, item_request)

ItemViewSet API.

This view set provides CRUD operations and additional actions for managing items.
Supports filtering, ordering, and annotations for enhanced querying capabilities.

### API Endpoints:
1. **List**: Retrieve a paginated list of items.
   Example: GET /items/?page=2
2. **Retrieve**: Get a specific item by its ID.
   Example: GET /items/{id}/
3. **Create**: Create a new item.
   Example: POST /items/
4. **Update**: Update a item by its ID.
   Example: PUT /items/{id}/
5. **Delete**: Soft delete a item by its ID.
   Example: DELETE /items/{id}/

### Additional Actions:
1. **Trashbin**: List soft deleted items for an items owner
    Example: GET /items/trashbin/

2. **Children**: List or create child items.
    Example: GET, POST /items/{id}/children/

3. **Favorite**: Get list of favorite items for a user. Mark or unmark
    a item as favorite.
    Examples:
    - GET /items/favorites/
    - POST, DELETE /items/{id}/favorite/

4. **Link Configuration**: Update item link configuration.
    Example: PUT /items/{id}/link-configuration/

5. **Media Auth**: Authorize access to item media.
    Example: GET /items/media-auth/

6. **Duplicate**: Duplicate an item of type file.
    Example:

### Ordering: created_at, updated_at, is_favorite, title

    Example:
    - Ascending: GET /api/v1.0/items/?ordering=created_at
    - Desceding: GET /api/v1.0/items/?ordering=-title

### Filtering:
    - `is_creator_me=true`: Returns items created by the current user.
    - `is_creator_me=false`: Returns items created by other users.
    - `is_favorite=true`: Returns items marked as favorite by the current user
    - `is_favorite=false`: Returns items not marked as favorite by the current user
    - `title=hello`: Returns items which title contains the "hello" string

    Example:
    - GET /api/v1.0/items/?is_creator_me=true&is_favorite=true
    - GET /api/v1.0/items/?is_creator_me=false&title=hello

### Annotations:
1. **is_favorite**: Indicates whether the item is marked as favorite by the current user.
2. *`*user_roles**: Roles the current user has on the item or its ancestors.

### Notes:
- Only the highest ancestor in a item hierarchy is shown in list views.
- Implements soft delete logic to retain item tree structures.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.models.item_request import ItemRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    item_request = openapi_client.ItemRequest() # ItemRequest | 

    try:
        api_response = api_instance.api_v1_0_items_update(id, item_request)
        print("The response of ApiApi->api_v1_0_items_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **item_request** | [**ItemRequest**](ItemRequest.md)|  | 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_upload_ended_create**
> Item api_v1_0_items_upload_ended_create(id, item_request)

Start the analysis of an item after a successful upload.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.models.item_request import ItemRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    item_request = openapi_client.ItemRequest() # ItemRequest | 

    try:
        api_response = api_instance.api_v1_0_items_upload_ended_create(id, item_request)
        print("The response of ApiApi->api_v1_0_items_upload_ended_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_upload_ended_create: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **item_request** | [**ItemRequest**](ItemRequest.md)|  | 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_items_wopi_retrieve**
> Item api_v1_0_items_wopi_retrieve(id)

This view is used to generate an access token and access token ttl in order to start
a WOPI session for the item and the current user.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.item import Item
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 

    try:
        api_response = api_instance.api_v1_0_items_wopi_retrieve(id)
        print("The response of ApiApi->api_v1_0_items_wopi_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_items_wopi_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 

### Return type

[**Item**](Item.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_sdk_relay_events_create**
> api_v1_0_sdk_relay_events_create()

POST /api/v1.0/sdk-relay/events/

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)

    try:
        api_instance.api_v1_0_sdk_relay_events_create()
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_sdk_relay_events_create: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_sdk_relay_events_retrieve**
> api_v1_0_sdk_relay_events_retrieve(id)

GET /api/v1.0/sdk-relay/events/<token>/

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = 'id_example' # str | 

    try:
        api_instance.api_v1_0_sdk_relay_events_retrieve(id)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_sdk_relay_events_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_user_reconciliations_retrieve**
> api_v1_0_user_reconciliations_retrieve(confirmation_id, user_type)

Check the confirmation ID and mark the corresponding email as checked.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    confirmation_id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    user_type = 'user_type_example' # str | 

    try:
        api_instance.api_v1_0_user_reconciliations_retrieve(confirmation_id, user_type)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_user_reconciliations_retrieve: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **confirmation_id** | **UUID**|  | 
 **user_type** | **str**|  | 

### Return type

void (empty response body)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_users_contacts_retrieve**
> UserLight api_v1_0_users_contacts_retrieve()

Return the people involved in sharing with the current user, in either
direction, most frequent first.

A contact either holds an access on one of the user's items ("shared
with") or created one of them ("shared by"). Frequency is the number of
such items they hold an access on, so a contact's own private items do
not inflate their ranking.

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.user_light import UserLight
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)

    try:
        api_response = api_instance.api_v1_0_users_contacts_retrieve()
        print("The response of ApiApi->api_v1_0_users_contacts_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_users_contacts_retrieve: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UserLight**](UserLight.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_users_list**
> List[User] api_v1_0_users_list()

User ViewSet

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.user import User
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)

    try:
        api_response = api_instance.api_v1_0_users_list()
        print("The response of ApiApi->api_v1_0_users_list:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_users_list: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[User]**](User.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_users_me_retrieve**
> UserMe api_v1_0_users_me_retrieve()

Return information on currently logged user

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.user_me import UserMe
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)

    try:
        api_response = api_instance.api_v1_0_users_me_retrieve()
        print("The response of ApiApi->api_v1_0_users_me_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_users_me_retrieve: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**UserMe**](UserMe.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_users_partial_update**
> User api_v1_0_users_partial_update(id, patched_user_request=patched_user_request)

User ViewSet

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.patched_user_request import PatchedUserRequest
from openapi_client.models.user import User
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    patched_user_request = openapi_client.PatchedUserRequest() # PatchedUserRequest |  (optional)

    try:
        api_response = api_instance.api_v1_0_users_partial_update(id, patched_user_request=patched_user_request)
        print("The response of ApiApi->api_v1_0_users_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_users_partial_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **patched_user_request** | [**PatchedUserRequest**](PatchedUserRequest.md)|  | [optional] 

### Return type

[**User**](User.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **api_v1_0_users_update**
> User api_v1_0_users_update(id, user_request=user_request)

User ViewSet

### Example

* Api Key Authentication (cookieAuth):

```python
import openapi_client
from openapi_client.models.user import User
from openapi_client.models.user_request import UserRequest
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: cookieAuth
configuration.api_key['cookieAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['cookieAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.ApiApi(api_client)
    id = UUID('38400000-8cf0-11bd-b23e-10b96e4ef00d') # UUID | 
    user_request = openapi_client.UserRequest() # UserRequest |  (optional)

    try:
        api_response = api_instance.api_v1_0_users_update(id, user_request=user_request)
        print("The response of ApiApi->api_v1_0_users_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ApiApi->api_v1_0_users_update: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **UUID**|  | 
 **user_request** | [**UserRequest**](UserRequest.md)|  | [optional] 

### Return type

[**User**](User.md)

### Authorization

[cookieAuth](../README.md#cookieAuth)

### HTTP request headers

 - **Content-Type**: application/json, multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

