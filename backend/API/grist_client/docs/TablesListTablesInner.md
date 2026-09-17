# TablesListTablesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**fields** | [**TablesListTablesInnerFields**](TablesListTablesInnerFields.md) |  | 
**columns** | [**List[TablesListTablesInnerColumnsInner]**](TablesListTablesInnerColumnsInner.md) | Included when expand&#x3D;column is set. Contains metadata for each column in the table. | [optional] 

## Example

```python
from grist_client.models.tables_list_tables_inner import TablesListTablesInner

# TODO update the JSON string below
json = "{}"
# create an instance of TablesListTablesInner from a JSON string
tables_list_tables_inner_instance = TablesListTablesInner.from_json(json)
# print the JSON string representation of the object
print(TablesListTablesInner.to_json())

# convert the object into a dict
tables_list_tables_inner_dict = tables_list_tables_inner_instance.to_dict()
# create an instance of TablesListTablesInner from a dict
tables_list_tables_inner_from_dict = TablesListTablesInner.from_dict(tables_list_tables_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


