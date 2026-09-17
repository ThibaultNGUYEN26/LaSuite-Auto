# SearchGroups200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**total_results** | **int** | Total number of groups found. | [optional] 
**resources** | [**List[GroupInResponse]**](GroupInResponse.md) |  | [optional] 

## Example

```python
from grist_client.models.search_groups200_response import SearchGroups200Response

# TODO update the JSON string below
json = "{}"
# create an instance of SearchGroups200Response from a JSON string
search_groups200_response_instance = SearchGroups200Response.from_json(json)
# print the JSON string representation of the object
print(SearchGroups200Response.to_json())

# convert the object into a dict
search_groups200_response_dict = search_groups200_response_instance.to_dict()
# create an instance of SearchGroups200Response from a dict
search_groups200_response_from_dict = SearchGroups200Response.from_dict(search_groups200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


