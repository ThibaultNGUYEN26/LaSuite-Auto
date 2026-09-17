# CopyDocRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | **int** |  | 
**document_name** | **str** |  | 
**as_template** | **bool** | Remove all data and history but keep the structure to use the document as a template | [optional] 

## Example

```python
from grist_client.models.copy_doc_request import CopyDocRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CopyDocRequest from a JSON string
copy_doc_request_instance = CopyDocRequest.from_json(json)
# print the JSON string representation of the object
print(CopyDocRequest.to_json())

# convert the object into a dict
copy_doc_request_dict = copy_doc_request_instance.to_dict()
# create an instance of CopyDocRequest from a dict
copy_doc_request_from_dict = CopyDocRequest.from_dict(copy_doc_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


