# GetStates200ResponseStatesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**n** | **int** | Sequential action number | 
**h** | **str** | Hash identifier for this state | 

## Example

```python
from grist_client.models.get_states200_response_states_inner import GetStates200ResponseStatesInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetStates200ResponseStatesInner from a JSON string
get_states200_response_states_inner_instance = GetStates200ResponseStatesInner.from_json(json)
# print the JSON string representation of the object
print(GetStates200ResponseStatesInner.to_json())

# convert the object into a dict
get_states200_response_states_inner_dict = get_states200_response_states_inner_instance.to_dict()
# create an instance of GetStates200ResponseStatesInner from a dict
get_states200_response_states_inner_from_dict = GetStates200ResponseStatesInner.from_dict(get_states200_response_states_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


