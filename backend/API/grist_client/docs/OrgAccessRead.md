# OrgAccessRead


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**users** | [**List[OrgAccessReadUsersInner]**](OrgAccessReadUsersInner.md) |  | 

## Example

```python
from grist_client.models.org_access_read import OrgAccessRead

# TODO update the JSON string below
json = "{}"
# create an instance of OrgAccessRead from a JSON string
org_access_read_instance = OrgAccessRead.from_json(json)
# print the JSON string representation of the object
print(OrgAccessRead.to_json())

# convert the object into a dict
org_access_read_dict = org_access_read_instance.to_dict()
# create an instance of OrgAccessRead from a dict
org_access_read_from_dict = OrgAccessRead.from_dict(org_access_read_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


