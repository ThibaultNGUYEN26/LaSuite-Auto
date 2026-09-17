# DocComparison

Comparison result between two document versions

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**left** | [**DocComparisonLeft**](DocComparisonLeft.md) |  | 
**right** | [**DocComparisonRight**](DocComparisonRight.md) |  | 
**parent** | [**DocComparisonParent**](DocComparisonParent.md) |  | 
**summary** | **str** | Relationship summary: - same: documents have the same most recent state - left: the left document has actions not yet in the right - right: the right document has actions not yet in the left - both: both documents have changes (possible divergence) - unrelated: no common history found  | 
**details** | [**DocComparisonDetails**](DocComparisonDetails.md) |  | [optional] 

## Example

```python
from grist_client.models.doc_comparison import DocComparison

# TODO update the JSON string below
json = "{}"
# create an instance of DocComparison from a JSON string
doc_comparison_instance = DocComparison.from_json(json)
# print the JSON string representation of the object
print(DocComparison.to_json())

# convert the object into a dict
doc_comparison_dict = doc_comparison_instance.to_dict()
# create an instance of DocComparison from a dict
doc_comparison_from_dict = DocComparison.from_dict(doc_comparison_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


