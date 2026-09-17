# CreateTables


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tables** | [**List[CreateTablesTablesInner]**](CreateTablesTablesInner.md) |  | 

## Example

```python
from grist_client.models.create_tables import CreateTables

# TODO update the JSON string below
json = "{}"
# create an instance of CreateTables from a JSON string
create_tables_instance = CreateTables.from_json(json)
# print the JSON string representation of the object
print(CreateTables.to_json())

# convert the object into a dict
create_tables_dict = create_tables_instance.to_dict()
# create an instance of CreateTables from a dict
create_tables_from_dict = CreateTables.from_dict(create_tables_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


