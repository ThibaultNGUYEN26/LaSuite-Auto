# GetStates200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**states** | [**List[GetStates200ResponseStatesInner]**](GetStates200ResponseStatesInner.md) |  | 

## Example

```python
from grist_client.models.get_states200_response import GetStates200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetStates200Response from a JSON string
get_states200_response_instance = GetStates200Response.from_json(json)
# print the JSON string representation of the object
print(GetStates200Response.to_json())

# convert the object into a dict
get_states200_response_dict = get_states200_response_instance.to_dict()
# create an instance of GetStates200Response from a dict
get_states200_response_from_dict = GetStates200Response.from_dict(get_states200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


