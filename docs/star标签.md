# AIML - &lt;star&gt; 标签

**&lt;star&gt; **标签用于在 &lt;pattren&gt; 标签中匹配通配符 \* 和 \_ 。

## 语法

```xml
<star index = "n"/>
```

**n **代表 &lt;pattern&gt; 标签中用于取代用户输入的 \* 的位置。

考虑以下例子：

```xml
<category>
   <pattern> A * is a *. </pattern>

   <template>
      When a <star index = "1"/> is not a <star index = "2"/>?
   </template>

</category>
```

如果用户输入 "A mango is a fruit."，那么机器人就会回复 "When a mango is not a fruit?"

## 例子

**star.aiml**

```xml
<?xml version = "1.0" encoding = "UTF-8"?>
<aiml version = "1.0.1" encoding = "UTF-8"?>

   <category>
      <pattern>I LIKE *</pattern>
      <template>
         I too like <star/>.
      </template>
   </category>

   <category>
      <pattern>A * IS A *</pattern>
      <template>
         How <star index = "1"/> can not be a <star index = "2"/>?
      </template>
   </category>

</aiml>
```

## 对话

可以看到如下对话：

```
Human: I like mango
Robot: I too like mango.
Human: A mango is a fruit
Robot: How mango can not be a fruit?
```

&lt;star index = "1"/&gt; 常被用作 &lt;star /&gt;

