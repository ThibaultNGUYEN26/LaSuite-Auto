# InvitationRequest

Serialize invitations.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** |  | 
**role** | [**RoleEnum**](RoleEnum.md) |  | [optional] 

## Example

```python
from openapi_client.models.invitation_request import InvitationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of InvitationRequest from a JSON string
invitation_request_instance = InvitationRequest.from_json(json)
# print the JSON string representation of the object
print(InvitationRequest.to_json())

# convert the object into a dict
invitation_request_dict = invitation_request_instance.to_dict()
# create an instance of InvitationRequest from a dict
invitation_request_from_dict = InvitationRequest.from_dict(invitation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


