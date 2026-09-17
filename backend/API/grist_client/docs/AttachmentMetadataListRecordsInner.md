# AttachmentMetadataListRecordsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **float** |  | 
**fields** | [**AttachmentMetadata**](AttachmentMetadata.md) |  | 

## Example

```python
from grist_client.models.attachment_metadata_list_records_inner import AttachmentMetadataListRecordsInner

# TODO update the JSON string below
json = "{}"
# create an instance of AttachmentMetadataListRecordsInner from a JSON string
attachment_metadata_list_records_inner_instance = AttachmentMetadataListRecordsInner.from_json(json)
# print the JSON string representation of the object
print(AttachmentMetadataListRecordsInner.to_json())

# convert the object into a dict
attachment_metadata_list_records_inner_dict = attachment_metadata_list_records_inner_instance.to_dict()
# create an instance of AttachmentMetadataListRecordsInner from a dict
attachment_metadata_list_records_inner_from_dict = AttachmentMetadataListRecordsInner.from_dict(attachment_metadata_list_records_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


