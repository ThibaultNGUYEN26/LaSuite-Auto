# PaginatedInvitationList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | 
**next** | **str** |  | [optional] 
**previous** | **str** |  | [optional] 
**results** | [**List[Invitation]**](Invitation.md) |  | 

## Example

```python
from openapi_client.models.paginated_invitation_list import PaginatedInvitationList

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedInvitationList from a JSON string
paginated_invitation_list_instance = PaginatedInvitationList.from_json(json)
# print the JSON string representation of the object
print(PaginatedInvitationList.to_json())

# convert the object into a dict
paginated_invitation_list_dict = paginated_invitation_list_instance.to_dict()
# create an instance of PaginatedInvitationList from a dict
paginated_invitation_list_from_dict = PaginatedInvitationList.from_dict(paginated_invitation_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


