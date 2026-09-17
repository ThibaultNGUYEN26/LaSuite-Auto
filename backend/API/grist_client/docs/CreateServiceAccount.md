# CreateServiceAccount


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** | The service account&#39;s display name | [optional] 
**description** | **str** | Description of service account&#39;s purpose | [optional] 
**expires_at** | **str** | The service account&#39;s expiration date | 

## Example

```python
from grist_client.models.create_service_account import CreateServiceAccount

# TODO update the JSON string below
json = "{}"
# create an instance of CreateServiceAccount from a JSON string
create_service_account_instance = CreateServiceAccount.from_json(json)
# print the JSON string representation of the object
print(CreateServiceAccount.to_json())

# convert the object into a dict
create_service_account_dict = create_service_account_instance.to_dict()
# create an instance of CreateServiceAccount from a dict
create_service_account_from_dict = CreateServiceAccount.from_dict(create_service_account_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


