# AIML 介绍

AIML 代表 “人工智能标记语言” （Artificial Intelligence Markup Language）。AIML 由爱丽丝免费软件社区和 Richard S. Wallance 博士在 1995-2000 年开发。AIML 用来创建 Alicebot ,一个基于 A.L.I.C.E. （Artificial Linguistic Internet Computer Entity）的免费对话框软件。

## AIML 标签

| **AIML 标签**          | **描述**                        |
| :------------------- | :---------------------------- |
| **&lt;aiml&gt;**     | 定义一个 AIML 文档的开始和结束            |
| **&lt;category&gt;** | 定义 alicebot 知识库的一个知识单元        |
| **&lt;pattern&gt;**  | 定义用于匹配用户可能输入在 alicebot 中输入的模式 |
| **&lt;template&gt;** | 定义 alicebot 对用户输入的回复          |

我们将在 AIML的基本标签 中讨论每种标签。

下面是其他某些被广泛使用的 AIML 标签。我们将在接下来的章节中讨论每种标签。

| **AIML标签**            | **描述**                               |
| :-------------------- | :----------------------------------- |
| **&lt;star&gt;**      | 用来匹配在 &lt;pattern&gt; 标签中的通配符 \*     |
| **&lt;srai&gt;**      | 多用途标签，用来调用/匹配其他的 category （类别）       |
| **&lt;random&gt;**    | 用 **&lt;random&gt; **来获得随机的回复        |
| **&lt;li&gt;**        | 用来表示多个回复                             |
| **&lt;set&gt;**       | 用来在 AIML 变量中设定值                      |
| **&lt;get&gt;**       | 用来获取 AIML 变量中的值                      |
| **&lt;that&gt;**      | 在 AIML 中基于上下文回复                      |
| **&lt;think&gt;**     | 在 AIML 中对用户不输出的情况下储存一个变量             |
| **&lt;condition&gt;** | 类似于编程语言中的switch语句。它帮助 ALICE 响应所匹配的输入 |

## AIML 词典

AIML词典使用单词，空格，以及两个特殊符号 \* 和 \_ 作为通配符。比起通配符 \*， AIML 解析器偏向于匹配含有 \_ 的 pattern（模式）。AIML标签兼容 XML 语法，且大小写不敏感。

**例子**

```xml
<aiml version = "1.0.1" encoding = "UTF-8"?>
   <category>
      <pattern> HELLO ALICE </pattern>

      <template>
         Hello User!
      </template>

   </category>
</aiml>
```

下面几点需要重点注意：

- **&lt;aiml&gt;** 标签表示 AIML 文档起始
- **&lt;category&gt;** 标签定义知识单元
- **&lt;pattern&gt;** 标签定义用户输入的模式
- **&lt;template&gt;** 标签定义当用户键入 ```Hello Alice``` 时的回复

**结果**

```
User: Hello Alice
Bot: Hello User
```
