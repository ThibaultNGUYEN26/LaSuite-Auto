# ListItemRequest

Serialize items with limited fields for display in lists.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**filename** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.list_item_request import ListItemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ListItemRequest from a JSON string
list_item_request_instance = ListItemRequest.from_json(json)
# print the JSON string representation of the object
print(ListItemRequest.to_json())

# convert the object into a dict
list_item_request_dict = list_item_request_instance.to_dict()
# create an instance of ListItemRequest from a dict
list_item_request_from_dict = ListItemRequest.from_dict(list_item_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


