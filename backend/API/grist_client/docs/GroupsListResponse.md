# GroupsListResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**total_results** | **int** | Total number of groups. | [optional] 
**items_per_page** | **int** | Number of groups returned per page. | [optional] 
**start_index** | **int** | Starting index. | [optional] 
**resources** | [**List[GroupInResponse]**](GroupInResponse.md) |  | [optional] 

## Example

```python
from grist_client.models.groups_list_response import GroupsListResponse

# TODO update the JSON string below
json = "{}"
# create an instance of GroupsListResponse from a JSON string
groups_list_response_instance = GroupsListResponse.from_json(json)
# print the JSON string representation of the object
print(GroupsListResponse.to_json())

# convert the object into a dict
groups_list_response_dict = groups_list_response_instance.to_dict()
# create an instance of GroupsListResponse from a dict
groups_list_response_from_dict = GroupsListResponse.from_dict(groups_list_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


