# 基本的 response 过程

对以下 aiml 文件内容进行分析：

```xml
<?xml version = "1.0" encoding = "UTF-8"?>
<aiml version="1.0">
<category><pattern>USER QUESTION</pattern>
<template> hello </template>
</category>
<category><pattern>USER ANOTHER</pattern>
<template> hello again</template>
</category>
</aiml>
```

形成如下对话：

```
Enter your message >> user question
hello
```



## 初步处理

在 Kernel.respond 方法中：

```python
"""Return the Kernel's response to the input string."""
if len(input) == 0:
    return ""

#ensure that input is a unicode string
try: input = input.decode(self._textEncoding, 'replace')
except UnicodeError: pass
except AttributeError: pass
        
# prevent other threads from stomping all over us.
self._respondLock.acquire()
```

首先进行常规的输入检测，保证输入内容不为空、编码为 Unicode，并且通过 python 自带的线程处理类对资源进行加锁处理。关于 `self._respondLock.acquire()` 详情参考 [Python线程同步机制](http://yoyzhou.github.io/blog/2013/02/28/python-threads-synchronization-locks/) 。

之后的代码

```python
# Add the session, if it doesn't already exist
self._addSession(sessionID)
```

是对于 self._sessions 维护的一部分。 **\_sessions 负责保存多次会话的详细内容**，用于 that、topic 等标签的匹配。默认的会话都保存在 sessionID 为 "\_global" 的记录中。

!>  **实际上，respond 功能含有大量的对 _sessions 的维护。在这里先将匹配过程抽离出来进行分析，并认为使用到的 _sessions 内容已经维护过。**

接下来通过

```python
# split the input into discrete sentences
sentences = Utils.sentences(input)
```

对用户输入的多句话进行分割，借助标点符号完成。ALICE 将对每句话进行分别回答。



## 匹配过程

在 respond 函数中调用 _respond 函数，进行真正的工作：

```python
response = self._respond(s, sessionID)
```

### `Kernel._respond 方法`

由于会话是第一次发生，在 Kernel._respond 函数中获取到代表输出历史记录的 outputHistory 为空列表。相应的，获取到的 that 内容为空字符串。

```python
outputHistory = self.getPredicate(self._outputHistory, sessionID)
try: that = outputHistory[-1]
except IndexError: that = ""
```

同理，紧接着获取的 topic 也是空字符串。

继续向下，调用 PatternMgr 中的 match 方法进行最终回复的确认：

```python
response = ""
elem = self._brain.match(subbedInput, subbedThat, subbedTopic)
```

传入参数中 subbedThat、subbedTopic 分别是对 that、topic 进行规范化词语替换得到（参考下方详细分析）。



### `PatternMgr.match 方法`

该方法中对每个单句进行初步处理，之后会调用 _match 方法进行匹配。

```python
if len(pattern) == 0:
	return None
			
input = string.upper(pattern)
input = re.sub(self._puncStripRE, " ", input)
```

确认句子不是空字符串后，将句子转换为全大写字母，并去除标点符号。

当检查到 that 和 topic （上一函数中的 subbedThat、subbedTopic ）为空时，分别为它们进行赋值处理：

```python
if that.strip() == u"": that = u"ULTRABOGUSDUMMYTHAT"
	
# 省略中间步骤

if topic.strip() == u"": topic = u"ULTRABOGUSDUMMYTOPIC"
```

接下来调用 _match 方法，获得

```python
patMatch, template = self._match(input.split(), thatInput.split(), topicInput.split(), self._root)
```



### `PatternMgr._match 方法`

在 Kernel.respond 中用户的输入被拆分为一个个句子进行处理，在 _match 方法中这些句子进一步被拆分为一个个单词进行匹配。

此时函数入口：

```python
def _match(self, words, thatWords, topicWords, root):
```

参数 words，thatWords，topicWords 因为被 string.split 处理过，分别为三个字符串列表 `[u'USER', u'QUESTION']` ，`[u'ULTRABOGUSDUMMYTHAT']` ，`[u'ULTRABOGUSDUMMYTOPIC']` ；参数 root 即通过读取 aiml 文件构建出的树形结构，参考 [规则树构建](learn函数生成元素树的分析.md) 。

![](assets/respond-1.jpg)

由于初始 words 不为空，跳过一段代码，执行：

```python
first = words[0]
suffix = words[1:]
```

first 取第一个单词 "USER"，suffix 为剩余列表 `[u'QUESTION']` 。

首先检查 root 中是否含有 "\_" 符号，"\_" 可以匹配任意一个单词。

```python
# Note: this is causing problems in the standard AIML set, and is
# currently disabled.
if root.has_key(self._UNDERSCORE):
	for j in range(len(suffix)+1):
		suf = suffix[j:]
		pattern, template = self._match(suf, thatWords, topicWords, root[self._UNDERSCORE])
		if template is not None:
			newPattern = [self._UNDERSCORE] + pattern
			return (newPattern, template)
```

如果在树中遇到一个 "\_" 结点，将从 suffix 的后一个元素开始继续匹配。根据注释，似乎现在的 pyaiml 代码对标准 aiml 集中的 "\_"解析会造成错误。关于 "\_" 的部分不做过多解释，接下来开始对 first 的匹配。

```python
if root.has_key(first):
	pattern, template = self._match(suffix, thatWords, topicWords, root[first])
	if template is not None:
		newPattern = [first] + pattern
		return (newPattern, template)
```

递归一次，现在 first 的内容是 "QUESTION"，suffix 为空列表。

!> _match 方法是一个递归函数，每次调用都会进入数的下一层结点。通过不断调用自己，逐层向下遍历树形结构进行匹配。

当前的匹配情况如下：

![](assets/respond-2.jpg)

当 _match 再一次递归时，words 已经成为空列表，进入最开始部分的代码段。

```python
if len(words) == 0:
	pattern = []
	template = None
	if len(thatWords) > 0:
		try:
			pattern, template = self._match(thatWords, [], topicWords, root[self._THAT])
			if pattern != None:
				pattern = [self._THAT] + pattern
		except KeyError:
			pattern = []
```

事实上，这里的代码匹配过程也是一种有限状态机的状态转换过程。由于输入单词用尽，解析方法进入了解析 that 的阶段。而能够成功匹配的条件就是：语法树此时也进入到了记录 that 的结点。

![](assets/respond-4.jpg)

!> **两个状态机同步进行状态转换，最终完成结果的索引。**

代码完成了又一次 _match 方法的递归，即进行了结点的下移，此时的情形如下：

![](assets/respond-3.jpg)

注意参数填写的顺序，此时 that 充当了 words，但这并不是状态回退，而是为了起到复用代码的作用。

经过多次判断，程序运行到了：

```python
if root.has_key(self._STAR):
	for j in range(len(suffix)+1):
		suf = suffix[j:]
		pattern, template = self._match(suf, thatWords, topicWords, root[self._STAR])
```

经过这步递归调用，_STAR （即 "\*" 通配符）“吃掉”了 that 中的一个单词内容。

随着程序检查到 words 和 that 的内容均为空，状态转换到了 topic 的匹配阶段。这一阶段与 that 相同，不做赘述。

最后一次的递归调用，原始输入的 words、that、topic 全部用尽，程序开始进行 template 状态的匹配：

```python
if template == None:
	pattern = []
	try: template = root[self._TEMPLATE]
	except KeyError: template

return (pattern, template)
```

至此，我们获取到了 template 中的内容，列表 `['template', {}, ['text', {'xml:space': 'default'}, u' hello ']]` ，与之同时记录的是为空列表的 pattern 。

递归开始不断向上返回：

```python
if template is not None:
	newPattern = [self._STAR] + pattern
	return (newPattern, template)
```

对 _STAR 的匹配向 pattern 追加了 "\*" 的记录（表示为整数 1）。随着递归栈的弹出，pattern 也不断被写入栈中的记录。

……然而在 match 返回时居然把 pattern 给丢了？！我调试追踪容易么我！



### `使用 _processElement 整合 template 内容`

敬请期待……


## 维护 _sessions (会话记录)



## 使用 sub 方法进行词语替换

