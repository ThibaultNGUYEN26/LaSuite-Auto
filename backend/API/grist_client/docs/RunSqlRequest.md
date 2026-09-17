# RunSqlRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sql** | **str** | The SQL query to run. Must be a single SELECT statement, with no trailing semicolon. WITH clauses are permitted. All Grist documents are currently SQLite databases, and the SQL query is interpreted and run by SQLite, with various defensive measures. Statements that would modify the database are not supported. | 
**args** | [**List[RunSqlRequestArgsInner]**](RunSqlRequestArgsInner.md) | Parameters for the query. | [optional] 
**timeout** | **float** | Timeout after which operations on the document will be interrupted. Specified in milliseconds. Defaults to 1000 (1 second). This default is controlled by an optional environment variable read by the Grist app, GRIST_SQL_TIMEOUT_MSEC. The default cannot be exceeded, only reduced. | [optional] 

## Example

```python
from grist_client.models.run_sql_request import RunSqlRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RunSqlRequest from a JSON string
run_sql_request_instance = RunSqlRequest.from_json(json)
# print the JSON string representation of the object
print(RunSqlRequest.to_json())

# convert the object into a dict
run_sql_request_dict = run_sql_request_instance.to_dict()
# create an instance of RunSqlRequest from a dict
run_sql_request_from_dict = RunSqlRequest.from_dict(run_sql_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


