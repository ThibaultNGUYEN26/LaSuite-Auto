# PatchGroupByIdRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**operations** | [**List[PatchGroupByIdRequestOperationsInner]**](PatchGroupByIdRequestOperationsInner.md) |  | [optional] 

## Example

```python
from grist_client.models.patch_group_by_id_request import PatchGroupByIdRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchGroupByIdRequest from a JSON string
patch_group_by_id_request_instance = PatchGroupByIdRequest.from_json(json)
# print the JSON string representation of the object
print(PatchGroupByIdRequest.to_json())

# convert the object into a dict
patch_group_by_id_request_dict = patch_group_by_id_request_instance.to_dict()
# create an instance of PatchGroupByIdRequest from a dict
patch_group_by_id_request_from_dict = PatchGroupByIdRequest.from_dict(patch_group_by_id_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


