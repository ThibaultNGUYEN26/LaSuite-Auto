# CreateWebhooksRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**webhooks** | [**List[CreateWebhooksRequestWebhooksInner]**](CreateWebhooksRequestWebhooksInner.md) |  | 

## Example

```python
from grist_client.models.create_webhooks_request import CreateWebhooksRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateWebhooksRequest from a JSON string
create_webhooks_request_instance = CreateWebhooksRequest.from_json(json)
# print the JSON string representation of the object
print(CreateWebhooksRequest.to_json())

# convert the object into a dict
create_webhooks_request_dict = create_webhooks_request_instance.to_dict()
# create an instance of CreateWebhooksRequest from a dict
create_webhooks_request_from_dict = CreateWebhooksRequest.from_dict(create_webhooks_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


