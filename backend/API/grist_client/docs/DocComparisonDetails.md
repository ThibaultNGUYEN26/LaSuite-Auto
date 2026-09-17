# DocComparisonDetails

Detailed change information (when requested)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**left_changes** | **object** | Changes in the left document relative to common ancestor | [optional] 
**right_changes** | **object** | Changes in the right document relative to common ancestor | [optional] 

## Example

```python
from grist_client.models.doc_comparison_details import DocComparisonDetails

# TODO update the JSON string below
json = "{}"
# create an instance of DocComparisonDetails from a JSON string
doc_comparison_details_instance = DocComparisonDetails.from_json(json)
# print the JSON string representation of the object
print(DocComparisonDetails.to_json())

# convert the object into a dict
doc_comparison_details_dict = doc_comparison_details_instance.to_dict()
# create an instance of DocComparisonDetails from a dict
doc_comparison_details_from_dict = DocComparisonDetails.from_dict(doc_comparison_details_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


