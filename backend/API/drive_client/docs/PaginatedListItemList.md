# PaginatedListItemList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | 
**next** | **str** |  | [optional] 
**previous** | **str** |  | [optional] 
**results** | [**List[ListItem]**](ListItem.md) |  | 

## Example

```python
from openapi_client.models.paginated_list_item_list import PaginatedListItemList

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedListItemList from a JSON string
paginated_list_item_list_instance = PaginatedListItemList.from_json(json)
# print the JSON string representation of the object
print(PaginatedListItemList.to_json())

# convert the object into a dict
paginated_list_item_list_dict = paginated_list_item_list_instance.to_dict()
# create an instance of PaginatedListItemList from a dict
paginated_list_item_list_from_dict = PaginatedListItemList.from_dict(paginated_list_item_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


