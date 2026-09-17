# ServiceAccountBody


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** | The service account&#39;s display name | [optional] 
**description** | **str** | Description of service account&#39;s purpose | [optional] 
**expires_at** | **str** | The service account&#39;s expiration date | [optional] 

## Example

```python
from grist_client.models.service_account_body import ServiceAccountBody

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceAccountBody from a JSON string
service_account_body_instance = ServiceAccountBody.from_json(json)
# print the JSON string representation of the object
print(ServiceAccountBody.to_json())

# convert the object into a dict
service_account_body_dict = service_account_body_instance.to_dict()
# create an instance of ServiceAccountBody from a dict
service_account_body_from_dict = ServiceAccountBody.from_dict(service_account_body_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


