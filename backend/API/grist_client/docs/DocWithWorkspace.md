# DocWithWorkspace


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**access** | [**Access**](Access.md) |  | 
**is_pinned** | **bool** |  | 
**url_id** | **str** |  | 
**workspace** | [**WorkspaceWithOrg**](WorkspaceWithOrg.md) |  | 

## Example

```python
from grist_client.models.doc_with_workspace import DocWithWorkspace

# TODO update the JSON string below
json = "{}"
# create an instance of DocWithWorkspace from a JSON string
doc_with_workspace_instance = DocWithWorkspace.from_json(json)
# print the JSON string representation of the object
print(DocWithWorkspace.to_json())

# convert the object into a dict
doc_with_workspace_dict = doc_with_workspace_instance.to_dict()
# create an instance of DocWithWorkspace from a dict
doc_with_workspace_from_dict = DocWithWorkspace.from_dict(doc_with_workspace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


