# RolesListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**total_results** | **int** | Total number of roles. | [optional] 
**items_per_page** | **int** | Number of roles returned per page. | [optional] 
**start_index** | **int** | Starting index. | [optional] 
**resources** | [**List[RoleInGetResponse]**](RoleInGetResponse.md) |  | [optional] 

## Example

```python
from grist_client.models.roles_list_response import RolesListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of RolesListResponse from a JSON string
roles_list_response_instance = RolesListResponse.from_json(json)
# print the JSON string representation of the object
print(RolesListResponse.to_json())

# convert the object into a dict
roles_list_response_dict = roles_list_response_instance.to_dict()
# create an instance of RolesListResponse from a dict
roles_list_response_from_dict = RolesListResponse.from_dict(roles_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


