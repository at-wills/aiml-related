# AIML 基本标签

在这篇教程里，我们将讨论 AIML 的基本标签。

- **&lt;aiml>** 定义 AIML 文档起止
- **&lt;category>** 定义 Alicebot 知识库的知识单元
- **&lt;pattern>** 定义用于匹配用户输入的模式
- **&lt;template>** 定义用户输入的回复
  下面的 AIML 文件作为参考

```xml
<?xml version = "1.0" encoding = "UTF-8"?>
<aiml version = "1.0.1" encoding = "UTF-8"?>
   <category>
      <pattern> HELLO ALICE </pattern>
      
      <template>
         Hello User
      </template>
      
   </category>
</aiml>
```

## ```<aiml> 标签```

&lt;aiml> 标签标记 AIML 文档的起止。标签包括版本和编码信息，储存在 version 和 encoding 属性中。版本属性储存了 ALICE 聊天机器人知识库的 AIML 的版本。例如，我们使用过 1.0.1 版本。此属性可选。

编码属性提供了文档所使用的字符集。例如，我们使用的是 UFT-8 字符集。作为强制要求，&lt;aiml> 标签必须含有至少一个 &lt;category> 标签。我们可以创建多个 AIML 文件，每个文件含有单个的 &lt;aiml> 标签。每个 AIML 文件的目的是用于增加至少一个知识单元。

```xml
<aiml version = "1.0.1" encoding = "UTF-8"?>
   ...
</aiml>
```

## ```<category> 标签```

&lt;category> 标签是 ALICE 机器人的基本知识单元。每个类别(category)包含：

- 句子形式的用户输入，可以是一个断言、问题，或者感叹句等。用户输入可以包含像是 * 或 _ 这样的通配符。
- 爱丽丝机器人回复的用户输入
- 可选的上下文

一个 &lt;category> 标签必须含有 &lt;pattern> 和 &lt;template> 标签。&lt;pattern> 表示用户输入，&lt;template> 表示机器人的回复。

```xml
<category>
   <pattern> HELLO ALICE </pattern>
   
   <template>
      Hello User
   </template>
   
</category>
```

这样，如果用户输入 **Hello Alice** ，机器人会回复 **Hello User**。

## ```<pattern> 标签```

&lt;pattern> 标签代表用户输入。它应为 &lt;category> 标签中的第一个标签。&lt;pattern> 标签可以包含通配符，来匹配多个用户输入。例如，在此例中，&lt;pattern> 包含了 ```HELLO ALICE```。

AIML 是大小写不敏感的。如果用户输入了 Hello Alice，hello alice，HELLO ALICE 等，所有的输入都是有效的，机器人都会匹配到 HELLO ALICE。

```xml
<category>
  <pattern> HELLO ALICE </pattern>
  <template>
    HELLO USER
  </template>
  <pattern>
</category>
```

模板是 "Hello User" ，表示机器人对用户输入的回复。

## ```<template> 标签```

&lt;template> 标签表示机器人对用户的回复。应为在 &lt;category> 标签中的第二个标签。&lt;template> 标签可以保存数据，调用另一个程序，给出有条件的答案，或者委托给另一个类别(category)。

```xml
<category>
  <pattern> HELLO ALICE </pattern>
  <template>
      Hello User
  </template>
</category>
```

模板是 "Hello User"，表示机器人对用户输入的回复。