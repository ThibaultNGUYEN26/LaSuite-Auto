# BatchShareRowRequest

One row of a batch share payload: a contact email and the role to grant.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** |  | 
**role** | [**RoleEnum**](RoleEnum.md) |  | 

## Example

```python
from openapi_client.models.batch_share_row_request import BatchShareRowRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BatchShareRowRequest from a JSON string
batch_share_row_request_instance = BatchShareRowRequest.from_json(json)
# print the JSON string representation of the object
print(BatchShareRowRequest.to_json())

# convert the object into a dict
batch_share_row_request_dict = batch_share_row_request_instance.to_dict()
# create an instance of BatchShareRowRequest from a dict
batch_share_row_request_from_dict = BatchShareRowRequest.from_dict(batch_share_row_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


