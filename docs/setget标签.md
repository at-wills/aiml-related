# AIML - &lt;set&gt;, &lt;get&gt; 标签

**&lt;set&gt; **和 **&lt;get&gt; **标签用于在 AIML 中使用变量。变量可以是预定义变量，或是程序员创建的变量。

## 语法

&lt;set&gt; 标签用于为变量赋值。

```xml
<set name = "variable-name"> variable-value </set>
```

&lt;get&gt; 标签用于从变量取值。

```xml
<get name = "variable-name"></get>
```

## 例子

**setget.aiml**

```xml
<?xml version = "1.0" encoding = "UTF-8"?>
<aiml version = "1.0.1" encoding = "UTF-8"?>
   <category>
      <pattern>I am *</pattern>
      <template>
         Hello <set name = "username"> <star/>! </set>
      </template>  
   </category>  

   <category>
      <pattern>Good Night</pattern>
      <template>
         Hi <get name = "username"/> Thanks for the conversation!
      </template>  
   </category>  

</aiml>
```

## 对话

```
Human: I am Mahesh
Robot: Hello Mahesh!
Human: Good Night
Robot: Good Night Mahesh! Thanks for the conversation!
```