# WorkspaceAccessRead


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max_inherited_role** | [**Access**](Access.md) |  | 
**users** | [**List[WorkspaceAccessReadUsersInner]**](WorkspaceAccessReadUsersInner.md) |  | 

## Example

```python
from grist_client.models.workspace_access_read import WorkspaceAccessRead

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceAccessRead from a JSON string
workspace_access_read_instance = WorkspaceAccessRead.from_json(json)
# print the JSON string representation of the object
print(WorkspaceAccessRead.to_json())

# convert the object into a dict
workspace_access_read_dict = workspace_access_read_instance.to_dict()
# create an instance of WorkspaceAccessRead from a dict
workspace_access_read_from_dict = WorkspaceAccessRead.from_dict(workspace_access_read_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


