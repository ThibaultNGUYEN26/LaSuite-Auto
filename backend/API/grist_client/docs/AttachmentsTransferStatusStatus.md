# AttachmentsTransferStatusStatus


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**pending_transfer_count** | **int** | Remaining transfers be performed | [optional] 
**is_running** | **bool** | Are files actively being transferred? | [optional] 

## Example

```python
from grist_client.models.attachments_transfer_status_status import AttachmentsTransferStatusStatus

# TODO update the JSON string below
json = "{}"
# create an instance of AttachmentsTransferStatusStatus from a JSON string
attachments_transfer_status_status_instance = AttachmentsTransferStatusStatus.from_json(json)
# print the JSON string representation of the object
print(AttachmentsTransferStatusStatus.to_json())

# convert the object into a dict
attachments_transfer_status_status_dict = attachments_transfer_status_status_instance.to_dict()
# create an instance of AttachmentsTransferStatusStatus from a dict
attachments_transfer_status_status_from_dict = AttachmentsTransferStatusStatus.from_dict(attachments_transfer_status_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


