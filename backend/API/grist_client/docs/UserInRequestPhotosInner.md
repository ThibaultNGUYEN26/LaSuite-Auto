# UserInRequestPhotosInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **str** | The picture of the user | [optional] 
**primary** | **bool** | Whether this is the primary picture | [optional] 
**type** | **str** | The picture type. Currently, we only offer pictures of type \&quot;photo\&quot;. | [optional] 

## Example

```python
from grist_client.models.user_in_request_photos_inner import UserInRequestPhotosInner

# TODO update the JSON string below
json = "{}"
# create an instance of UserInRequestPhotosInner from a JSON string
user_in_request_photos_inner_instance = UserInRequestPhotosInner.from_json(json)
# print the JSON string representation of the object
print(UserInRequestPhotosInner.to_json())

# convert the object into a dict
user_in_request_photos_inner_dict = user_in_request_photos_inner_instance.to_dict()
# create an instance of UserInRequestPhotosInner from a dict
user_in_request_photos_inner_from_dict = UserInRequestPhotosInner.from_dict(user_in_request_photos_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


