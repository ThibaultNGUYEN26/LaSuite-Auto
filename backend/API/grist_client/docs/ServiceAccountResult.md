# ServiceAccountResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **float** |  | 
**login** | **str** |  | 
**label** | **str** |  | 
**description** | **str** |  | 
**expires_at** | **datetime** |  | 
**has_valid_key** | **bool** |  | 

## Example

```python
from grist_client.models.service_account_result import ServiceAccountResult

# TODO update the JSON string below
json = "{}"
# create an instance of ServiceAccountResult from a JSON string
service_account_result_instance = ServiceAccountResult.from_json(json)
# print the JSON string representation of the object
print(ServiceAccountResult.to_json())

# convert the object into a dict
service_account_result_dict = service_account_result_instance.to_dict()
# create an instance of ServiceAccountResult from a dict
service_account_result_from_dict = ServiceAccountResult.from_dict(service_account_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


