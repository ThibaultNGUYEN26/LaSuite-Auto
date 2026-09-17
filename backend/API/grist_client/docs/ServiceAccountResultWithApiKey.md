# ServiceAccountResultWithApiKey


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **float** |  | 
**login** | **str** |  | 
**label** | **str** |  | 
**description** | **str** |  | 
**expires_at** | **datetime** |  | 
**has_valid_key** | **bool** |  | 
**key** | **str** |  | [optional] 

## Example

```python
from grist_client.models.service_account_result_with_api_key import ServiceAccountResultWithApiKey

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceAccountResultWithApiKey from a JSON string
service_account_result_with_api_key_instance = ServiceAccountResultWithApiKey.from_json(json)
# print the JSON string representation of the object
print(ServiceAccountResultWithApiKey.to_json())

# convert the object into a dict
service_account_result_with_api_key_dict = service_account_result_with_api_key_instance.to_dict()
# create an instance of ServiceAccountResultWithApiKey from a dict
service_account_result_with_api_key_from_dict = ServiceAccountResultWithApiKey.from_dict(service_account_result_with_api_key_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


