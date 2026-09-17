# UpdateUserLocaleRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**locale** | **str** | Locale code (e.g. &#39;en-US&#39;, &#39;fr&#39;). Set to null to clear. | [optional] 

## Example

```python
from grist_client.models.update_user_locale_request import UpdateUserLocaleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateUserLocaleRequest from a JSON string
update_user_locale_request_instance = UpdateUserLocaleRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateUserLocaleRequest.to_json())

# convert the object into a dict
update_user_locale_request_dict = update_user_locale_request_instance.to_dict()
# create an instance of UpdateUserLocaleRequest from a dict
update_user_locale_request_from_dict = UpdateUserLocaleRequest.from_dict(update_user_locale_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


