# AIML - &lt;condition&gt; 标签

**&lt;condition&gt;** 标签类似编程语言中的 switch 语句。它帮助 ALICE 回复匹配的输入。

## 语法

```xml
<condition name = "variable-name" value = "variable-value"/>
```

## 对话

```
Human: How are you feeling today
Robot: I am happy!
```

将 **happy** 作为 ALICE 的状态，从而回答 "I am happy!"。



## 例子

**condition.aiml**

```xml
<?xml version = "1.0" encoding = "UTF-8"?>
<aiml version = "1.0.1" encoding = "UTF-8"?>
   <category>
      <pattern> HOW ARE YOU FEELING TODAY </pattern>
      
      <template>
         <think><set name = "state"> happy</set></think>
         <condition name = "state" value = "happy">
            I am happy!
         </condition>
         
         <condition name = "state" value = "sad">
            I am sad!
         </condition>
      </template>
      
   </category>
</aiml>
```



