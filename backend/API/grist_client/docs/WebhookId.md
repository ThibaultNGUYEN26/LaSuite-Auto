# WebhookId


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Webhook identifier | 

## Example

```python
from grist_client.models.webhook_id import WebhookId

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookId from a JSON string
webhook_id_instance = WebhookId.from_json(json)
# print the JSON string representation of the object
print(WebhookId.to_json())

# convert the object into a dict
webhook_id_dict = webhook_id_instance.to_dict()
# create an instance of WebhookId from a dict
webhook_id_from_dict = WebhookId.from_dict(webhook_id_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


