# ModifyOrgAccessRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delta** | [**OrgAccessWrite**](OrgAccessWrite.md) |  | 

## Example

```python
from grist_client.models.modify_org_access_request import ModifyOrgAccessRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ModifyOrgAccessRequest from a JSON string
modify_org_access_request_instance = ModifyOrgAccessRequest.from_json(json)
# print the JSON string representation of the object
print(ModifyOrgAccessRequest.to_json())

# convert the object into a dict
modify_org_access_request_dict = modify_org_access_request_instance.to_dict()
# create an instance of ModifyOrgAccessRequest from a dict
modify_org_access_request_from_dict = ModifyOrgAccessRequest.from_dict(modify_org_access_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


