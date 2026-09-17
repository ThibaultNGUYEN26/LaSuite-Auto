# WorkspaceWithDocsAndOrg


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**access** | [**Access**](Access.md) |  | 
**docs** | [**List[Doc]**](Doc.md) |  | 
**org** | [**Org**](Org.md) |  | 

## Example

```python
from grist_client.models.workspace_with_docs_and_org import WorkspaceWithDocsAndOrg

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceWithDocsAndOrg from a JSON string
workspace_with_docs_and_org_instance = WorkspaceWithDocsAndOrg.from_json(json)
# print the JSON string representation of the object
print(WorkspaceWithDocsAndOrg.to_json())

# convert the object into a dict
workspace_with_docs_and_org_dict = workspace_with_docs_and_org_instance.to_dict()
# create an instance of WorkspaceWithDocsAndOrg from a dict
workspace_with_docs_and_org_from_dict = WorkspaceWithDocsAndOrg.from_dict(workspace_with_docs_and_org_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


