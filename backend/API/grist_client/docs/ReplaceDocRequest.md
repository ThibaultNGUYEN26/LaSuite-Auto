# ReplaceDocRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**source_doc_id** | **str** | ID of document to copy content from | [optional] 
**snapshot_id** | **str** | ID of snapshot to restore from | [optional] 
**reset_tutorial_metadata** | **bool** | Reset tutorial progress when replacing (for tutorial forks) | [optional] 

## Example

```python
from grist_client.models.replace_doc_request import ReplaceDocRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ReplaceDocRequest from a JSON string
replace_doc_request_instance = ReplaceDocRequest.from_json(json)
# print the JSON string representation of the object
print(ReplaceDocRequest.to_json())

# convert the object into a dict
replace_doc_request_dict = replace_doc_request_instance.to_dict()
# create an instance of ReplaceDocRequest from a dict
replace_doc_request_from_dict = ReplaceDocRequest.from_dict(replace_doc_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


