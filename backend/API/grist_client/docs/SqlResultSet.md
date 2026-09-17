# SqlResultSet


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**statement** | **str** | A copy of the SQL statement. | 
**records** | [**List[SqlResultSetRecordsInner]**](SqlResultSetRecordsInner.md) |  | 

## Example

```python
from grist_client.models.sql_result_set import SqlResultSet

# TODO update the JSON string below
json = "{}"
# create an instance of SqlResultSet from a JSON string
sql_result_set_instance = SqlResultSet.from_json(json)
# print the JSON string representation of the object
print(SqlResultSet.to_json())

# convert the object into a dict
sql_result_set_dict = sql_result_set_instance.to_dict()
# create an instance of SqlResultSet from a dict
sql_result_set_from_dict = SqlResultSet.from_dict(sql_result_set_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


