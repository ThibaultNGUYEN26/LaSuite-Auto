# BatchShareResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**accesses_created** | **int** |  | 
**invitations_created** | **int** |  | 
**skipped** | **List[Dict[str, object]]** |  | 

## Example

```python
from openapi_client.models.batch_share_response import BatchShareResponse

# TODO update the JSON string below
json = "{}"
# create an instance of BatchShareResponse from a JSON string
batch_share_response_instance = BatchShareResponse.from_json(json)
# print the JSON string representation of the object
print(BatchShareResponse.to_json())

# convert the object into a dict
batch_share_response_dict = batch_share_response_instance.to_dict()
# create an instance of BatchShareResponse from a dict
batch_share_response_from_dict = BatchShareResponse.from_dict(batch_share_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


