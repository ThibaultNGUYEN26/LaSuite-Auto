# DocComparisonLeft

Left/local document state

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**n** | **int** | Sequential action number | [optional] 
**h** | **str** | Hash identifier | [optional] 

## Example

```python
from grist_client.models.doc_comparison_left import DocComparisonLeft

# TODO update the JSON string below
json = "{}"
# create an instance of DocComparisonLeft from a JSON string
doc_comparison_left_instance = DocComparisonLeft.from_json(json)
# print the JSON string representation of the object
print(DocComparisonLeft.to_json())

# convert the object into a dict
doc_comparison_left_dict = doc_comparison_left_instance.to_dict()
# create an instance of DocComparisonLeft from a dict
doc_comparison_left_from_dict = DocComparisonLeft.from_dict(doc_comparison_left_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


