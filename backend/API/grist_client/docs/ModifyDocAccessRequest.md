# ModifyDocAccessRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delta** | [**WorkspaceAccessWrite**](WorkspaceAccessWrite.md) |  | 

## Example

```python
from grist_client.models.modify_doc_access_request import ModifyDocAccessRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ModifyDocAccessRequest from a JSON string
modify_doc_access_request_instance = ModifyDocAccessRequest.from_json(json)
# print the JSON string representation of the object
print(ModifyDocAccessRequest.to_json())

# convert the object into a dict
modify_doc_access_request_dict = modify_doc_access_request_instance.to_dict()
# create an instance of ModifyDocAccessRequest from a dict
modify_doc_access_request_from_dict = ModifyDocAccessRequest.from_dict(modify_doc_access_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


