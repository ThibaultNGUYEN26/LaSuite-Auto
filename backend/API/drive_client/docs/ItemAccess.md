# ItemAccess

Serialize item accesses.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** | primary key for the record as UUID | [readonly] 
**user** | [**User**](User.md) |  | [readonly] 
**team** | **str** |  | [optional] 
**role** | [**RoleEnum**](RoleEnum.md) |  | [optional] 
**abilities** | **str** |  | [readonly] 
**max_ancestors_role** | **str** |  | [readonly] 
**max_ancestors_role_item_id** | **str** |  | [readonly] 
**max_role** | **str** |  | [readonly] 
**item** | [**ItemLight**](ItemLight.md) |  | [readonly] 
**is_explicit** | **str** |  | [readonly] 

## Example

```python
from openapi_client.models.item_access import ItemAccess

# TODO update the JSON string below
json = "{}"
# create an instance of ItemAccess from a JSON string
item_access_instance = ItemAccess.from_json(json)
# print the JSON string representation of the object
print(ItemAccess.to_json())

# convert the object into a dict
item_access_dict = item_access_instance.to_dict()
# create an instance of ItemAccess from a dict
item_access_from_dict = ItemAccess.from_dict(item_access_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


