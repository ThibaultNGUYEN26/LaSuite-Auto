# ColumnsListColumnsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] 
**fields** | [**GetFields**](GetFields.md) |  | [optional] 

## Example

```python
from grist_client.models.columns_list_columns_inner import ColumnsListColumnsInner

# TODO update the JSON string below
json = "{}"
# create an instance of ColumnsListColumnsInner from a JSON string
columns_list_columns_inner_instance = ColumnsListColumnsInner.from_json(json)
# print the JSON string representation of the object
print(ColumnsListColumnsInner.to_json())

# convert the object into a dict
columns_list_columns_inner_dict = columns_list_columns_inner_instance.to_dict()
# create an instance of ColumnsListColumnsInner from a dict
columns_list_columns_inner_from_dict = ColumnsListColumnsInner.from_dict(columns_list_columns_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


