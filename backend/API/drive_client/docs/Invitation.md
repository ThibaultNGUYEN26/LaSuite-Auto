# Invitation

Serialize invitations.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** | primary key for the record as UUID | [readonly] 
**abilities** | **Dict[str, object]** | Return abilities of the logged-in user on the instance. | [readonly] 
**created_at** | **datetime** | date and time at which a record was created | [readonly] 
**email** | **str** |  | 
**item** | **UUID** | primary key for the record as UUID | [readonly] 
**role** | [**RoleEnum**](RoleEnum.md) |  | [optional] 
**issuer** | **UUID** | primary key for the record as UUID | [readonly] 
**is_expired** | **str** |  | [readonly] 

## Example

```python
from openapi_client.models.invitation import Invitation

# TODO update the JSON string below
json = "{}"
# create an instance of Invitation from a JSON string
invitation_instance = Invitation.from_json(json)
# print the JSON string representation of the object
print(Invitation.to_json())

# convert the object into a dict
invitation_dict = invitation_instance.to_dict()
# create an instance of Invitation from a dict
invitation_from_dict = Invitation.from_dict(invitation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


