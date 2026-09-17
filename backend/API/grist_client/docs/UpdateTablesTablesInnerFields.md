# UpdateTablesTablesInnerFields


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**table_id** | **str** | Set to a new value to rename the table | [optional] 
**on_demand** | **bool** | Whether the table should use on-demand loading | [optional] 

## Example

```python
from grist_client.models.update_tables_tables_inner_fields import UpdateTablesTablesInnerFields

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateTablesTablesInnerFields from a JSON string
update_tables_tables_inner_fields_instance = UpdateTablesTablesInnerFields.from_json(json)
# print the JSON string representation of the object
print(UpdateTablesTablesInnerFields.to_json())

# convert the object into a dict
update_tables_tables_inner_fields_dict = update_tables_tables_inner_fields_instance.to_dict()
# create an instance of UpdateTablesTablesInnerFields from a dict
update_tables_tables_inner_fields_from_dict = UpdateTablesTablesInnerFields.from_dict(update_tables_tables_inner_fields_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


