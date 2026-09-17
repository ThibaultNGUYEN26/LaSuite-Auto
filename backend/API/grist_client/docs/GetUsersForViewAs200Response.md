# GetUsersForViewAs200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**users** | [**List[User]**](User.md) | Users the document is shared with | [optional] 
**attribute_table_users** | [**List[User]**](User.md) | Users found in user attribute tables | [optional] 
**example_users** | [**List[User]**](User.md) | Predefined example users | [optional] 

## Example

```python
from grist_client.models.get_users_for_view_as200_response import GetUsersForViewAs200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetUsersForViewAs200Response from a JSON string
get_users_for_view_as200_response_instance = GetUsersForViewAs200Response.from_json(json)
# print the JSON string representation of the object
print(GetUsersForViewAs200Response.to_json())

# convert the object into a dict
get_users_for_view_as200_response_dict = get_users_for_view_as200_response_instance.to_dict()
# create an instance of GetUsersForViewAs200Response from a dict
get_users_for_view_as200_response_from_dict = GetUsersForViewAs200Response.from_dict(get_users_for_view_as200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


