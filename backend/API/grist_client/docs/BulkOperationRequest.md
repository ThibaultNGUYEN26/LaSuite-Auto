# BulkOperationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**operations** | [**List[BulkOperationRequestOperationsInner]**](BulkOperationRequestOperationsInner.md) | List of operations to be executed. | [optional] 

## Example

```python
from grist_client.models.bulk_operation_request import BulkOperationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of BulkOperationRequest from a JSON string
bulk_operation_request_instance = BulkOperationRequest.from_json(json)
# print the JSON string representation of the object
print(BulkOperationRequest.to_json())

# convert the object into a dict
bulk_operation_request_dict = bulk_operation_request_instance.to_dict()
# create an instance of BulkOperationRequest from a dict
bulk_operation_request_from_dict = BulkOperationRequest.from_dict(bulk_operation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


