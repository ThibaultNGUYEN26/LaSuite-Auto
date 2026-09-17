# PostSearch


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schemas** | **List[str]** |  | [optional] 
**filter** | **str** | Filter expression for resources. | [optional] 
**sort_by** | **str** | Field to sort by. | [optional] 
**sort_order** | **str** | Order of sorting (ascending or descending). | [optional] 
**attributes** | **List[str]** | A multi-valued list of strings indicating the names of resource attributes to return in the response. | [optional] 
**excluded_attributes** | **List[str]** | A multi-valued list of strings indicating the names of resource attributes to be removed from the default set of attributes to return. | [optional] 
**start_index** | **int** | The starting index for pagination. | [optional] 
**count** | **int** | The number of resources to retrieve. | [optional] 

## Example

```python
from grist_client.models.post_search import PostSearch

# TODO update the JSON string below
json = "{}"
# create an instance of PostSearch from a JSON string
post_search_instance = PostSearch.from_json(json)
# print the JSON string representation of the object
print(PostSearch.to_json())

# convert the object into a dict
post_search_dict = post_search_instance.to_dict()
# create an instance of PostSearch from a dict
post_search_from_dict = PostSearch.from_dict(post_search_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


