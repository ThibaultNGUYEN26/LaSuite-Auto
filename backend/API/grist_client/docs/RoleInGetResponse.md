# RoleInGetResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | 
**meta** | [**RoleInResponseMeta**](RoleInResponseMeta.md) |  | 
**id** | **str** | The unique identifier of the role. | 
**display_name** | **str** | The name of the role. | 
**members** | [**List[SchemasMembersInResponseInner]**](SchemasMembersInResponseInner.md) |  | 
**org_id** | **float** | The ID of the organization that the role applies to | 
**workspace_id** | **float** | The ID of the workspace that the role applies to | 
**doc_id** | **str** | The ID of the document that the role applies to | 

## Example

```python
from grist_client.models.role_in_get_response import RoleInGetResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RoleInGetResponse from a JSON string
role_in_get_response_instance = RoleInGetResponse.from_json(json)
# print the JSON string representation of the object
print(RoleInGetResponse.to_json())

# convert the object into a dict
role_in_get_response_dict = role_in_get_response_instance.to_dict()
# create an instance of RoleInGetResponse from a dict
role_in_get_response_from_dict = RoleInGetResponse.from_dict(role_in_get_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


