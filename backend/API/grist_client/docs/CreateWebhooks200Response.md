# CreateWebhooks200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**webhooks** | [**List[WebhookId]**](WebhookId.md) |  | 

## Example

```python
from grist_client.models.create_webhooks200_response import CreateWebhooks200Response

# TODO update the JSON string below
json = "{}"
# create an instance of CreateWebhooks200Response from a JSON string
create_webhooks200_response_instance = CreateWebhooks200Response.from_json(json)
# print the JSON string representation of the object
print(CreateWebhooks200Response.to_json())

# convert the object into a dict
create_webhooks200_response_dict = create_webhooks200_response_instance.to_dict()
# create an instance of CreateWebhooks200Response from a dict
create_webhooks200_response_from_dict = CreateWebhooks200Response.from_dict(create_webhooks200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


