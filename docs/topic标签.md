# AIML - &lt;topic&gt; 标签

**&lt;topic&gt; **标签用于在 AIML 中储存一份上下文，这样之后的对话可以基于此上下文进行。通常，**&lt;topic&gt; **用于 **Yes/No 类型会话**。它帮助 AIML 在一个主题的上下文中搜索类别 \(category\)。

## 语法

使用 &lt;set&gt; 标签定义主题：

```xml
<template> 
   <set name = "topic"> topic-name </set>
</template>
```

使用 &lt;topic&gt; 标签修饰类别：

```xml
<topic name = "topic-name">
   <category>
      ...
   </category>     
</topic>
```

考虑如下对话：

```
Human: let discuss movies
Robot: Yes movies
Human: Comedy movies are nice to watch
Robot: Watching good movie refreshes our minds.
Human: I like watching comedy
Robot: I too like watching comedy.
```

此处机器人以 "movie" 作为回复的主题。

## 例子

```xml
<?xml version = "1.0" encoding = "UTF-8"?>
<aiml version = "1.0.1" encoding = "UTF-8"?>
   <category>
      <pattern>LET DISCUSS MOVIES</pattern>
      <template>Yes <set name = "topic">movies</set></template>  
   </category>

   <topic name = "movies">
      <category>
         <pattern> * </pattern>
         <template>Watching good movie refreshes our minds.</template>
      </category>

      <category>
         <pattern> I LIKE WATCHING COMEDY! </pattern>
         <template>I like comedy movies too.</template>
      </category>

   </topic>
</aiml>
```

#### 对话：

```
Human: let discuss movies
Robot: Yes movies
Human: Comedy movies are nice to watch
Robot: Watching good movie refreshes our minds.
Human: I like watching comedy
Robot: I too like watching comedy.
```



