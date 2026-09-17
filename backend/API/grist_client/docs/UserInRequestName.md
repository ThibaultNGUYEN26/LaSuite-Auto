# UserInRequestName


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**formatted** | **str** | Full name of the user. | [optional] 

## Example

```python
from grist_client.models.user_in_request_name import UserInRequestName

# TODO update the JSON string below
json = "{}"
# create an instance of UserInRequestName from a JSON string
user_in_request_name_instance = UserInRequestName.from_json(json)
# print the JSON string representation of the object
print(UserInRequestName.to_json())

# convert the object into a dict
user_in_request_name_dict = user_in_request_name_instance.to_dict()
# create an instance of UserInRequestName from a dict
user_in_request_name_from_dict = UserInRequestName.from_dict(user_in_request_name_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


