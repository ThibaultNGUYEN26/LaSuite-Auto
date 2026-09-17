# WorkspaceAccessReadUsersInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**email** | **str** |  | [optional] 
**access** | [**Access**](Access.md) |  | [optional] 
**parent_access** | [**Access**](Access.md) |  | [optional] 

## Example

```python
from grist_client.models.workspace_access_read_users_inner import WorkspaceAccessReadUsersInner

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceAccessReadUsersInner from a JSON string
workspace_access_read_users_inner_instance = WorkspaceAccessReadUsersInner.from_json(json)
# print the JSON string representation of the object
print(WorkspaceAccessReadUsersInner.to_json())

# convert the object into a dict
workspace_access_read_users_inner_dict = workspace_access_read_users_inner_instance.to_dict()
# create an instance of WorkspaceAccessReadUsersInner from a dict
workspace_access_read_users_inner_from_dict = WorkspaceAccessReadUsersInner.from_dict(workspace_access_read_users_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


