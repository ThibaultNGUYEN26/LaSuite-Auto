# WorkspaceWithDocsAndDomain


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**name** | **str** |  | 
**access** | [**Access**](Access.md) |  | 
**docs** | [**List[Doc]**](Doc.md) |  | 
**org_domain** | **str** |  | [optional] 

## Example

```python
from grist_client.models.workspace_with_docs_and_domain import WorkspaceWithDocsAndDomain

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceWithDocsAndDomain from a JSON string
workspace_with_docs_and_domain_instance = WorkspaceWithDocsAndDomain.from_json(json)
# print the JSON string representation of the object
print(WorkspaceWithDocsAndDomain.to_json())

# convert the object into a dict
workspace_with_docs_and_domain_dict = workspace_with_docs_and_domain_instance.to_dict()
# create an instance of WorkspaceWithDocsAndDomain from a dict
workspace_with_docs_and_domain_from_dict = WorkspaceWithDocsAndDomain.from_dict(workspace_with_docs_and_domain_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


