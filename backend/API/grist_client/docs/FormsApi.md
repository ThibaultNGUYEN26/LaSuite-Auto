# grist_client.FormsApi

All URIs are relative to *http://10.19.22.91:8484/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_form_data**](FormsApi.md#get_form_data) | **GET** /docs/{docId}/forms/{viewSectionId} | Get form view data


# **get_form_data**
> GetFormData200Response get_form_data(doc_id, view_section_id)

Get form view data

Get the form configuration for a specific view section. Forms are
a special view type that allows external users to submit data.


### Example

* Bearer (Authorization: Bearer XXXXXXXXXXX) Authentication (ApiKey):

```python
import grist_client
from grist_client.models.get_form_data200_response import GetFormData200Response
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
    api_instance = grist_client.FormsApi(api_client)
    doc_id = 'doc_id_example' # str | A string id (UUID)
    view_section_id = 56 # int | ID of the view section (form)

    try:
        # Get form view data
        api_response = api_instance.get_form_data(doc_id, view_section_id)
        print("The response of FormsApi->get_form_data:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FormsApi->get_form_data: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **doc_id** | **str**| A string id (UUID) | 
 **view_section_id** | **int**| ID of the view section (form) | 

### Return type

[**GetFormData200Response**](GetFormData200Response.md)

### Authorization

[ApiKey](../README.md#ApiKey)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Form data |  -  |
**404** | Form not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

