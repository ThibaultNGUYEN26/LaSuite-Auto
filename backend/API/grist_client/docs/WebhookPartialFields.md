# WebhookPartialFields


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**memo** | **str** |  | [optional] 
**url** | **str** |  | [optional] 
**enabled** | **bool** |  | [optional] 
**event_types** | **List[str]** |  | [optional] 
**is_ready_column** | **str** |  | [optional] 
**table_id** | **str** |  | [optional] 

## Example

```python
from grist_client.models.webhook_partial_fields import WebhookPartialFields

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookPartialFields from a JSON string
webhook_partial_fields_instance = WebhookPartialFields.from_json(json)
# print the JSON string representation of the object
print(WebhookPartialFields.to_json())

# convert the object into a dict
webhook_partial_fields_dict = webhook_partial_fields_instance.to_dict()
# create an instance of WebhookPartialFields from a dict
webhook_partial_fields_from_dict = WebhookPartialFields.from_dict(webhook_partial_fields_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


