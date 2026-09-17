# WebhookBatchStatus


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**size** | **float** |  | 
**attempts** | **float** |  | 
**error_message** | **str** |  | [optional] 
**http_status** | **float** |  | [optional] 
**status** | **str** |  | 

## Example

```python
from grist_client.models.webhook_batch_status import WebhookBatchStatus

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookBatchStatus from a JSON string
webhook_batch_status_instance = WebhookBatchStatus.from_json(json)
# print the JSON string representation of the object
print(WebhookBatchStatus.to_json())

# convert the object into a dict
webhook_batch_status_dict = webhook_batch_status_instance.to_dict()
# create an instance of WebhookBatchStatus from a dict
webhook_batch_status_from_dict = WebhookBatchStatus.from_dict(webhook_batch_status_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


