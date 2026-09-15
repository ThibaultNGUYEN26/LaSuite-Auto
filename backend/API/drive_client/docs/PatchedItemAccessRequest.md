# PatchedItemAccessRequest

Serialize item accesses.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_id** | **UUID** | primary key for the record as UUID | [optional] 
**team** | **str** |  | [optional] 
**role** | [**RoleEnum**](RoleEnum.md) |  | [optional] 

## Example

```python
from openapi_client.models.patched_item_access_request import PatchedItemAccessRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedItemAccessRequest from a JSON string
patched_item_access_request_instance = PatchedItemAccessRequest.from_json(json)
# print the JSON string representation of the object
print(PatchedItemAccessRequest.to_json())

# convert the object into a dict
patched_item_access_request_dict = patched_item_access_request_instance.to_dict()
# create an instance of PatchedItemAccessRequest from a dict
patched_item_access_request_from_dict = PatchedItemAccessRequest.from_dict(patched_item_access_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


