# PatchGroupByIdRequestOperationsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**op** | **str** | Operation type (add, replace, remove). | [optional] 
**path** | **object** |  | [optional] 
**value** | **object** |  | [optional] 

## Example

```python
from grist_client.models.patch_group_by_id_request_operations_inner import PatchGroupByIdRequestOperationsInner

# TODO update the JSON string below
json = "{}"
# create an instance of PatchGroupByIdRequestOperationsInner from a JSON string
patch_group_by_id_request_operations_inner_instance = PatchGroupByIdRequestOperationsInner.from_json(json)
# print the JSON string representation of the object
print(PatchGroupByIdRequestOperationsInner.to_json())

# convert the object into a dict
patch_group_by_id_request_operations_inner_dict = patch_group_by_id_request_operations_inner_instance.to_dict()
# create an instance of PatchGroupByIdRequestOperationsInner from a dict
patch_group_by_id_request_operations_inner_from_dict = PatchGroupByIdRequestOperationsInner.from_dict(patch_group_by_id_request_operations_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


