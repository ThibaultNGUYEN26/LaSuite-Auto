# WebhookProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**size** | **float** |  | [optional] 
**attempts** | **float** |  | [optional] 
**error_message** | **str** |  | [optional] 
**http_status** | **float** |  | [optional] 
**status** | **str** |  | [optional] 

## Example

```python
from grist_client.models.webhook_properties import WebhookProperties

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookProperties from a JSON string
webhook_properties_instance = WebhookProperties.from_json(json)
# print the JSON string representation of the object
print(WebhookProperties.to_json())

# convert the object into a dict
webhook_properties_dict = webhook_properties_instance.to_dict()
# create an instance of WebhookProperties from a dict
webhook_properties_from_dict = WebhookProperties.from_dict(webhook_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


