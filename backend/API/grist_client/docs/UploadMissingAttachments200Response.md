# UploadMissingAttachments200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**added** | **int** | Total files added to external storage. | [optional] 
**errored** | **int** | Total files that errored when attempting to process them. | [optional] 
**unused** | **int** | Total files that aren&#39;t needed, or don&#39;t match an existing attachment. | [optional] 

## Example

```python
from grist_client.models.upload_missing_attachments200_response import UploadMissingAttachments200Response

# TODO update the JSON string below
json = "{}"
# create an instance of UploadMissingAttachments200Response from a JSON string
upload_missing_attachments200_response_instance = UploadMissingAttachments200Response.from_json(json)
# print the JSON string representation of the object
print(UploadMissingAttachments200Response.to_json())

# convert the object into a dict
upload_missing_attachments200_response_dict = upload_missing_attachments200_response_instance.to_dict()
# create an instance of UploadMissingAttachments200Response from a dict
upload_missing_attachments200_response_from_dict = UploadMissingAttachments200Response.from_dict(upload_missing_attachments200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


