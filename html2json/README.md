## HTML2JSON

从html文件提取出元素的各种属性值，转换为json格式。

### 使用 Selenium 需注意的细节
1. 不位于浏览器窗口可见范围内的元素是不可点击的。
2. 若 A 元素位于 B 元素之上，A元素可点击，B元素不可点击。需点击 B 元素，要先通过操作 js 脚本删除 A 元素。
3. webdriver 实例是不可 pickle 的，即不能序列化，所以不能多进程的方式同时操作多个浏览器。

### 收获
1. 中文字典写入 json 文件的正确姿势
```python
import json

test_dict = {'字典': 2}
with open('test.json', 'a', encoding='utf8') as f:
    f.write(json.dumps(test_dict, ensure_ascii=False))
```
2. 异步IO实际上是用一个线程在多个任务函数之间来回切换，适用于需要等待网络请求的返回或读写磁盘的任务。异步IO和多线程都是在IO密集型任务上优势明显，它们都可以避免IO等待时造成的资源浪费。相比多线程，异步更适合每次等待时间更长，等待任务更多的程序，因为线程太多会使竞争现象更加明显，造成的资源浪费也会更多。
