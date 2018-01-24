# LOAD ALICE 与 Kernel.learn 方法

在最初的测试程序中，使用了如下语句进行 AIML 机器人的初始化加载：

```python
alice = aiml.Kernel()
alice.learn("startup.xml")
alice.respond('LOAD ALICE')
```

以下介绍机制。

## startup.xml

事实上，这个 xml 文件与普通的 aiml 文件结构完全一致，但是其中的 **template** 标签嵌套了大量的 **learn** 标签。

```xml
<aiml version="1.0">
<category>
<pattern>LOAD ALICE</pattern>
<template>

<learn>ai.aiml</learn>
<learn>drugs.aiml</learn>
<!-- 省略 -->
<learn>pickup.aiml</learn>
<learn>salutations.aiml</learn>

</template>
</category>
</aiml>
```

结合之前的内容可以知道，进行最初的 `alice.learn("startup.xml")` 学习后，形成的 brain.root 字典含有单一的 key “LOAD”，并向下嵌套，形成实际上的单一枝条的树形结构。末端记录的内容即 template 标签中的 `<learn>ai.aiml ...salutations.aiml</learn>` 与其他内容。

> 参考 [对 learn 函数中生成元素树的分析](learn函数生成元素树的分析.md) 。



## respond('LOAD ALICE')

程序向下执行，在 `alice.respond('LOAD ALICE')` 语句中，当迭代读取至内层数据

```xml
['learn', {}, ['text', {'xml:space': 'default'}, u'ai.aiml']]
```

时，调用 _processElement 方法进行相应的操作。

> 参考 [基本的 respond 过程分析 - _processElement 整合内容](http://127.0.0.1:3000/#/respond%E8%BF%87%E7%A8%8B%E5%88%86%E6%9E%90?id=_processelement-%e6%95%b4%e5%90%88%e5%86%85%e5%ae%b9)

对应于 learn 标签的方法是 `_processLearn` ，它再次调用了 Kernel.learn 方法。此时标签内容作为学习的文件名传入。

!>应该注意一点的是，在 learn 方法读入 aiml 文件的时候，采用了 python 中的 **glob** 模块。由于传入参数仅有文件名，因此当前的 python 执行路径必须定于在语料库文件夹下。所以需要使用 `os.chdir` 函数更改当前工作路径。

