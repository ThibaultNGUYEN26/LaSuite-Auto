# grist_client.WebhooksApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**clear_webhook_queue**](WebhooksApi.md#clear_webhook_queue) | **DELETE** /docs/{docId}/webhooks/queue | Empty a document&#39;s queue of undelivered payloads
[**clear_webhook_queue_for_webhook**](WebhooksApi.md#clear_webhook_queue_for_webhook) | **DELETE** /docs/{docId}/webhooks/queue/{webhookId} | Clear queue for a specific webhook
[**create_webhooks**](WebhooksApi.md#create_webhooks) | **POST** /docs/{docId}/webhooks | Create new webhooks for a document
[**delete_webhook**](WebhooksApi.md#delete_webhook) | **DELETE** /docs/{docId}/webhooks/{webhookId} | Remove a webhook
[**list_webhooks**](WebhooksApi.md#list_webhooks) | **GET** /docs/{docId}/webhooks | Webhooks associated with a document
[**modify_webhook**](WebhooksApi.md#modify_webhook) | **PATCH** /docs/{docId}/webhooks/{webhookId} | Modify a webhook


# **clear_webhook_queue**
> clear_webhook_queue(doc_id)

Empty a document's queue of undelivered payloads

Clear all pending webhook deliveries for this document. Use this
if the queue has built up due to unreachable endpoints.


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
    api_instance = grist_client.WebhooksApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Empty a document's queue of undelivered payloads
        api_instance.clear_webhook_queue(doc_id)
    except Exception as e:
        print("Exception when calling WebhooksApi->clear_webhook_queue: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

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
**200** | Queue cleared successfully. Returns empty body. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **clear_webhook_queue_for_webhook**
> ClearWebhookQueueForWebhook200Response clear_webhook_queue_for_webhook(doc_id, webhook_id)

Clear queue for a specific webhook

Clear the queue of pending payloads for a specific webhook.
Only document owners can call this endpoint.


### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.clear_webhook_queue_for_webhook200_response import ClearWebhookQueueForWebhook200Response
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
    api_instance = grist_client.WebhooksApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    webhook_id = 'webhook_id_example' # str | ID of the webhook

    try:
        # Clear queue for a specific webhook
        api_response = api_instance.clear_webhook_queue_for_webhook(doc_id, webhook_id)
        print("The response of WebhooksApi->clear_webhook_queue_for_webhook:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->clear_webhook_queue_for_webhook: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **webhook_id** | **str**| ID of the webhook | 

### Return type

[**ClearWebhookQueueForWebhook200Response**](ClearWebhookQueueForWebhook200Response.md)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Queue cleared |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_webhooks**
> CreateWebhooks200Response create_webhooks(doc_id, create_webhooks_request=create_webhooks_request)

Create new webhooks for a document

Creates one or more webhooks that will POST to specified URLs when
data in the document changes. Returns the IDs of the created webhooks.


### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.create_webhooks200_response import CreateWebhooks200Response
from grist_client.models.create_webhooks_request import CreateWebhooksRequest
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
    api_instance = grist_client.WebhooksApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    create_webhooks_request = grist_client.CreateWebhooksRequest() # CreateWebhooksRequest | an array of webhook settings (optional)

    try:
        # Create new webhooks for a document
        api_response = api_instance.create_webhooks(doc_id, create_webhooks_request=create_webhooks_request)
        print("The response of WebhooksApi->create_webhooks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->create_webhooks: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **create_webhooks_request** | [**CreateWebhooksRequest**](CreateWebhooksRequest.md)| an array of webhook settings | [optional] 

### Return type

[**CreateWebhooks200Response**](CreateWebhooks200Response.md)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_webhook**
> DeleteWebhook200Response delete_webhook(doc_id, webhook_id)

Remove a webhook

Permanently delete a webhook. Any pending deliveries in the queue
for this webhook will also be removed.


### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.delete_webhook200_response import DeleteWebhook200Response
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
    api_instance = grist_client.WebhooksApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    webhook_id = 'webhook_id_example' # str | 

    try:
        # Remove a webhook
        api_response = api_instance.delete_webhook(doc_id, webhook_id)
        print("The response of WebhooksApi->delete_webhook:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->delete_webhook: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **webhook_id** | **str**|  | 

### Return type

[**DeleteWebhook200Response**](DeleteWebhook200Response.md)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Webhook deleted successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_webhooks**
> ListWebhooks200Response list_webhooks(doc_id)

Webhooks associated with a document

Returns all webhooks configured for this document, including their
settings and delivery statistics.


### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.list_webhooks200_response import ListWebhooks200Response
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
    api_instance = grist_client.WebhooksApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)

    try:
        # Webhooks associated with a document
        api_response = api_instance.list_webhooks(doc_id)
        print("The response of WebhooksApi->list_webhooks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WebhooksApi->list_webhooks: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 

### Return type

[**ListWebhooks200Response**](ListWebhooks200Response.md)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of webhooks. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **modify_webhook**
> modify_webhook(doc_id, webhook_id, webhook_partial_fields=webhook_partial_fields)

Modify a webhook

Update the configuration of an existing webhook, such as its URL,
enabled state, or event types.


### Example

* OAuth Authentication (OAuth2):
* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.webhook_partial_fields import WebhookPartialFields
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
    api_instance = grist_client.WebhooksApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    webhook_id = 'webhook_id_example' # str | 
    webhook_partial_fields = grist_client.WebhookPartialFields() # WebhookPartialFields | the changes to make (optional)

    try:
        # Modify a webhook
        api_instance.modify_webhook(doc_id, webhook_id, webhook_partial_fields=webhook_partial_fields)
    except Exception as e:
        print("Exception when calling WebhooksApi->modify_webhook: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **webhook_id** | **str**|  | 
 **webhook_partial_fields** | [**WebhookPartialFields**](WebhookPartialFields.md)| the changes to make | [optional] 

### Return type

void (empty response body)

### Authorization

[OAuth2](../README.md#OAuth2), [ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Webhook updated successfully. Returns empty body. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

