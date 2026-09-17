# UpdateTablesTablesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Current table identifier | 
**fields** | [**UpdateTablesTablesInnerFields**](UpdateTablesTablesInnerFields.md) |  | 

## Example

```python
from grist_client.models.update_tables_tables_inner import UpdateTablesTablesInner

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateTablesTablesInner from a JSON string
update_tables_tables_inner_instance = UpdateTablesTablesInner.from_json(json)
# print the JSON string representation of the object
print(UpdateTablesTablesInner.to_json())

# convert the object into a dict
update_tables_tables_inner_dict = update_tables_tables_inner_instance.to_dict()
# create an instance of UpdateTablesTablesInner from a dict
update_tables_tables_inner_from_dict = UpdateTablesTablesInner.from_dict(update_tables_tables_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


