# UpdateUserNameRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | New display name | 

## Example

```python
from grist_client.models.update_user_name_request import UpdateUserNameRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUserNameRequest from a JSON string
update_user_name_request_instance = UpdateUserNameRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateUserNameRequest.to_json())

# convert the object into a dict
update_user_name_request_dict = update_user_name_request_instance.to_dict()
# create an instance of UpdateUserNameRequest from a dict
update_user_name_request_from_dict = UpdateUserNameRequest.from_dict(update_user_name_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


