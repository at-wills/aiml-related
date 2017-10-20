# AIML - &lt;think&gt; 标签

**&lt;think&gt; **标签在不对用户产生输出语句的情况下储存变量。

## 语法

使用 &lt;think&gt; 标签储存一个变量：

```xml
<think> 
   <set name = "variable-name"> variable-value </set>
</think>
```

考虑如下对话：

```
Human: My name is Mahesh
Robot: Hello!
Human: Byeee
Robot: Hi Mahesh Thanks for the conversation!
```

## 例子

**think.aiml**

```xml
<?xml version = "1.0" encoding = "UTF-8"?>
<aiml version = "1.0.1" encoding = "UTF-8"?>
   <category>
      <pattern>My name is *</pattern>
      <template>
         Hello!<think><set name = "username"> <star/></set></think>
      </template>  
   </category>  

   <category>
      <pattern>Byeee</pattern>
      <template>
         Hi <get name = "username"/> Thanks for the conversation!
      </template>  
   </category>  

</aiml>
```



