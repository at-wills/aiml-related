# AIML - &lt;srai&gt; 标签

**&lt;srai&gt; **标签是一种多用途标签。这种标签使得 AIML 可以为同一个模板定义不同的目标。

## 语法

```xml
<srai> pattern </srai>
```

下面是srai 有关的常见情况：

* 减少符号 \(Symbolic Reduction\)
* 分治 \(Divide and Conquer\)
* 同义词分辨 \(Synonyms resolution\)
* 关键词检测 \(Keywords detection\)

## 减少符号

符号减少技术用于精简模式。可以减少复杂的语法模式 \(pattern\)。

例如，考虑以下情况：

```
Human: Who was Albert Einstein?
Robot: Albert Einstein was a German physicist.
Human: Who was Isaac Newton?
Robot: Isaac Newton was a English physicist and mathematician.
```

如果问题是这样的呢？

```
Human: DO YOU KNOW WHO Albert Einstein IS?
Human: DO YOU KNOW WHO Isaac Newton IS?
```

此时，**&lt;srai&gt; **标签就发挥作用了。它可以将用户的模式 \(pattern\) 作为一个模板。

### 例子

创建测试 aiml ：

**srai.aiml**

```xml
<?xml version = "1.0" encoding = "UTF-8"?>
<aiml version = "1.0.1" encoding = "UTF-8"?>
   <category>
      <pattern> WHO IS ALBERT EINSTEIN </pattern>
      <template>Albert Einstein was a German physicist.</template>
   </category>

   <category>
      <pattern> WHO IS Isaac NEWTON </pattern>
      <template>Isaac Newton was a English physicist and mathematician.</template>
   </category>

   <category>
      <pattern>DO YOU KNOW WHO * IS</pattern>
      <template>
         <srai>WHO IS <star/></srai>
      </template>
   </category>
</aiml>
```

### 对话

对话如下：

```
Human: Do you know who Albert Einstein is
Robot: Albert Einstein was a German physicist.
```

## 分治

分治策略用于在进行完整回答时复用子句，有助于减少定义多个类别 \(category\)。

考虑以下对话：

```
Human: Bye
Robot: GoodBye!
Human: Bye Alice!
Robot: GoodBye!
```

机器人应在用户于句首使用 **Bye** 时回复 **Goodbye！**。

在这里使用 &lt;srai&gt; 标签。

### 例子

```xml
<?xml version = "1.0" encoding = "UTF-8"?>
<aiml version = "1.0.1" encoding = "UTF-8"?>
   <category>
      <pattern>BYE</pattern>
      <template>Good Bye!</template>
   </category>

   <category>
      <pattern>BYE *</pattern>
      <template>
         <srai>BYE</srai>
      </template>
   </category>

</aiml>
```

### 对话

```
Human: Bye
Robot: GoodBye!
Human: Bye Alice!
Robot: GoodBye!
```

## 同义词分辨

机器人应对含义相似的词进行相同回复。

例如

```
Human: Factory
Robot: Development Center!
Human: Industry
Robot: Development Center!
```

无论用户说 **Factory **还是** Industry **机器人都应回复 **Development Center!**。

### 例子

```xml
<?xml version = "1.0" encoding = "UTF-8"?>
<aiml version = "1.0.1" encoding = "UTF-8"?>
   <category>
      <pattern>FACTORY</pattern>
      <template>Development Center!</template>
   </category>

   <category>
      <pattern>INDUSTRY</pattern>
      <template>
         <srai>FACTORY</srai>
      </template>
   </category>

</aiml>
```

### 对话

```
Human: Factory
Robot: Development Center!
Human: Industry
Robot: Development Center!
```

## 同义词检测

使用 **srai**，我们可以为特定关键词的用户输入进行相同的回复，不论关键词出现在句子的什么位置。

### 例子

```xml
<?xml version = "1.0" encoding = "UTF-8"?>
<aiml version = "1.0.1" encoding = "UTF-8"?>   
   <category>
      <pattern>SCHOOL</pattern>
      <template>School is an important institution in a child's life.</template>
   </category>  

   <category>
      <pattern>_ SCHOOL</pattern>
      <template>
         <srai>SCHOOL</srai>
      </template>
   </category>

   <category>
      <pattern>_ SCHOOL</pattern>
      <template>
         <srai>SCHOOL</srai>
      </template>
   </category>

   <category>
      <pattern>SCHOOL *</pattern>
      <template>
         <srai>SCHOOL</srai>
      </template>
   </category>

   <category>
      <pattern>_ SCHOOL *</pattern>
      <template>
         <srai>SCHOOL</srai>
      </template>
   </category>

</aiml>
```

### 对话

```
Human: I love going to school daily.
Robot: School is an important institution in a child's life.
Human: I like my school.
Robot: School is an important institution in a child's life.
```



