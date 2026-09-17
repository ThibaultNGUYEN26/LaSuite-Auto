# WorkspaceWithOrg


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**access** | [**Access**](Access.md) |  | 
**org** | [**Org**](Org.md) |  | 

## Example

```python
from grist_client.models.workspace_with_org import WorkspaceWithOrg

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceWithOrg from a JSON string
workspace_with_org_instance = WorkspaceWithOrg.from_json(json)
# print the JSON string representation of the object
print(WorkspaceWithOrg.to_json())

# convert the object into a dict
workspace_with_org_dict = workspace_with_org_instance.to_dict()
# create an instance of WorkspaceWithOrg from a dict
workspace_with_org_from_dict = WorkspaceWithOrg.from_dict(workspace_with_org_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


