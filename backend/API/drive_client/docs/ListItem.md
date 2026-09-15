# ListItem

Serialize items with limited fields for display in lists.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** | primary key for the record as UUID | [readonly] 
**abilities** | **Dict[str, object]** | Return abilities of the logged-in user on the instance. | [readonly] 
**ancestors_link_reach** | **str** |  | [readonly] 
**ancestors_link_role** | **str** |  | [readonly] 
**computed_link_reach** | **str** |  | [readonly] 
**computed_link_role** | **str** |  | [readonly] 
**created_at** | **datetime** | date and time at which a record was created | [readonly] 
**creator** | [**UserLight**](UserLight.md) |  | [readonly] 
**depth** | **str** |  | [readonly] 
**is_favorite** | **bool** |  | [readonly] 
**link_role** | [**LinkRoleEnum**](LinkRoleEnum.md) |  | [readonly] 
**link_reach** | **str** |  | [readonly] 
**is_restricted** | **str** |  | [readonly] 
**nb_accesses** | **int** |  | [readonly] 
**numchild** | **str** |  | [readonly] 
**numchild_folder** | **str** |  | [readonly] 
**path** | **str** |  | [readonly] 
**target** | [**RestrictionTarget**](RestrictionTarget.md) |  | [readonly] 
**title** | **str** |  | 
**updated_at** | **datetime** | date and time at which a record was last updated | [readonly] 
**user_role** | **str** |  | [readonly] 
**type** | [**TypeEnum**](TypeEnum.md) |  | [readonly] 
**upload_state** | **str** |  | [readonly] 
**url** | **str** |  | [readonly] 
**url_permalink** | **str** |  | [readonly] 
**url_preview** | **str** |  | [readonly] 
**filename** | **str** |  | [optional] 
**mimetype** | **str** |  | [readonly] 
**main_workspace** | **bool** |  | [readonly] 
**size** | **int** |  | [readonly] 
**description** | **str** |  | [readonly] 
**deleted_at** | **datetime** |  | [readonly] 
**hard_delete_at** | **str** |  | [readonly] 
**is_wopi_supported** | **str** |  | [readonly] 

## Example

```python
from openapi_client.models.list_item import ListItem

# TODO update the JSON string below
json = "{}"
# create an instance of ListItem from a JSON string
list_item_instance = ListItem.from_json(json)
# print the JSON string representation of the object
print(ListItem.to_json())

# convert the object into a dict
list_item_dict = list_item_instance.to_dict()
# create an instance of ListItem from a dict
list_item_from_dict = ListItem.from_dict(list_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


