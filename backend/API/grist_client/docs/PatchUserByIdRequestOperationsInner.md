# PatchUserByIdRequestOperationsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**op** | **str** | Operation type (add, replace, remove). | [optional] 
**path** | **object** |  | [optional] 
**value** | **object** |  | [optional] 

## Example

```python
from grist_client.models.patch_user_by_id_request_operations_inner import PatchUserByIdRequestOperationsInner

# TODO update the JSON string below
json = "{}"
# create an instance of PatchUserByIdRequestOperationsInner from a JSON string
patch_user_by_id_request_operations_inner_instance = PatchUserByIdRequestOperationsInner.from_json(json)
# print the JSON string representation of the object
print(PatchUserByIdRequestOperationsInner.to_json())

# convert the object into a dict
patch_user_by_id_request_operations_inner_dict = patch_user_by_id_request_operations_inner_instance.to_dict()
# create an instance of PatchUserByIdRequestOperationsInner from a dict
patch_user_by_id_request_operations_inner_from_dict = PatchUserByIdRequestOperationsInner.from_dict(patch_user_by_id_request_operations_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


