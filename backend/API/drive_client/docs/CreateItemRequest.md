# CreateItemRequest

Serializer used to create a new item

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** | primary key for the record as UUID | [optional] 
**title** | **str** |  | [optional] 
**type** | [**TypeEnum**](TypeEnum.md) |  | [optional] 
**filename** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**extension** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.create_item_request import CreateItemRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateItemRequest from a JSON string
create_item_request_instance = CreateItemRequest.from_json(json)
# print the JSON string representation of the object
print(CreateItemRequest.to_json())

# convert the object into a dict
create_item_request_dict = create_item_request_instance.to_dict()
# create an instance of CreateItemRequest from a dict
create_item_request_from_dict = CreateItemRequest.from_dict(create_item_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


