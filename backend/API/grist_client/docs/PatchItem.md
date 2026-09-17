# PatchItem


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**op** | **str** | Operation type (add, replace, remove). | [optional] 
**path** | **str** | The field to be updated. | [optional] 
**value** | **str** | New value for the field. | [optional] 

## Example

```python
from grist_client.models.patch_item import PatchItem

# TODO update the JSON string below
json = "{}"
# create an instance of PatchItem from a JSON string
patch_item_instance = PatchItem.from_json(json)
# print the JSON string representation of the object
print(PatchItem.to_json())

# convert the object into a dict
patch_item_dict = patch_item_instance.to_dict()
# create an instance of PatchItem from a dict
patch_item_from_dict = PatchItem.from_dict(patch_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


