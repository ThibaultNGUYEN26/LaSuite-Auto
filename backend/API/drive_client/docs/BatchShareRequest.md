# BatchShareRequest

Validate the payload of the item batch-share action.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rows** | [**List[BatchShareRowRequest]**](BatchShareRowRequest.md) |  | 

## Example

```python
from openapi_client.models.batch_share_request import BatchShareRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BatchShareRequest from a JSON string
batch_share_request_instance = BatchShareRequest.from_json(json)
# print the JSON string representation of the object
print(BatchShareRequest.to_json())

# convert the object into a dict
batch_share_request_dict = batch_share_request_instance.to_dict()
# create an instance of BatchShareRequest from a dict
batch_share_request_from_dict = BatchShareRequest.from_dict(batch_share_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


