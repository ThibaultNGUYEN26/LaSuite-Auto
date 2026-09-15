# ItemLight

Minimal item serializer for nesting in item accesses.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** | primary key for the record as UUID | [readonly] 
**path** | **str** |  | [readonly] 
**depth** | **str** |  | [readonly] 

## Example

```python
from openapi_client.models.item_light import ItemLight

# TODO update the JSON string below
json = "{}"
# create an instance of ItemLight from a JSON string
item_light_instance = ItemLight.from_json(json)
# print the JSON string representation of the object
print(ItemLight.to_json())

# convert the object into a dict
item_light_dict = item_light_instance.to_dict()
# create an instance of ItemLight from a dict
item_light_from_dict = ItemLight.from_dict(item_light_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


