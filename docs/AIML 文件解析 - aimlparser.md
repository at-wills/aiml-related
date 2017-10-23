# AIML 文件解析 - AimlParser

AimlParser 类是 PYAIML 用于完成解析 AIML 文件的部分，它将 AIML 语法中的匹配规则转换为结构化的对象形式进行存储。

## AimlParser 运行机制

AimlParser 实际上是对 xml.sax 的扩展，通过自定义的 AimlHandler 来指明相应的 AIML 文件的语法解析规则。

```python
def create_parser():
    """Create and return an AIML parser object."""
    parser = xml.sax.make_parser()
    handler = AimlHandler("UTF-8")
    parser.setContentHandler(handler)
    return parser
```

常见的语法解析器由两类接口，一类是基于对象的（如：DOM），另一类是基于事件的接口（如：SAX）。

* 基于对象的接口，通过在内存中显示地构建对象树来与应用程序通信，对象树是 XML 文件中元素树的精确映射。

* 而基于事件的语法分析器将事件发送给应用程序，这些事件类似于用户界面事件，应用程序会对这些事件进行捕捉并作出反应。在 XML 语法分析器中，事件与用户操作无关，而与正在读取的 XML 文档中的元素有关。常见的驱动事件有：元素开始和结束标记、元素内容、实体以及语法分析错误等。

