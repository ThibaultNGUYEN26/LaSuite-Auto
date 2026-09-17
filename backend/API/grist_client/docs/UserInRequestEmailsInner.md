# UserInRequestEmailsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value** | **str** | The user&#39;s email address. | [optional] 
**primary** | **bool** | Whether this is the primary email. | [optional] 

## Example

```python
from grist_client.models.user_in_request_emails_inner import UserInRequestEmailsInner

# TODO update the JSON string below
json = "{}"
# create an instance of UserInRequestEmailsInner from a JSON string
user_in_request_emails_inner_instance = UserInRequestEmailsInner.from_json(json)
# print the JSON string representation of the object
print(UserInRequestEmailsInner.to_json())

# convert the object into a dict
user_in_request_emails_inner_dict = user_in_request_emails_inner_instance.to_dict()
# create an instance of UserInRequestEmailsInner from a dict
user_in_request_emails_inner_from_dict = UserInRequestEmailsInner.from_dict(user_in_request_emails_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


