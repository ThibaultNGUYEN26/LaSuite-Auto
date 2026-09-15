# PatchedItemRequest

Serialize items with all fields for display in detail views.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.patched_item_request import PatchedItemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedItemRequest from a JSON string
patched_item_request_instance = PatchedItemRequest.from_json(json)
# print the JSON string representation of the object
print(PatchedItemRequest.to_json())

# convert the object into a dict
patched_item_request_dict = patched_item_request_instance.to_dict()
# create an instance of PatchedItemRequest from a dict
patched_item_request_from_dict = PatchedItemRequest.from_dict(patched_item_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


