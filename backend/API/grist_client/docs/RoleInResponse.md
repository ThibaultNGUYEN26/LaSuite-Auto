# RoleInResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**meta** | [**RoleInResponseMeta**](RoleInResponseMeta.md) |  | [optional] 
**id** | **str** | The unique identifier of the role. | [optional] 
**display_name** | **str** | The name of the role. | [optional] 
**members** | [**List[SchemasMembersInResponseInner]**](SchemasMembersInResponseInner.md) |  | [optional] 

## Example

```python
from grist_client.models.role_in_response import RoleInResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RoleInResponse from a JSON string
role_in_response_instance = RoleInResponse.from_json(json)
# print the JSON string representation of the object
print(RoleInResponse.to_json())

# convert the object into a dict
role_in_response_dict = role_in_response_instance.to_dict()
# create an instance of RoleInResponse from a dict
role_in_response_from_dict = RoleInResponse.from_dict(role_in_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


