import xml.etree.cElementTree as et
import csv
import sys

def parse_xml(file): 
    """
    使用 ElementTree 的迭代解析接口。
    每解析到一个 document 元素，获取其id，
    并深度遍历 document 下每个 passage 的子元素，
    处理完一个 document 后 clear 该元素占用的内存，并 yield 一个结果 doc_dict。
    """
    for event, elem in et.iterparse(file):
        if event == 'end':
            if elem.tag == 'document':
                document_id = elem.find('.//id').text.strip()
                passages = elem.findall('.//passage')
                one_row = [document_id]
                identifier_flag = 0  # 标记是否有 identifier
                for passage in passages:  
                    for element in passage.iter():
                        if 'key' in element.attrib:
                            if element.attrib['key'] == 'type' and identifier_flag == 1:
                                one_row.append(element.text.strip())
                            if element.attrib['key'] == 'identifier':
                                identifier_flag = 1
                                one_row.append(element.text.strip())
                        elif identifier_flag == 1:  # identifier 值不为空
                            if 'offset' in element.attrib and 'length' in element.attrib:
                                one_row += [element.attrib['offset'], element.attrib['length']]
                            elif element.tag == 'text':
                                one_row.append(element.text.strip())
                                yield one_row  # 输出一行数据
                                one_row = [document_id]
                                identifier_flag = 0
                elem.clear()  # 清理该元素占用的内存


if __name__ == '__main__':
    file_name = sys.argv[1]
    with open(file_name, 'w') as f:
        tsv_writer = csv.writer(f, delimiter='\t')
        tsv_writer.writerow(['id', 'identifier', 'type', 'offset', 'length', 'text'])
        count = 0
        with open('test.xml') as f:
            p = parse_xml(f)
            for i in p:
                tsv_writer.writerow(i)
                count += 1
            print('已写入行数：', count)