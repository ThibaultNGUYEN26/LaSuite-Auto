# PatchedInvitationRequest

Serialize invitations.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** |  | [optional] 
**role** | [**RoleEnum**](RoleEnum.md) |  | [optional] 

## Example

```python
from openapi_client.models.patched_invitation_request import PatchedInvitationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedInvitationRequest from a JSON string
patched_invitation_request_instance = PatchedInvitationRequest.from_json(json)
# print the JSON string representation of the object
print(PatchedInvitationRequest.to_json())

# convert the object into a dict
patched_invitation_request_dict = patched_invitation_request_instance.to_dict()
# create an instance of PatchedInvitationRequest from a dict
patched_invitation_request_from_dict = PatchedInvitationRequest.from_dict(patched_invitation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


