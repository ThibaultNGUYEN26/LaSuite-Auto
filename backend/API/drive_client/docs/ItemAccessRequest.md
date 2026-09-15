# ItemAccessRequest

Serialize item accesses.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **UUID** | primary key for the record as UUID | [optional] 
**team** | **str** |  | [optional] 
**role** | [**RoleEnum**](RoleEnum.md) |  | [optional] 

## Example

```python
from openapi_client.models.item_access_request import ItemAccessRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ItemAccessRequest from a JSON string
item_access_request_instance = ItemAccessRequest.from_json(json)
# print the JSON string representation of the object
print(ItemAccessRequest.to_json())

# convert the object into a dict
item_access_request_dict = item_access_request_instance.to_dict()
# create an instance of ItemAccessRequest from a dict
item_access_request_from_dict = ItemAccessRequest.from_dict(item_access_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


