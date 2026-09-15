# UserRequest

Serialize users.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**language** | **str** | The language in which the user wants to see the interface.  * &#x60;en-us&#x60; - English * &#x60;fr-fr&#x60; - French * &#x60;de-de&#x60; - German * &#x60;nl-nl&#x60; - Dutch | [optional] 
**last_release_note_seen** | **str** |  | [optional] 
**column_preferences** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.user_request import UserRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UserRequest from a JSON string
user_request_instance = UserRequest.from_json(json)
# print the JSON string representation of the object
print(UserRequest.to_json())

# convert the object into a dict
user_request_dict = user_request_instance.to_dict()
# create an instance of UserRequest from a dict
user_request_from_dict = UserRequest.from_dict(user_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


