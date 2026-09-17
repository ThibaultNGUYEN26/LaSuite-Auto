# SearchGroupsRequest


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
from grist_client.models.search_groups_request import SearchGroupsRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SearchGroupsRequest from a JSON string
search_groups_request_instance = SearchGroupsRequest.from_json(json)
# print the JSON string representation of the object
print(SearchGroupsRequest.to_json())

# convert the object into a dict
search_groups_request_dict = search_groups_request_instance.to_dict()
# create an instance of SearchGroupsRequest from a dict
search_groups_request_from_dict = SearchGroupsRequest.from_dict(search_groups_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


