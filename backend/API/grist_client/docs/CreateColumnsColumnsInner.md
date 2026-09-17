# CreateColumnsColumnsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Column identifier | [optional] 
**fields** | [**CreateFields**](CreateFields.md) |  | [optional] 

## Example

```python
from grist_client.models.create_columns_columns_inner import CreateColumnsColumnsInner

# TODO update the JSON string below
json = "{}"
# create an instance of CreateColumnsColumnsInner from a JSON string
create_columns_columns_inner_instance = CreateColumnsColumnsInner.from_json(json)
# print the JSON string representation of the object
print(CreateColumnsColumnsInner.to_json())

# convert the object into a dict
create_columns_columns_inner_dict = create_columns_columns_inner_instance.to_dict()
# create an instance of CreateColumnsColumnsInner from a dict
create_columns_columns_inner_from_dict = CreateColumnsColumnsInner.from_dict(create_columns_columns_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


