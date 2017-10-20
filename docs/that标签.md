# AIML - &lt;that&gt; 标签

在 AIML 中使用 **&lt;that&gt;** 标签以基于上下文进行回复。

## 语法

```xml
<that> template </that>
```

考虑以下对话：

```
Human: Hi Alice! What about movies?
Robot: Do you like comedy movies?
Human: No
Robot: Ok! But I like comedy movies.
```



## 例子

**that.aiml**

```xml
<?xml version = "1.0" encoding = "UTF-8"?>
<aiml version = "1.0.1" encoding = "UTF-8"?>
   <category>
      <pattern>WHAT ABOUT MOVIES</pattern>
      <template>Do you like comedy movies</template>  
   </category>
   
   <category>
      <pattern>YES</pattern>
      <that>Do you like comedy movies</that>
      <template>Nice, I like comedy movies too.</template>
   </category>
   
   <category>
      <pattern>NO</pattern>
      <that>Do you like comedy movies</that>
      <template>Ok! But I like comedy movies.</template>
   </category> 
   
</aiml>
```



