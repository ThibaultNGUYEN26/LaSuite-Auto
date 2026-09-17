# GroupInRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**display_name** | **str** | The display name of the group. | [optional] 
**members** | [**List[MembersInRequestInner]**](MembersInRequestInner.md) |  | [optional] 

## Example

```python
from grist_client.models.group_in_request import GroupInRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GroupInRequest from a JSON string
group_in_request_instance = GroupInRequest.from_json(json)
# print the JSON string representation of the object
print(GroupInRequest.to_json())

# convert the object into a dict
group_in_request_dict = group_in_request_instance.to_dict()
# create an instance of GroupInRequest from a dict
group_in_request_from_dict = GroupInRequest.from_dict(group_in_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


