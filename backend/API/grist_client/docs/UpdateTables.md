# UpdateTables


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tables** | [**List[UpdateTablesTablesInner]**](UpdateTablesTablesInner.md) |  | 

## Example

```python
from grist_client.models.update_tables import UpdateTables

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateTables from a JSON string
update_tables_instance = UpdateTables.from_json(json)
# print the JSON string representation of the object
print(UpdateTables.to_json())

# convert the object into a dict
update_tables_dict = update_tables_instance.to_dict()
# create an instance of UpdateTables from a dict
update_tables_from_dict = UpdateTables.from_dict(update_tables_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


