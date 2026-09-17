# AttachmentsTransferStatus


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**AttachmentsTransferStatusStatus**](AttachmentsTransferStatusStatus.md) |  | [optional] 
**location_summary** | [**DocumentAttachmentsLocation**](DocumentAttachmentsLocation.md) |  | [optional] 

## Example

```python
from grist_client.models.attachments_transfer_status import AttachmentsTransferStatus

# TODO update the JSON string below
json = "{}"
# create an instance of AttachmentsTransferStatus from a JSON string
attachments_transfer_status_instance = AttachmentsTransferStatus.from_json(json)
# print the JSON string representation of the object
print(AttachmentsTransferStatus.to_json())

# convert the object into a dict
attachments_transfer_status_dict = attachments_transfer_status_instance.to_dict()
# create an instance of AttachmentsTransferStatus from a dict
attachments_transfer_status_from_dict = AttachmentsTransferStatus.from_dict(attachments_transfer_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


