# WebhookRequiredFields


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**unsubscribe_key** | **str** |  | 

## Example

```python
from grist_client.models.webhook_required_fields import WebhookRequiredFields

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookRequiredFields from a JSON string
webhook_required_fields_instance = WebhookRequiredFields.from_json(json)
# print the JSON string representation of the object
print(WebhookRequiredFields.to_json())

# convert the object into a dict
webhook_required_fields_dict = webhook_required_fields_instance.to_dict()
# create an instance of WebhookRequiredFields from a dict
webhook_required_fields_from_dict = WebhookRequiredFields.from_dict(webhook_required_fields_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