以上DOM和SAX的介绍信息，参考 [Python：使用基于事件驱动的SAX解析XML](http://www.cnblogs.com/hongfei/p/python-xml-sax.html)

AimlHandler 是对 xml.sax.handler.ContentHandler 的扩展，其定义了 AIML 文件的语法解析规则，我们需要关注的是它语法解析过程的三个主要函数：

* **startElement\(name, attr\)：**遇到XML开始标签时调用，name是标签的名字，attr是标签的属性值字典

* **characters\(content\)：**

  * 从行开始，遇到标签之前，存在字符，content的值为这些字符串

  * 从一个标签，遇到下一个标签之前， 存在字符，content的值为这些字符串

  * 从一个标签，遇到行结束符之前，存在字符，content的值为这些字符串

* **endElement\(name\)：**遇到XML结束标签时调用

因此，我们也重点关注 AimlHandler 中的这三个函数

**由于SAX是基于事件驱动的语法解析器，在解析过程中我们会通过记录不同的状态来标记我们的语法解析进程。而语法解析过程的状态是有限的，为了方便我们描述 AimlParser 的完整解析过程，下面将通过有限自动机来描述这一过程。有限自动机的主要概念包括：状态、事件、转换、动作。**

其中 startElement、characters、endElement 等函数定义了有限自动机的事件，并且包含以下状态：

* \_STATE\_OutsideAiml —— 当前解析过程处于 &lt;aiml&gt; 标签外，记为 OUT_AIML
* \_STATE\_InsideAiml —— 当前解析过程处于 &lt;aiml&gt; 标签中，记为 IN_AIML
* \_STATE\_InsideCategory —— 当前解析过程处于 &lt;category&gt; 标签中，记为 IN_CATEGORY
* \_STATE\_InsidePattern —— 当前解析过程处于 &lt;pattern&gt; 标签中，记为 IN_PATTERN
* \_STATE\_AfterPattern —— 当前解析过程处于 &lt;pattern&gt; 标签后，记为 ATR_PATTERN
* \_STATE\_InsideThat —— 当前解析过程处于 &lt;that&gt; 标签中，记为 IN_THAT
* \_STATE\_AfterThat —— 当前解析过程处于 &lt;that&gt; 标签后，记为 ATR_THAT
* \_STATE\_InsideTemplate —— 当前解析过程处于 &lt;template&gt; 标签中，记为 IN_TEMPLATE
* \_STATE\_AfterTemplate —— 当前解析过程处于 &lt;template&gt; 标签后，记为 ATR_TEMPLATE

## startElement函数

```python
def startElement(self, name, attr):
    # Wrapper around _startElement, which catches errors in _startElement()
    # and keeps going.

    # If we're inside an unknown element, ignore everything until we're
    # out again.
    if self._currentUnknown != "":
        return
    # If we're skipping the current category, ignore everything until
    # it's finished.
    if self._skipCurrentCategory:
        return

    # process this start-element.
    try: self._startElement(name, attr)
    except AimlParserError, msg:
        # Print the error message
        sys.stderr.write("PARSE ERROR: %s\n" % msg)

        self._numParseErrors += 1 # increment error count
        # In case of a parse error, if we're inside a category, skip it.
        if self._state >= self._STATE_InsideCategory:
            self._skipCurrentCategory = True
```

startElement 函数被调用，表明XML语法解析进入到一个元素的开始标签，首先需要对不合法内容进行过滤，不合法情况分为两种：
* 当前解析标签的祖先标签是未知标签，即其祖先标签不存在于AIML语法定义中，对于这类标签我们不作处理
* 解析当前 category（匹配规则）过程中出现了语法错误，则对于该 category 包括的全部内容也跳过不作处理。在完成不合法内容进行过滤后，我们通过调用 \_startElement 函数来对标签进行解析，同时捕捉该函数抛出的语法错误异常

```python
def _startElement(self, name, attr):
    if name == "aiml":
        # deal with event start_aiml
    elif self._state == self._STATE_OutsideAiml:
        # deal with event start_not_aiml
    elif name == "topic":
        # <topic> tags are only legal in the InsideAiml state, and only
        # if we're not already inside a topic.
        if (self._state != self._STATE_InsideAiml) or self._insideTopic:
            raise AimlParserError, "Unexpected <topic> tag", self._location()
        try: self._currentTopic = unicode(attr['name'])
        except KeyError:
            raise AimlParserError, "Required \"name\" attribute missing in <topic> element "+self._location()
        self._insideTopic = True
    elif name == "category":
        # deal with event start_category
    elif name == "pattern":
        # deal with event start_pattern
    elif name == "that" and self._state == self._STATE_AfterPattern:
        # deal with event start_that
    elif name == "template":
        # deal with event start_template
    elif self._state == self._STATE_InsidePattern:
        # Certain tags are allowed inside <pattern> elements.
        if name == "bot" and attr.has_key("name") and attr["name"] == u"name":
            # Insert a special character string that the PatternMgr will
            # replace with the bot's name.
            self._currentPattern += u" BOT_NAME "
        else:
            raise AimlParserError, ("Unexpected <%s> tag " % name)+self._location()
    elif self._state == self._STATE_InsideThat:
        # Certain tags are allowed inside <that> elements.
        if name == "bot" and attr.has_key("name") and attr["name"] == u"name":
            # Insert a special character string that the PatternMgr will
            # replace with the bot's name.
            self._currentThat += u" BOT_NAME "
        else:
            raise AimlParserError, ("Unexpected <%s> tag " % name)+self._location()
    elif self._state == self._STATE_InsideTemplate and self._validInfo.has_key(name):
        # deal with event start_valid
    else:
        # we're now inside an unknown element.
        if self._forwardCompatibleMode:
            # In Forward Compatibility Mode, we ignore the element and its
            # contents.
            self._currentUnknown = name
        else:
            # Otherwise, unknown elements are grounds for error!
            raise AimlParserError, ("Unexpected <%s> tag " % name)+self._location()
```

该函数通过 \_state 对当前语法解析器的状态进行记录，当事件触发后，通过对当前状态的判断以及本次事件的信息来转移到另一种相应的状态。具体可描述为以下状态转换过程：

### 事件 start_aiml

```python
if name == "aiml":
    # <aiml> tags are only legal in the OutsideAiml state
    if self._state != self._STATE_OutsideAiml:
        raise AimlParserError, "Unexpected <aiml> tag "+self._location()
    self._state = self._STATE_InsideAiml
    self._insideTopic = False
    self._currentTopic = u""
    try: self._version = attr["version"]
    except KeyError:
        # This SHOULD be a syntax error, but so many AIML sets out there are missing
        # "version" attributes that it just seems nicer to let it slide.
        #raise AimlParserError, "Missing 'version' attribute in <aiml> tag "+self._location()
        #print "WARNING: Missing 'version' attribute in <aiml> tag "+self._location()
        #print "         Defaulting to version 1.0"
        self._version = "1.0"
    self._forwardCompatibleMode = (self._version != "1.0.1")
    self._pushWhitespaceBehavior(attr)    
```

当解析标签为&lt;aiml&gt;，记为事件 start_aiml
* 若状态为 OUT_AIML，则 OUT_AIML —&gt; \(start_aiml\) IN_AIML

### 事件 start_not_aiml

```python
elif self._state == self._STATE_OutsideAiml:
    # If we're outside of an AIML element, we ignore all tags.
    return    
```

当解析标签不是&lt;aiml&gt;，记为事件 start_not_aiml
* 若状态为 OUT_AIML，则OUT_AIML —&gt; \(start_not_aiml\) OUT_AIML

### 事件 start_category

```python
elif name == "category":
    # <category> tags are only legal in the InsideAiml state
    if self._state != self._STATE_InsideAiml:
        raise AimlParserError, "Unexpected <category> tag "+self._location()
    self._state = self._STATE_InsideCategory
    self._currentPattern = u""
    self._currentThat = u""
    # If we're not inside a topic, the topic is implicitly set to *
    if not self._insideTopic: self._currentTopic = u"*"
    self._elemStack = []
    self._pushWhitespaceBehavior(attr)
```

当解析标签为&lt;category&gt;，记为事件 start_category
* 若状态为 IN_AIML，则 IN_AIML —&gt; \(start_category\) IN_CATEGORY，并对\_currentPattern、\_currentThat、\_elemStack进行初始化

### 事件 start_pattern

```python
elif name == "pattern":
    # <pattern> tags are only legal in the InsideCategory state
    if self._state != self._STATE_InsideCategory:
        raise AimlParserError, "Unexpected <pattern> tag "+self._location()
    self._state = self._STATE_InsidePattern
```

当解析标签为&lt;pattern&gt;，记为事件 start_pattern
* 若状态为 IN_CATEGORY，则 IN_CATEGORY —&gt; \(start_pattern\) IN_PATTERN

### 事件 start_that

```python
elif name == "that" and self._state == self._STATE_AfterPattern:
    # <that> are legal either inside a <template> element, or
    # inside a <category> element, between the <pattern> and the
    # <template> elements.  This clause handles the latter case.
    self._state = self._STATE_InsideThat
```

当解析标签为&lt;that&gt;，记为事件 start_that
* 若状态为 ATR_PATTERN，则 ATR_PATTERN —&gt; \(start_that\) IN_THAT

### 事件 start_template

```python
elif name == "template":
    # <template> tags are only legal in the AfterPattern and AfterThat
    # states
    if self._state not in [self._STATE_AfterPattern, self._STATE_AfterThat]:
        raise AimlParserError, "Unexpected <template> tag "+self._location()
    # if no <that> element was specified, it is implicitly set to *
    if self._state == self._STATE_AfterPattern:
        self._currentThat = u"*"
    self._state = self._STATE_InsideTemplate
    self._elemStack.append(['template',{}])
    self._pushWhitespaceBehavior(attr)
```

当解析标签为&lt;template&gt;，记为事件 start_template
* 若状态为 ATR_PATTERN，则 ATR_PATTERN —> \(start_template\) IN_TEMPLATE，并对\_currentThat进行初始化，同时向\_elemStack添加template描述
* 若状态为 ATR_THAT，则 ATR_THAT —&gt; \(start_template\) IN_TEMPLATE，并向\_elemStack添加template描述

### 事件 start_valid

```python
elif self._state == self._STATE_InsideTemplate and self._validInfo.has_key(name):
    # Starting a new element inside the current pattern. First
    # we need to convert 'attr' into a native Python dictionary,
    # so it can later be marshaled.
    attrDict = {}
    for k,v in attr.items():
        #attrDict[k[1].encode(self._encoding)] = v.encode(self._encoding)
        attrDict[k.encode(self._encoding)] = unicode(v)
    self._validateElemStart(name, attrDict, self._version)
    # Push the current element onto the element stack.
    self._elemStack.append([name.encode(self._encoding),attrDict])
    self._pushWhitespaceBehavior(attr)
    # If this is a condition element, push a new entry onto the
    # foundDefaultLiStack
    if name == "condition":
        self._foundDefaultLiStack.append(False)
```

当解析标签为 template 合法子标签，记为事件 start_valid
* 若状态为 IN_TEMPLATE，则 IN_TEMPLATE —> \(start_valid\) IN_TEMPLATE，并对标签开始部分的合法性进行检查，同时\_elemStack添加当前标签的描述

### 辅助函数功能说明

* \_pushWhitespaceBehavior\(\) —— 管理维护各个标签的文本，对于空白字符的处理方式
* \_validateElemStart\(\) —— 检查扩展标签的开始部分是否合法，规则如下：
  * 标签名称必须包含在 \_validInfo 字典中
  * 必须满足 \_validInfo 字典中对于该标签“必须属性”、“可选属性”的要求
  * 必须满足 \_validInfo 字典中对其父标签“可作为父标签”的要求
  * 若父标签为 &lt;condition&gt; 或 &lt;random&gt;，则标签名称只能为 &lt;li&gt;
  * 若标签名称为 &lt;li&gt;，则父标签只能为 &lt;condition&gt; 或 &lt;random&gt;且合法

## characters函数

```python
def characters(self, ch):
    # Wrapper around _characters which catches errors in _characters()
    # and keeps going.
    if self._state == self._STATE_OutsideAiml:
        # If we're outside of an AIML element, we ignore all text
        return
    if self._currentUnknown != "":
        # If we're inside an unknown element, ignore all text
        return
    if self._skipCurrentCategory:
        # If we're skipping the current category, ignore all text.
        return
    try: self._characters(ch)
    except AimlParserError, msg:
        # Print the message
        sys.stderr.write("PARSE ERROR: %s\n" % msg)
        self._numParseErrors += 1 # increment error count
        # In case of a parse error, if we're inside a category, skip it.
        if self._state >= self._STATE_InsideCategory:
            self._skipCurrentCategory = True
```

characters 函数被调用，表明XML语法解析从一个标签结束到一个新标签开始之间存在字符，同样首先需要对不合法内容进行过滤，不合法情况分为三种。一是当前状态处于 OUT_AIML，即解析过程不在&lt;aiml&gt;标签中，则忽略这些内容；另外两种情况同前面的startElement函数。在完成不合法内容进行过滤后，我们通过调用 \_characters 函数来对字符串内容进行解析，同时捕捉该函数抛出的语法错误异常。

```python
def _characters(self, ch):
    text = unicode(ch)
    if self._state == self._STATE_InsidePattern:
        # TODO: text inside patterns must be upper-case!
        self._currentPattern += text
    elif self._state == self._STATE_InsideThat:
        self._currentThat += text
    elif self._state == self._STATE_InsideTemplate:
        # First, see whether the element at the top of the element stack
        # is permitted to contain text.
        try:
            parent = self._elemStack[-1][0]
            parentAttr = self._elemStack[-1][1]
            required, optional, canBeParent = self._validInfo[parent]
            nonBlockStyleCondition = (parent == "condition" and not (parentAttr.has_key("name") and parentAttr.has_key("value")))
            if not canBeParent:
                raise AimlParserError, ("Unexpected text inside <%s> element "%parent)+self._location()
            elif parent == "random" or nonBlockStyleCondition:
                # <random> elements can only contain <li> subelements. However,
                # there's invariably some whitespace around the <li> that we need
                # to ignore. Same for non-block-style <condition> elements (i.e.
                # those which don't have both a "name" and a "value" attribute).
                if len(text.strip()) == 0:
                    # ignore whitespace inside these elements.
                    return
                else:
                    # non-whitespace text inside these elements is a syntax error.
                    raise AimlParserError, ("Unexpected text inside <%s> element "%parent)+self._location()
        except IndexError:
            # the element stack is empty. This should never happen.
            raise AimlParserError, "Element stack is empty while validating text "+self._location()

        # Add a new text element to the element at the top of the element
        # stack. If there's already a text element there, simply append the
        # new characters to its contents.
        try: textElemOnStack = (self._elemStack[-1][-1][0] == "text")
        except IndexError: textElemOnStack = False
        except KeyError: textElemOnStack = False
        if textElemOnStack:
            self._elemStack[-1][-1][2] += text
        else:
            self._elemStack[-1].append(["text", {"xml:space": self._whitespaceBehaviorStack[-1]}, text])
    else:
        # all other text is ignored
        pass
```

同理，以上函数可描述为以下状态转换过程：

将解析字符串内容统一记为事件 get_chars
* 若状态为 IN_PATTERN，则 IN_PATTERN —&gt; \(get_chars\) IN_PATTERN，并将字符串内容串连到 \_currentPattern 上
* 若状态为 IN_THAT，则 IN_THAT —&gt; \(get_chars\) IN_THAT，并将字符串内容串连到 \_currentThat 上
* 若状态为 IN_TEMPLATE，则 IN_TEMPLATE —&gt; \(get_chars\) IN_TEMPLATE，并在保证父标签与当前标签关系合法的前提下，将字符串内容存放到 \_elemStack中

## endElement函数

```python
def endElement(self, name):
    """Wrapper around _endElement which catches errors in _characters()
    and keeps going.

    """
    if self._state == self._STATE_OutsideAiml:
        # If we're outside of an AIML element, ignore all tags
        return
    if self._currentUnknown != "":
        # see if we're at the end of an unknown element.  If so, we can
        # stop ignoring everything.
        if name == self._currentUnknown:
            self._currentUnknown = ""
        return
    if self._skipCurrentCategory:
        # If we're skipping the current category, see if it's ending. We
        # stop on ANY </category> tag, since we're not keeping track of
        # state in ignore-mode.
        if name == "category":
            self._skipCurrentCategory = False
            self._state = self._STATE_InsideAiml
        return
    try: self._endElement(name)
    except AimlParserError, msg:
        # Print the message
        sys.stderr.write("PARSE ERROR: %s\n" % msg)
        self._numParseErrors += 1 # increment error count
        # In case of a parse error, if we're inside a category, skip it.
        if self._state >= self._STATE_InsideCategory:
            self._skipCurrentCategory = True
```

endElement 函数被调用，表明XML语法解析进入到一个元素的结束标签，同样首先需要对不合法内容进行过滤，不合法情况分为三种，且与前面的 character 函数相同。在完成不合法内容进行过滤后，我们通过调用 \_endElement 函数来对标签进行解析，同时捕捉该函数抛出的语法错误异常。

```python
def _endElement(self, name):
    """Verify that an AIML end element is valid in the current
    context.

    Raises an AimlParserError if an illegal end element is encountered.

    """
    if name == "aiml":
        # deal with event end_aiml
    elif name == "topic":
        # </topic> tags are only legal in the InsideAiml state, and
        # only if _insideTopic is true.
        if self._state != self._STATE_InsideAiml or not self._insideTopic:
            raise AimlParserError, "Unexpected </topic> tag "+self._location()
        self._insideTopic = False
        self._currentTopic = u""
    elif name == "category":
        # deal with event end_category
    elif name == "pattern":
        # deal with event end_pattern
    elif name == "that" and self._state == self._STATE_InsideThat:
        # deal with event end_that
    elif name == "template":
        # deal with event end_template
    elif self._state == self._STATE_InsidePattern:
        # Certain tags are allowed inside <pattern> elements.
        if name not in ["bot"]:
            raise AimlParserError, ("Unexpected </%s> tag " % name)+self._location()
    elif self._state == self._STATE_InsideThat:
        # Certain tags are allowed inside <that> elements.
        if name not in ["bot"]:
            raise AimlParserError, ("Unexpected </%s> tag " % name)+self._location()
    elif self._state == self._STATE_InsideTemplate:
        # deal with event end_valid
    else:
        # Unexpected closing tag
        raise AimlParserError, ("Unexpected </%s> tag " % name)+self._location()
```

同理，以上函数可描述为以下状态转换过程：

### 事件 end_aiml

```python
if name == "aiml":
    # </aiml> tags are only legal in the InsideAiml state
    if self._state != self._STATE_InsideAiml:
        raise AimlParserError, "Unexpected </aiml> tag "+self._location()
    self._state = self._STATE_OutsideAiml
    self._whitespaceBehaviorStack.pop()
```

当解析标签为 &lt;/aiml&gt;，记为事件 end_aiml
* 若状态为 IN_AIML，则IN_AIML —&gt; \(end_aiml\) OUT_AIML

### 事件 end_category

```python
elif name == "category":
    # </category> tags are only legal in the AfterTemplate state
    if self._state != self._STATE_AfterTemplate:
        raise AimlParserError, "Unexpected </category> tag "+self._location()
    self._state = self._STATE_InsideAiml
    # End the current category.  Store the current pattern/that/topic and
    # element in the categories dictionary.
    key = (self._currentPattern.strip(), self._currentThat.strip(),self._currentTopic.strip())
    self.categories[key] = self._elemStack[-1]
    self._whitespaceBehaviorStack.pop()
```

当解析标签为 &lt;/category&gt;，记为事件 end_category
* 若状态为 ATR_TEMPLATE，则 ATR_TEMPLATE —&gt; \(end_category\) IN_AIML，并将完整的匹配规则存放到 categories 字典中，一个完整的匹配规则包括：pattern\(必须\)、that\(可选\)、topic\(可选\)、template\(必须\)等四方面信息

### 事件 end_pattern

```python
elif name == "pattern":
    # </pattern> tags are only legal in the InsidePattern state
    if self._state != self._STATE_InsidePattern:
        raise AimlParserError, "Unexpected </pattern> tag "+self._location()
    self._state = self._STATE_AfterPattern
```

当解析标签为 &lt;/pattern&gt;，记为事件 end_pattern
* 若状态为 IN_PATTERN，则 IN_PATTERN —&gt; \(end_pattern\) ATR_PATTERN

### 事件 end_that

```python
elif name == "that" and self._state == self._STATE_InsideThat:
    # </that> tags are only allowed inside <template> elements or in
    # the InsideThat state.  This clause handles the latter case.
    self._state = self._STATE_AfterThat
```

当解析标签为 &lt;/that&gt;，记为事件 end_that
* 若状态为 IN_THAT，则 IN_THAT —&gt; \(end_that\) ATR_THAT

### 事件 end_template

```python
elif name == "template":
    # </template> tags are only allowed in the InsideTemplate state.
    if self._state != self._STATE_InsideTemplate:
        raise AimlParserError, "Unexpected </template> tag "+self._location()
    self._state = self._STATE_AfterTemplate
    self._whitespaceBehaviorStack.pop()
```

当解析标签为 &lt;/template&gt;，记为事件 end_template
* 若状态为 IN_TEMPLATE，则 IN_TEMPLATE —&gt; \(end_template\) ATR_TEMPLATE

### 事件 end_valid

```python
elif self._state == self._STATE_InsideTemplate:
    # End of an element inside the current template.  Append the
    # element at the top of the stack onto the one beneath it.
    elem = self._elemStack.pop()
    self._elemStack[-1].append(elem)
    self._whitespaceBehaviorStack.pop()
    # If the element was a condition, pop an item off the
    # foundDefaultLiStack as well.
    if elem[0] == "condition": self._foundDefaultLiStack.pop()
```

当解析标签为 template 合法子标签，记为事件 end_valid
* 若状态为 IN_TEMPLATE，则 IN_TEMPLATE —&gt; \(end_valid\) IN_TEMPLATE，并将 \_elemStack 的最后一个数据放到 \_elemStack 的倒数第二个数据中

## 结果

**最终可得以下有限自动机模型**

![](/assets/model.png)

> 若图像不清晰，可以右键点击图片-在新标签页中打开图片，查看大图

**存放于 categories 的结构化的对象形式如下**

```
key：({category}, {that}, {topic})

value:
value：
[
    'template', {},
    ['text', {'xml:space': 'default'}, u'answer']
]
OR
[
    'template', {},
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
