# CreateItem

Serializer used to create a new item

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **UUID** | primary key for the record as UUID | [optional] 
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
**nb_accesses** | **int** |  | [readonly] 
**numchild** | **str** |  | [readonly] 
**numchild_folder** | **str** |  | [readonly] 
**path** | **str** |  | [readonly] 
**title** | **str** |  | [optional] 
**updated_at** | **datetime** | date and time at which a record was last updated | [readonly] 
**user_role** | **str** |  | [readonly] 
**type** | [**TypeEnum**](TypeEnum.md) |  | [optional] 
**upload_state** | **str** |  | [readonly] 
**url** | **str** |  | [readonly] 
**url_permalink** | **str** |  | [readonly] 
**filename** | **str** |  | [optional] 
**policy** | **str** |  | [readonly] 
**main_workspace** | **bool** |  | [readonly] 
**size** | **int** |  | [readonly] 
**description** | **str** |  | [optional] 
**hard_delete_at** | **str** |  | [readonly] 

## Example

```python
from openapi_client.models.create_item import CreateItem

# TODO update the JSON string below
json = "{}"
# create an instance of CreateItem from a JSON string
create_item_instance = CreateItem.from_json(json)
# print the JSON string representation of the object
print(CreateItem.to_json())

# convert the object into a dict
create_item_dict = create_item_instance.to_dict()
# create an instance of CreateItem from a dict
create_item_from_dict = CreateItem.from_dict(create_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


