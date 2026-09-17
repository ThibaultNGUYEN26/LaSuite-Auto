# RoleInResponseMeta


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**resource_type** | **str** |  | [optional] 
**location** | **str** |  | [optional] 

## Example

```python
from grist_client.models.role_in_response_meta import RoleInResponseMeta

# TODO update the JSON string below
json = "{}"
# create an instance of RoleInResponseMeta from a JSON string
role_in_response_meta_instance = RoleInResponseMeta.from_json(json)
# print the JSON string representation of the object
print(RoleInResponseMeta.to_json())

# convert the object into a dict
role_in_response_meta_dict = role_in_response_meta_instance.to_dict()
# create an instance of RoleInResponseMeta from a dict
role_in_response_meta_from_dict = RoleInResponseMeta.from_dict(role_in_response_meta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


