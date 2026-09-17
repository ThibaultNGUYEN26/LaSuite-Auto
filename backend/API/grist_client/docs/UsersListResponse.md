# UsersListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**total_results** | **int** | Total number of users. | [optional] 
**items_per_page** | **int** | Number of users returned per page. | [optional] 
**start_index** | **int** | Starting index. | [optional] 
**resources** | [**List[UserInResponse]**](UserInResponse.md) |  | [optional] 

## Example

```python
from grist_client.models.users_list_response import UsersListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UsersListResponse from a JSON string
users_list_response_instance = UsersListResponse.from_json(json)
# print the JSON string representation of the object
print(UsersListResponse.to_json())

# convert the object into a dict
users_list_response_dict = users_list_response_instance.to_dict()
# create an instance of UsersListResponse from a dict
users_list_response_from_dict = UsersListResponse.from_dict(users_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


