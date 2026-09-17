# RecoverDocRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**recovery_mode** | **bool** | Whether to enable recovery mode. Defaults to true if not specified. | [optional] 

## Example

```python
from grist_client.models.recover_doc_request import RecoverDocRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RecoverDocRequest from a JSON string
recover_doc_request_instance = RecoverDocRequest.from_json(json)
# print the JSON string representation of the object
print(RecoverDocRequest.to_json())

# convert the object into a dict
recover_doc_request_dict = recover_doc_request_instance.to_dict()
# create an instance of RecoverDocRequest from a dict
recover_doc_request_from_dict = RecoverDocRequest.from_dict(recover_doc_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


