# ApplyUserActions200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**action_num** | **int** | The action number assigned | [optional] 
**ret_values** | **List[object]** | Return values from each action (e.g. new row IDs) | [optional] 

## Example

```python
from grist_client.models.apply_user_actions200_response import ApplyUserActions200Response

# TODO update the JSON string below
json = "{}"
# create an instance of ApplyUserActions200Response from a JSON string
apply_user_actions200_response_instance = ApplyUserActions200Response.from_json(json)
# print the JSON string representation of the object
print(ApplyUserActions200Response.to_json())

# convert the object into a dict
apply_user_actions200_response_dict = apply_user_actions200_response_instance.to_dict()
# create an instance of ApplyUserActions200Response from a dict
apply_user_actions200_response_from_dict = ApplyUserActions200Response.from_dict(apply_user_actions200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


