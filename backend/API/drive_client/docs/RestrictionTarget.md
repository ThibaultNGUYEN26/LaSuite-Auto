# RestrictionTarget

Serialize the restricted folder a restriction points to.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** | primary key for the record as UUID | [readonly] 
**title** | **str** |  | [readonly] 
**is_restricted** | **bool** | Return True: the target of an existing restriction is restricted by definition. | [readonly] 
**deleted** | **bool** | Return whether the target is in the trash. | [readonly] 
**can_access** | **bool** | Return whether the request user can open the target. | [readonly] 

## Example

```python
from openapi_client.models.restriction_target import RestrictionTarget

# TODO update the JSON string below
json = "{}"
# create an instance of RestrictionTarget from a JSON string
restriction_target_instance = RestrictionTarget.from_json(json)
# print the JSON string representation of the object
print(RestrictionTarget.to_json())

# convert the object into a dict
restriction_target_dict = restriction_target_instance.to_dict()
# create an instance of RestrictionTarget from a dict
restriction_target_from_dict = RestrictionTarget.from_dict(restriction_target_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


