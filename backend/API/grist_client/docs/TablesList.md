# TablesList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tables** | [**List[TablesListTablesInner]**](TablesListTablesInner.md) |  | 

## Example

```python
from grist_client.models.tables_list import TablesList

# TODO update the JSON string below
json = "{}"
# create an instance of TablesList from a JSON string
tables_list_instance = TablesList.from_json(json)
# print the JSON string representation of the object
print(TablesList.to_json())

# convert the object into a dict
tables_list_dict = tables_list_instance.to_dict()
# create an instance of TablesList from a dict
tables_list_from_dict = TablesList.from_dict(tables_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


