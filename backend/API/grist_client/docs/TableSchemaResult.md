# TableSchemaResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | The ID (technical name) of the table | 
**title** | **str** | The human readable name of the table | 
**path** | **str** | The URL to download the CSV | [optional] 
**format** | **str** |  | [optional] 
**mediatype** | **str** |  | [optional] 
**encoding** | **str** |  | [optional] 
**dialect** | [**CsvDialect**](CsvDialect.md) |  | [optional] 
**var_schema** | [**TableSchema**](TableSchema.md) |  | 

## Example

```python
from grist_client.models.table_schema_result import TableSchemaResult

# TODO update the JSON string below
json = "{}"
# create an instance of TableSchemaResult from a JSON string
table_schema_result_instance = TableSchemaResult.from_json(json)
# print the JSON string representation of the object
print(TableSchemaResult.to_json())

# convert the object into a dict
table_schema_result_dict = table_schema_result_instance.to_dict()
# create an instance of TableSchemaResult from a dict
table_schema_result_from_dict = TableSchemaResult.from_dict(table_schema_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


