# SchemasMembersInRequestInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **str** | The ID of a member. | 
**display** | **str** | The display name of a member. | [optional] 
**type** | **str** | The type of member (User or Group). | 
**ref** | **str** | The URL to access the member | [optional] 

## Example

```python
from grist_client.models.schemas_members_in_request_inner import SchemasMembersInRequestInner

# TODO update the JSON string below
json = "{}"
# create an instance of SchemasMembersInRequestInner from a JSON string
schemas_members_in_request_inner_instance = SchemasMembersInRequestInner.from_json(json)
# print the JSON string representation of the object
print(SchemasMembersInRequestInner.to_json())

# convert the object into a dict
schemas_members_in_request_inner_dict = schemas_members_in_request_inner_instance.to_dict()
# create an instance of SchemasMembersInRequestInner from a dict
schemas_members_in_request_inner_from_dict = SchemasMembersInRequestInner.from_dict(schemas_members_in_request_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


