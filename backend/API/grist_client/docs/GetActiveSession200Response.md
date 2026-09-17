# GetActiveSession200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user** | [**User**](User.md) |  | [optional] 
**org** | [**Org**](Org.md) |  | [optional] 
**org_error** | [**GetActiveSession200ResponseOrgError**](GetActiveSession200ResponseOrgError.md) |  | [optional] 

## Example

```python
from grist_client.models.get_active_session200_response import GetActiveSession200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetActiveSession200Response from a JSON string
get_active_session200_response_instance = GetActiveSession200Response.from_json(json)
# print the JSON string representation of the object
print(GetActiveSession200Response.to_json())

# convert the object into a dict
get_active_session200_response_dict = get_active_session200_response_instance.to_dict()
# create an instance of GetActiveSession200Response from a dict
get_active_session200_response_from_dict = GetActiveSession200Response.from_dict(get_active_session200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


