# UpdateColumnsColumnsInnerFields


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Column type, by default Any. Ref, RefList and DateTime types requires a postfix, e.g. &lt;code&gt;DateTime:America/New_York&lt;/code&gt;, &lt;code&gt;Ref:Users&lt;/code&gt; | [optional] 
**label** | **str** | Column label. | [optional] 
**formula** | **str** | A python formula, e.g.: &lt;code&gt;$A + Table1.lookupOne(B&#x3D;$B)&lt;/code&gt; | [optional] 
**is_formula** | **bool** | Use \&quot;true\&quot; to indicate that the column is a formula column. Use \&quot;false\&quot; for trigger formula column. | [optional] 
**widget_options** | **str** | A JSON object with widget options, e.g.: &lt;code&gt;{\&quot;choices\&quot;: [\&quot;cat\&quot;, \&quot;dog\&quot;], \&quot;alignment\&quot;: \&quot;right\&quot;}&lt;/code&gt; | [optional] 
**untie_col_id_from_label** | **bool** | Use \&quot;true\&quot; to indicate that the column label should not be used as the column identifier. Use \&quot;false\&quot; to use the label as the identifier. | [optional] 
**recalc_when** | **int** | A number indicating when the column should be recalculated. &lt;ol start&#x3D;&#39;0&#39;&gt;&lt;li&gt;On new records or when any field in recalcDeps changes, it&#39;s a &#39;data-cleaning&#39;.&lt;/li&gt;&lt;li&gt;Never.&lt;/li&gt;&lt;li&gt;Calculate on new records and on manual updates to any data field.&lt;/li&gt;&lt;/ol&gt; | [optional] 
**visible_col** | **int** | For Ref and RefList columns, the colRef of a column to display | [optional] 
**recalc_deps** | **str** | An encoded array of column identifiers (colRefs) that this column depends on. If any of these columns change, the column will be recalculated. E.g.: &lt;code&gt;[2, 3]&lt;/code&gt; | [optional] 
**col_id** | **str** | Set it to the new column ID when you want to change it. | [optional] 

## Example

```python
from grist_client.models.update_columns_columns_inner_fields import UpdateColumnsColumnsInnerFields

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateColumnsColumnsInnerFields from a JSON string
update_columns_columns_inner_fields_instance = UpdateColumnsColumnsInnerFields.from_json(json)
# print the JSON string representation of the object
print(UpdateColumnsColumnsInnerFields.to_json())

# convert the object into a dict
update_columns_columns_inner_fields_dict = update_columns_columns_inner_fields_instance.to_dict()
# create an instance of UpdateColumnsColumnsInnerFields from a dict
update_columns_columns_inner_fields_from_dict = UpdateColumnsColumnsInnerFields.from_dict(update_columns_columns_inner_fields_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


