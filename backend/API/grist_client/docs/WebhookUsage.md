# WebhookUsage


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**num_waiting** | **int** |  | 
**status** | **str** |  | 
**updated_time** | **float** |  | [optional] 
**last_success_time** | **float** |  | [optional] 
**last_failure_time** | **float** |  | [optional] 
**last_error_message** | **str** |  | [optional] 
**last_http_status** | **float** |  | [optional] 
**last_event_batch** | [**WebhookBatchStatus**](WebhookBatchStatus.md) |  | [optional] 

## Example

```python
from grist_client.models.webhook_usage import WebhookUsage

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookUsage from a JSON string
webhook_usage_instance = WebhookUsage.from_json(json)
# print the JSON string representation of the object
print(WebhookUsage.to_json())

# convert the object into a dict
webhook_usage_dict = webhook_usage_instance.to_dict()
# create an instance of WebhookUsage from a dict
webhook_usage_from_dict = WebhookUsage.from_dict(webhook_usage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


