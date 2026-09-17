# grist_client.WidgetsApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_widgets**](WidgetsApi.md#list_widgets) | **GET** /widgets | List available custom widgets


# **list_widgets**
> List[ListWidgets200ResponseInner] list_widgets()

List available custom widgets

Get all widget definitions from the configured widget repository.
Custom widgets extend Grist's functionality with specialized views.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.list_widgets200_response_inner import ListWidgets200ResponseInner
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
    api_instance = grist_client.WidgetsApi(api_client)

    try:
        # List available custom widgets
        api_response = api_instance.list_widgets()
        print("The response of WidgetsApi->list_widgets:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WidgetsApi->list_widgets: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[ListWidgets200ResponseInner]**](ListWidgets200ResponseInner.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of widgets |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

