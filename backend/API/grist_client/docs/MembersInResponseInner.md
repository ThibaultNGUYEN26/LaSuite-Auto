# MembersInResponseInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **str** | The ID of a member. | 
**display** | **str** | The display name of a member. | 
**type** | **str** | The type of member (User or Group). | 
**ref** | **str** | The URL to access the member | 

## Example

```python
from grist_client.models.members_in_response_inner import MembersInResponseInner

# TODO update the JSON string below
json = "{}"
# create an instance of MembersInResponseInner from a JSON string
members_in_response_inner_instance = MembersInResponseInner.from_json(json)
# print the JSON string representation of the object
print(MembersInResponseInner.to_json())

# convert the object into a dict
members_in_response_inner_dict = members_in_response_inner_instance.to_dict()
# create an instance of MembersInResponseInner from a dict
members_in_response_inner_from_dict = MembersInResponseInner.from_dict(members_in_response_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


