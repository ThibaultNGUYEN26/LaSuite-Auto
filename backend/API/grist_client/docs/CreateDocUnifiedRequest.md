# CreateDocUnifiedRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_id** | **int** | The workspace to save the document in. If omitted, creates an unsaved document. | [optional] 
**document_name** | **str** | Name for the new document (required when copying) | [optional] 
**source_document_id** | **str** | ID of document to copy from. Requires workspaceId and documentName. | [optional] 
**as_template** | **bool** | When copying, if true, copy structure only without data | [optional] 
**timezone** | **str** | Timezone for the document | [optional] 

## Example

```python
from grist_client.models.create_doc_unified_request import CreateDocUnifiedRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateDocUnifiedRequest from a JSON string
create_doc_unified_request_instance = CreateDocUnifiedRequest.from_json(json)
# print the JSON string representation of the object
print(CreateDocUnifiedRequest.to_json())

# convert the object into a dict
create_doc_unified_request_dict = create_doc_unified_request_instance.to_dict()
# create an instance of CreateDocUnifiedRequest from a dict
create_doc_unified_request_from_dict = CreateDocUnifiedRequest.from_dict(create_doc_unified_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


