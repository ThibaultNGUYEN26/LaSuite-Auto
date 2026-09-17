# ColumnsList


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[ColumnsListColumnsInner]**](ColumnsListColumnsInner.md) |  | [optional] 

## Example

```python
from grist_client.models.columns_list import ColumnsList

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnsList from a JSON string
columns_list_instance = ColumnsList.from_json(json)
# print the JSON string representation of the object
print(ColumnsList.to_json())

# convert the object into a dict
columns_list_dict = columns_list_instance.to_dict()
# create an instance of ColumnsList from a dict
columns_list_from_dict = ColumnsList.from_dict(columns_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


