## 处理大型 xml 文件

功能：
* 使用 elementTree 包迭代解析单行xml并提取结构化信息。
* 使用生成器返回结果，将结果写入 tsv 文件，文件名需在运行脚本时指定。

如何使用：
```python
python parse_xml2tsv_et.py test.tsv
```