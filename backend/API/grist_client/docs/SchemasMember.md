# SchemasMember


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **str** | The ID of a member. | [optional] 
**display** | **str** | The display name of a member. | [optional] 
**type** | **str** | The type of member (User or Group). | [optional] 
**ref** | **str** | The URL to access the member | [optional] 

## Example

```python
from grist_client.models.schemas_member import SchemasMember

# TODO update the JSON string below
json = "{}"
# create an instance of SchemasMember from a JSON string
schemas_member_instance = SchemasMember.from_json(json)
# print the JSON string representation of the object
print(SchemasMember.to_json())

# convert the object into a dict
schemas_member_dict = schemas_member_instance.to_dict()
# create an instance of SchemasMember from a dict
schemas_member_from_dict = SchemasMember.from_dict(schemas_member_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


