# OrgAccessReadUsersInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**email** | **str** |  | [optional] 
**access** | [**Access**](Access.md) |  | [optional] 

## Example

```python
from grist_client.models.org_access_read_users_inner import OrgAccessReadUsersInner

# TODO update the JSON string below
json = "{}"
# create an instance of OrgAccessReadUsersInner from a JSON string
org_access_read_users_inner_instance = OrgAccessReadUsersInner.from_json(json)
# print the JSON string representation of the object
print(OrgAccessReadUsersInner.to_json())

# convert the object into a dict
org_access_read_users_inner_dict = org_access_read_users_inner_instance.to_dict()
# create an instance of OrgAccessReadUsersInner from a dict
org_access_read_users_inner_from_dict = OrgAccessReadUsersInner.from_dict(org_access_read_users_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


