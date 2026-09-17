# WebhookFields


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**memo** | **str** |  | 
**url** | **str** |  | 
**enabled** | **bool** |  | 
**event_types** | **List[str]** |  | 
**is_ready_column** | **str** |  | 
**table_id** | **str** |  | 
**unsubscribe_key** | **str** |  | 

## Example

```python
from grist_client.models.webhook_fields import WebhookFields

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookFields from a JSON string
webhook_fields_instance = WebhookFields.from_json(json)
# print the JSON string representation of the object
print(WebhookFields.to_json())

# convert the object into a dict
webhook_fields_dict = webhook_fields_instance.to_dict()
# create an instance of WebhookFields from a dict
webhook_fields_from_dict = WebhookFields.from_dict(webhook_fields_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


