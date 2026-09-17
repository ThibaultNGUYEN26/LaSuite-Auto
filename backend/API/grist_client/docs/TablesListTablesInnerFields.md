# TablesListTablesInnerFields


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**table_ref** | **int** | Row ID of the table in the _grist_Tables metadata table | [optional] 
**on_demand** | **bool** | Whether the table uses on-demand loading | [optional] 

## Example

```python
from grist_client.models.tables_list_tables_inner_fields import TablesListTablesInnerFields

# TODO update the JSON string below
json = "{}"
# create an instance of TablesListTablesInnerFields from a JSON string
tables_list_tables_inner_fields_instance = TablesListTablesInnerFields.from_json(json)
# print the JSON string representation of the object
print(TablesListTablesInnerFields.to_json())

# convert the object into a dict
tables_list_tables_inner_fields_dict = tables_list_tables_inner_fields_instance.to_dict()
# create an instance of TablesListTablesInnerFields from a dict
tables_list_tables_inner_fields_from_dict = TablesListTablesInnerFields.from_dict(tables_list_tables_inner_fields_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


