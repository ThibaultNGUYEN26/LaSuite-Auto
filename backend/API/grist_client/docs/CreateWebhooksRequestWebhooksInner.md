# CreateWebhooksRequestWebhooksInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fields** | [**WebhookPartialFields**](WebhookPartialFields.md) |  | 

## Example

```python
from grist_client.models.create_webhooks_request_webhooks_inner import CreateWebhooksRequestWebhooksInner

# TODO update the JSON string below
json = "{}"
# create an instance of CreateWebhooksRequestWebhooksInner from a JSON string
create_webhooks_request_webhooks_inner_instance = CreateWebhooksRequestWebhooksInner.from_json(json)
# print the JSON string representation of the object
print(CreateWebhooksRequestWebhooksInner.to_json())

# convert the object into a dict
create_webhooks_request_webhooks_inner_dict = create_webhooks_request_webhooks_inner_instance.to_dict()
# create an instance of CreateWebhooksRequestWebhooksInner from a dict
create_webhooks_request_webhooks_inner_from_dict = CreateWebhooksRequestWebhooksInner.from_dict(create_webhooks_request_webhooks_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


