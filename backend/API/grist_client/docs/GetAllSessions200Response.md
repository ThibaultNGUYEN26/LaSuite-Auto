# GetAllSessions200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**users** | [**List[User]**](User.md) |  | [optional] 
**orgs** | [**List[Org]**](Org.md) |  | [optional] 

## Example

```python
from grist_client.models.get_all_sessions200_response import GetAllSessions200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetAllSessions200Response from a JSON string
get_all_sessions200_response_instance = GetAllSessions200Response.from_json(json)
# print the JSON string representation of the object
print(GetAllSessions200Response.to_json())

# convert the object into a dict
get_all_sessions200_response_dict = get_all_sessions200_response_instance.to_dict()
# create an instance of GetAllSessions200Response from a dict
get_all_sessions200_response_from_dict = GetAllSessions200Response.from_dict(get_all_sessions200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


