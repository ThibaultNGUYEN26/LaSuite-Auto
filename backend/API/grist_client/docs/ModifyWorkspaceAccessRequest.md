# ModifyWorkspaceAccessRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delta** | [**WorkspaceAccessWrite**](WorkspaceAccessWrite.md) |  | 

## Example

```python
from grist_client.models.modify_workspace_access_request import ModifyWorkspaceAccessRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ModifyWorkspaceAccessRequest from a JSON string
modify_workspace_access_request_instance = ModifyWorkspaceAccessRequest.from_json(json)
# print the JSON string representation of the object
print(ModifyWorkspaceAccessRequest.to_json())

# convert the object into a dict
modify_workspace_access_request_dict = modify_workspace_access_request_instance.to_dict()
# create an instance of ModifyWorkspaceAccessRequest from a dict
modify_workspace_access_request_from_dict = ModifyWorkspaceAccessRequest.from_dict(modify_workspace_access_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


