# 对 AimlParser 元素栈的分析

AimlParser 是pyaiml中用于解析 AIML 文件的类，通过使用 python 中的 xml.sax 类驱动解析 xml 树形结构。详细参考 [https://faunleaf.gitbooks.io/pyaiml/content/chapter2.html](https://faunleaf.gitbooks.io/pyaiml/content/chapter2.html "此处分析") 最后一部分的解释。

**以下方 xml 为例：**

```xml
<aiml version="1.0">
<category>
    <pattern>user question</pattern>
    <template>
        <random>
            <li>answer 1</li>
            <li>answer 2</li>
        </random>
    </template>
</category>
```

**解析出的字典的一个 key-value 对：**

```
key：({category}, {that}, {topic})

value:
[
    'template', {}, ['text', {'xml:space': 'default'}, u'\n        '],
    [
        'random', {}, 
        [
            'li', {}, ['text', {'xml:space': 'default'}, u'answer1']
        ], 
        [
            'li', {}, ['text', {'xml:space': 'default'}, u'answer2']
        ]
    ]
]
```

空的字典是每个标签的属性。因为常见标签没有额外属性，所以为空。

---

## 详细过程

主要过程请参考上方给出文章，本文给出一些细节内容。

#### **头部标签**

```xml
<aiml version="1.0">
<category>
    <pattern>user question</pattern>
    <template>
```

当解析到此处时，解析类中的元素栈`_elemStack`中含有一个列表元素，该列表内容如图所示：

![](/assets/snipaste 2017.10.13-01.20.jpg)

\_elemStack 此时为含有三个元素的列表，形如

```
[
    'template', {}, 
    [
        'text', {'xml:space': 'default'}, '\n'
    ]
]
```

其中含有 'text' 内容的列表元素，由以下代码生成：

```py
try: textElemOnStack = (self._elemStack[-1][-1][0] == "text")
except IndexError: textElemOnStack = False
except KeyError: textElemOnStack = False
if textElemOnStack:
    self._elemStack[-1][-1][2] += text
else:
    self._elemStack[-1].append(["text", {"xml:space": self._whitespaceBehaviorStack[-1]}, text])
```

另外关于 `_whitespaceBehaviorStack` 这个栈，它负责处理记录的是每行 aiml 中的多余空白符，即属于两个标签（不必配对）中间的空白符。当 aiml 内容格式如上方所示，含有缩进所用的空白符时，这个栈将记录它们，并在解析过程中被存入元素栈，即 `['text', {'xml:space': 'default'}, u'answer1']` 部分内容。实际发布的项目中，使用的 aiml 文件中空白符的数量会被减少。该条记录的实际作用尚未得知…

#### random 标签部分

继续向下进行解析，`_startElemnet` 方法中传入参数 `name` 通过为 "random"，进行判断：

```
self._state == self._STATE_InsideTemplate and self._validInfo.has_key(name)
```

得知 "random" 标签属于可以解析的扩展标签。

接下来将被调用的是 `_validateElemStart` 方法，验证处在 `template` 中的标签的有效性。该方法与前面解析的过程有少许重复，应该是出于程序健壮性考虑引入的冗余。

进一步元素入栈，此时 `_elemStack` 含有两个列表元素：

![](/assets/snipaste 2017.10.13-01.59.jpg)

#### li 标签部分

解析到 li 标签的startElement 结束，栈内元素如下：

![](/assets/snipaste 2017.10.13-02.04.jpg)

当对 li 标签内的文字内容执行 \_characters\(\) 方法，代码：

```py
self._elemStack[-1].append(["text", {"xml:space": self._whitespaceBehaviorStack[-1]}, text])
```

将 li 标签内容正确添加进来：

![](/assets/snipaste 2017.10.13-02.13.jpg)

程序进行到处理 li 标签结束的 \_endElement\(\) 方法，此时判断条件

```py
elif self._state == self._STATE_InsideTemplate:
```

成立，该结束标签是在 template 标签内出现的。开始进行元素栈的加工处理。

```py
# pop出栈中最后的元素
elem = self._elemStack.pop()

# 添加到前一个元素中
self._elemStack[-1].append(elem)
```

将最后 li 标签的列表出栈，加入前一个 random 标签元素中：

![](/assets/snipaste 2017.10.13-02.25_0.jpg)

于此同时，其对应在 \_whitespaceBehaviorStack 栈中的元素也出栈。

#### 过程推广

经过以上过程，元素栈中结构如下：

```
['template', {}, ['text', {'xmlspace': 'default'}, u'\n        ']],
[
    'random', {}, 
    [
        ['li', {}, ['text', {'xmlspace': 'default'}, u'answer 1']]
    ]
]
```

当进行到下一个 li 标签时，会产生第三个元素，在其 \_endElement\(\) 方法执行过程中被压栈进入 random 标签元素内，与上一个 li 标签元素同级，如下图：

![](/assets/snipaste 2017.10.13-02.37.jpg)

同理，在 random 的结束标签被处理时，它也被扩充进入了上一层 template 标签元素中。

#### key 的生成

程序最终储存的是一个字典 `categories`， key 是在 category 结束标签处理过程中生成的，value 即是 \_elemStack 中的元素。

```py
elif name == "category":
    if self._state != self._STATE_AfterTemplate:
        raise AimlParserError, "Unexpected </category> tag "+self._location()
    self._state = self._STATE_InsideAiml
    # End the current category.  Store the current pattern/that/topic and
    # element in the categories dictionary.
    key = (self._currentPattern.strip(), self._currentThat.strip(),self._currentTopic.strip())
    self.categories[key] = self._elemStack[-1]
```

key 值如下：

![](/assets/snipaste 2017.10.13-03.01.jpg)

#### 补充：

事实上，测试程序的实际结果与文章最前面提到的不同，真实数据如下：

![](/assets/snipaste 2017.10.13-03.03.jpg)多出来的两个列表 `['text', {'xml:space': 'default'}, u'\n        ']`，是由于 category 中的换行带来的。

纠正原 aiml 文件中的内容如下：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<aiml version="1.0">
<category><pattern>user question</pattern>
<template><random>  <li>answer 1</li>  <li>answer 2</li>  </random></template>
</category>
</aiml>
```

此时结果符合预测：![](/assets/snipaste 2017.10.13-17.07.jpg)

