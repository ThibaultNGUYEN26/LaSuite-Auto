# ItemRequest

Serialize items with all fields for display in detail views.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**description** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.item_request import ItemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ItemRequest from a JSON string
item_request_instance = ItemRequest.from_json(json)
# print the JSON string representation of the object
print(ItemRequest.to_json())

# convert the object into a dict
item_request_dict = item_request_instance.to_dict()
# create an instance of ItemRequest from a dict
item_request_from_dict = ItemRequest.from_dict(item_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


