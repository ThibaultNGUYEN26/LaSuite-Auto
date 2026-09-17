# PatchUserByIdRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**operations** | [**List[PatchUserByIdRequestOperationsInner]**](PatchUserByIdRequestOperationsInner.md) |  | [optional] 

## Example

```python
from grist_client.models.patch_user_by_id_request import PatchUserByIdRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchUserByIdRequest from a JSON string
patch_user_by_id_request_instance = PatchUserByIdRequest.from_json(json)
# print the JSON string representation of the object
print(PatchUserByIdRequest.to_json())

# convert the object into a dict
patch_user_by_id_request_dict = patch_user_by_id_request_instance.to_dict()
# create an instance of PatchUserByIdRequest from a dict
patch_user_by_id_request_from_dict = PatchUserByIdRequest.from_dict(patch_user_by_id_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


