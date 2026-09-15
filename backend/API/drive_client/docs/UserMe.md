# UserMe

Serialize users for me endpoint.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** | primary key for the record as UUID | [readonly] 
**email** | **str** |  | [readonly] 
**full_name** | **str** |  | [readonly] 
**short_name** | **str** |  | [readonly] 
**language** | **str** | The language in which the user wants to see the interface.  * &#x60;en-us&#x60; - English * &#x60;fr-fr&#x60; - French * &#x60;de-de&#x60; - German * &#x60;nl-nl&#x60; - Dutch | [optional] 
**last_release_note_seen** | **str** |  | [optional] 
**column_preferences** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.user_me import UserMe

# TODO update the JSON string below
json = "{}"
# create an instance of UserMe from a JSON string
user_me_instance = UserMe.from_json(json)
# print the JSON string representation of the object
print(UserMe.to_json())

# convert the object into a dict
user_me_dict = user_me_instance.to_dict()
# create an instance of UserMe from a dict
user_me_from_dict = UserMe.from_dict(user_me_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


