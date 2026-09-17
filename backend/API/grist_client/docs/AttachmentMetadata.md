# AttachmentMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file_name** | **str** |  | [optional] 
**file_size** | **float** |  | [optional] 
**time_uploaded** | **str** |  | [optional] 

## Example

```python
from grist_client.models.attachment_metadata import AttachmentMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of AttachmentMetadata from a JSON string
attachment_metadata_instance = AttachmentMetadata.from_json(json)
# print the JSON string representation of the object
print(AttachmentMetadata.to_json())

# convert the object into a dict
attachment_metadata_dict = attachment_metadata_instance.to_dict()
# create an instance of AttachmentMetadata from a dict
attachment_metadata_from_dict = AttachmentMetadata.from_dict(attachment_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


