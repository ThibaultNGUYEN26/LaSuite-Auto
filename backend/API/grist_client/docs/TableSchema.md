# TableSchema

A Table Schema for this resource, compliant with the [Table Schema](/tableschema/) specification.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fields** | [**List[OneOfobjectobjectobjectobjectobjectobjectobjectobjectobjectobjectobjectobjectobjectobjectobject]**](OneOfobjectobjectobjectobjectobjectobjectobjectobjectobjectobjectobjectobjectobjectobjectobject.md) | An &#x60;array&#x60; of Table Schema Field objects. | 
**primary_key** | [**OneOfsetstring**](OneOfsetstring.md) | A primary key is a field name or an array of field names, whose values &#x60;MUST&#x60; uniquely identify each row in the table. | [optional] 
**foreign_keys** | [**List[OneOfobjectobject]**](OneOfobjectobject.md) |  | [optional] 
**missing_values** | **List[str]** | Values that when encountered in the source, should be considered as &#x60;null&#x60;, &#39;not present&#39;, or &#39;blank&#39; values. | [optional] [default to [""]]

## Example

```python
from grist_client.models.table_schema import TableSchema

# TODO update the JSON string below
json = "{}"
# create an instance of TableSchema from a JSON string
table_schema_instance = TableSchema.from_json(json)
# print the JSON string representation of the object
print(TableSchema.to_json())

# convert the object into a dict
table_schema_dict = table_schema_instance.to_dict()
# create an instance of TableSchema from a dict
table_schema_from_dict = TableSchema.from_dict(table_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


