# AttachmentMetadataList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**records** | [**List[AttachmentMetadataListRecordsInner]**](AttachmentMetadataListRecordsInner.md) |  | 

## Example

```python
from grist_client.models.attachment_metadata_list import AttachmentMetadataList

# TODO update the JSON string below
json = "{}"
# create an instance of AttachmentMetadataList from a JSON string
attachment_metadata_list_instance = AttachmentMetadataList.from_json(json)
# print the JSON string representation of the object
print(AttachmentMetadataList.to_json())

# convert the object into a dict
attachment_metadata_list_dict = attachment_metadata_list_instance.to_dict()
# create an instance of AttachmentMetadataList from a dict
attachment_metadata_list_from_dict = AttachmentMetadataList.from_dict(attachment_metadata_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


