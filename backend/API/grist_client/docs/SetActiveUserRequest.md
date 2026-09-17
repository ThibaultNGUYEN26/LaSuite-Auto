# SetActiveUserRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** | Email of the user to make active | 
**org** | **str** | Organization subdomain or &#39;current&#39; | [optional] 

## Example

```python
from grist_client.models.set_active_user_request import SetActiveUserRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SetActiveUserRequest from a JSON string
set_active_user_request_instance = SetActiveUserRequest.from_json(json)
# print the JSON string representation of the object
print(SetActiveUserRequest.to_json())

# convert the object into a dict
set_active_user_request_dict = set_active_user_request_instance.to_dict()
# create an instance of SetActiveUserRequest from a dict
set_active_user_request_from_dict = SetActiveUserRequest.from_dict(set_active_user_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


