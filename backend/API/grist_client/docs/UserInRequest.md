# UserInRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**user_name** | **str** | The unique username. | [optional] 
**name** | [**UserInRequestName**](UserInRequestName.md) |  | [optional] 
**emails** | [**List[UserInRequestEmailsInner]**](UserInRequestEmailsInner.md) |  | [optional] 
**display_name** | **str** | the display name of the user | [optional] 
**preferred_language** | **str** | Indicates the user&#39;s preferred written or spoken languages and is generally used for selecting a localized user interface. | [optional] 
**locale** | **str** | Used to indicate the User&#39;s default location for purposes of localizing such items as currency, date time format, or numerical representations. | [optional] 
**photos** | [**List[UserInRequestPhotosInner]**](UserInRequestPhotosInner.md) | The picture of the user. It is expected to have a single item in the context of Grist. | [optional] 

## Example

```python
from grist_client.models.user_in_request import UserInRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UserInRequest from a JSON string
user_in_request_instance = UserInRequest.from_json(json)
# print the JSON string representation of the object
print(UserInRequest.to_json())

# convert the object into a dict
user_in_request_dict = user_in_request_instance.to_dict()
# create an instance of UserInRequest from a dict
user_in_request_from_dict = UserInRequest.from_dict(user_in_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


