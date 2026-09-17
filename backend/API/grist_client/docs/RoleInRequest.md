# RoleInRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**members** | [**List[SchemasMembersInRequestInner]**](SchemasMembersInRequestInner.md) |  | [optional] 

## Example

```python
from grist_client.models.role_in_request import RoleInRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RoleInRequest from a JSON string
role_in_request_instance = RoleInRequest.from_json(json)
# print the JSON string representation of the object
print(RoleInRequest.to_json())

# convert the object into a dict
role_in_request_dict = role_in_request_instance.to_dict()
# create an instance of RoleInRequest from a dict
role_in_request_from_dict = RoleInRequest.from_dict(role_in_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


