# RecoverDoc200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**recovery_mode** | **bool** | The current recovery mode state of the document | 

## Example

```python
from grist_client.models.recover_doc200_response import RecoverDoc200Response

# TODO update the JSON string below
json = "{}"
# create an instance of RecoverDoc200Response from a JSON string
recover_doc200_response_instance = RecoverDoc200Response.from_json(json)
# print the JSON string representation of the object
print(RecoverDoc200Response.to_json())

# convert the object into a dict
recover_doc200_response_dict = recover_doc200_response_instance.to_dict()
# create an instance of RecoverDoc200Response from a dict
recover_doc200_response_from_dict = RecoverDoc200Response.from_dict(recover_doc200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


