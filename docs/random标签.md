# AIML - random 标签

**&lt;random&gt; **标签用于获得随机回复。此标签使得 AIML 对相同输入进行不同回应。&lt;random&gt; 标签与 &lt;li&gt; 标签同时使用。&lt;li&gt; 标签记录将要随机传达给用户的不同回复。

## 语法

```xml
<random>
   <li> pattern1 </li>
   <li> pattern2 </li>
   ...
   <li> patternN </li>
</random>
```

## 例子

**random.aiml**

```xml
<?xml version = "1.0" encoding = "UTF-8"?>
<aiml version = "1.0.1" encoding ="UTF-8"?>
   <category>
      <pattern>HI</pattern>

      <template>
         <random>
            <li> Hello! </li>
            <li> Hi! Nice to meet you! </li>
         </random>
      </template>

   <category>      
</aiml>
```

## 对话

```
Human: Hi
Robot: Hello!
Human: Hi
Robot: Hi! Nice to meet you!
```