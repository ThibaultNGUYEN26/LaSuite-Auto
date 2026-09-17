# GroupInResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**meta** | [**GroupInResponseMeta**](GroupInResponseMeta.md) |  | [optional] 
**id** | **str** | The unique identifier of the group. | [optional] 
**display_name** | **str** | The name of the group. | [optional] 
**members** | [**List[MembersInResponseInner]**](MembersInResponseInner.md) |  | [optional] 

## Example

```python
from grist_client.models.group_in_response import GroupInResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GroupInResponse from a JSON string
group_in_response_instance = GroupInResponse.from_json(json)
# print the JSON string representation of the object
print(GroupInResponse.to_json())

# convert the object into a dict
group_in_response_dict = group_in_response_instance.to_dict()
# create an instance of GroupInResponse from a dict
group_in_response_from_dict = GroupInResponse.from_dict(group_in_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


