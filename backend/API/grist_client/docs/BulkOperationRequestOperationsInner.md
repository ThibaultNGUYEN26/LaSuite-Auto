# BulkOperationRequestOperationsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**method** | **str** | HTTP method for the operation. | [optional] 
**path** | **str** | Resource path for the operation. | [optional] 
**data** | **object** | Data for the operation. | [optional] 

## Example

```python
from grist_client.models.bulk_operation_request_operations_inner import BulkOperationRequestOperationsInner

# TODO update the JSON string below
json = "{}"
# create an instance of BulkOperationRequestOperationsInner from a JSON string
bulk_operation_request_operations_inner_instance = BulkOperationRequestOperationsInner.from_json(json)
# print the JSON string representation of the object
print(BulkOperationRequestOperationsInner.to_json())

# convert the object into a dict
bulk_operation_request_operations_inner_dict = bulk_operation_request_operations_inner_instance.to_dict()
# create an instance of BulkOperationRequestOperationsInner from a dict
bulk_operation_request_operations_inner_from_dict = BulkOperationRequestOperationsInner.from_dict(bulk_operation_request_operations_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


