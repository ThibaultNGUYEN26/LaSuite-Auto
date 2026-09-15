# UserLight

Serialize users with limited fields.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** | primary key for the record as UUID | [readonly] 
**full_name** | **str** |  | [readonly] 
**short_name** | **str** |  | [readonly] 

## Example

```python
from openapi_client.models.user_light import UserLight

# TODO update the JSON string below
json = "{}"
# create an instance of UserLight from a JSON string
user_light_instance = UserLight.from_json(json)
# print the JSON string representation of the object
print(UserLight.to_json())

# convert the object into a dict
user_light_dict = user_light_instance.to_dict()
# create an instance of UserLight from a dict
user_light_from_dict = UserLight.from_dict(user_light_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


