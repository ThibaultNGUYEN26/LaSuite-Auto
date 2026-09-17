# GetActiveSession200ResponseOrgError

Error information if org access failed

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** |  | [optional] 
**status** | **int** |  | [optional] 

## Example

```python
from grist_client.models.get_active_session200_response_org_error import GetActiveSession200ResponseOrgError

# TODO update the JSON string below
json = "{}"
# create an instance of GetActiveSession200ResponseOrgError from a JSON string
get_active_session200_response_org_error_instance = GetActiveSession200ResponseOrgError.from_json(json)
# print the JSON string representation of the object
print(GetActiveSession200ResponseOrgError.to_json())

# convert the object into a dict
get_active_session200_response_org_error_dict = get_active_session200_response_org_error_instance.to_dict()
# create an instance of GetActiveSession200ResponseOrgError from a dict
get_active_session200_response_org_error_from_dict = GetActiveSession200ResponseOrgError.from_dict(get_active_session200_response_org_error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


