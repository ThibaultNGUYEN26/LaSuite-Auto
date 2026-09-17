# SearchUsersRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**filter** | **object** |  | [optional] 
**sort_by** | **object** |  | [optional] 
**sort_order** | **str** | Order of sorting (ascending or descending). | [optional] 
**attributes** | **object** |  | [optional] 
**excluded_attributes** | **object** |  | [optional] 
**start_index** | **int** | The starting index for pagination. | [optional] 
**count** | **int** | The number of resources to retrieve. | [optional] 

## Example

```python
from grist_client.models.search_users_request import SearchUsersRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SearchUsersRequest from a JSON string
search_users_request_instance = SearchUsersRequest.from_json(json)
# print the JSON string representation of the object
print(SearchUsersRequest.to_json())

# convert the object into a dict
search_users_request_dict = search_users_request_instance.to_dict()
# create an instance of SearchUsersRequest from a dict
search_users_request_from_dict = SearchUsersRequest.from_dict(search_users_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


