# WorkspaceWithDocs


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**access** | [**Access**](Access.md) |  | 
**docs** | [**List[Doc]**](Doc.md) |  | 

## Example

```python
from grist_client.models.workspace_with_docs import WorkspaceWithDocs

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceWithDocs from a JSON string
workspace_with_docs_instance = WorkspaceWithDocs.from_json(json)
# print the JSON string representation of the object
print(WorkspaceWithDocs.to_json())

# convert the object into a dict
workspace_with_docs_dict = workspace_with_docs_instance.to_dict()
# create an instance of WorkspaceWithDocs from a dict
workspace_with_docs_from_dict = WorkspaceWithDocs.from_dict(workspace_with_docs_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


