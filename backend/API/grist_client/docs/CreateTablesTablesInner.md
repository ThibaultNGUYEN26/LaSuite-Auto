# CreateTablesTablesInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**columns** | [**List[CreateTablesTablesInnerColumnsInner]**](CreateTablesTablesInnerColumnsInner.md) |  | 

## Example

```python
from grist_client.models.create_tables_tables_inner import CreateTablesTablesInner

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTablesTablesInner from a JSON string
create_tables_tables_inner_instance = CreateTablesTablesInner.from_json(json)
# print the JSON string representation of the object
print(CreateTablesTablesInner.to_json())

# convert the object into a dict
create_tables_tables_inner_dict = create_tables_tables_inner_instance.to_dict()
# create an instance of CreateTablesTablesInner from a dict
create_tables_tables_inner_from_dict = CreateTablesTablesInner.from_dict(create_tables_tables_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


