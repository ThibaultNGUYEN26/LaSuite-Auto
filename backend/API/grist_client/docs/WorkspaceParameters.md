# WorkspaceParameters


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 

## Example

```python
from grist_client.models.workspace_parameters import WorkspaceParameters

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceParameters from a JSON string
workspace_parameters_instance = WorkspaceParameters.from_json(json)
# print the JSON string representation of the object
print(WorkspaceParameters.to_json())

# convert the object into a dict
workspace_parameters_dict = workspace_parameters_instance.to_dict()
# create an instance of WorkspaceParameters from a dict
workspace_parameters_from_dict = WorkspaceParameters.from_dict(workspace_parameters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


