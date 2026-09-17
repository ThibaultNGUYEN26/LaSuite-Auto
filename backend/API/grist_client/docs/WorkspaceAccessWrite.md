# WorkspaceAccessWrite


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**max_inherited_role** | [**Access**](Access.md) |  | [optional] 
**users** | **Dict[str, str]** |  | [optional] 

## Example

```python
from grist_client.models.workspace_access_write import WorkspaceAccessWrite

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceAccessWrite from a JSON string
workspace_access_write_instance = WorkspaceAccessWrite.from_json(json)
# print the JSON string representation of the object
print(WorkspaceAccessWrite.to_json())

# convert the object into a dict
workspace_access_write_dict = workspace_access_write_instance.to_dict()
# create an instance of WorkspaceAccessWrite from a dict
workspace_access_write_from_dict = WorkspaceAccessWrite.from_dict(workspace_access_write_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


