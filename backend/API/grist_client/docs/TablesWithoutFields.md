# TablesWithoutFields


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tables** | [**List[TablesWithoutFieldsTablesInner]**](TablesWithoutFieldsTablesInner.md) |  | 

## Example

```python
from grist_client.models.tables_without_fields import TablesWithoutFields

# TODO update the JSON string below
json = "{}"
# create an instance of TablesWithoutFields from a JSON string
tables_without_fields_instance = TablesWithoutFields.from_json(json)
# print the JSON string representation of the object
print(TablesWithoutFields.to_json())

# convert the object into a dict
tables_without_fields_dict = tables_without_fields_instance.to_dict()
# create an instance of TablesWithoutFields from a dict
tables_without_fields_from_dict = TablesWithoutFields.from_dict(tables_without_fields_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


