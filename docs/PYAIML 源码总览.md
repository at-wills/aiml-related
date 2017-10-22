# PYAIML 源码总览

PYAIML 源码可以直接通过 pip 安装的 aiml 包获得，当然你也可以从[这里](https://github.com/at-wills/aiml-related) 获得我们即将分析的代码。由 pip 直接安装得到 PYAIML 是只支持英文聊天，后面我们将为其添加中文聊天的功能。

## 项目目录结构

PYAIML 项目的目录结构如下，主要分两部分。一是 AIML 的解析代码，该部分定义了 AIML 的语法规则以及解析规则，是 AIML 的核心代码部分；一是 AIML 语料库，该部分定义了机器人的问答规则，是机器人的“主脑”。

```

```

## 项目运行测试

测试代码如下

```py
# -*- coding: utf-8 -*-
import aiml
import os

alice_path = './aiml/alice/'
# 切换到语料库所在目录
os.chdir(alice_path)

alice = aiml.Kernel()
alice.learn("startup.xml")
alice.respond('LOAD ALICE')

while True:
    print alice.respond(raw_input(">> "))
```

测试结果

![](/assets/test_answer.png)

从上面的聊天中可以看到，聊天在一定程度上还是比较流畅。当然，AIML 应用在聊天上，由于聊天是相对开放的领域，涉及的内容五花八门，这对我们机器人的匹配规则是相当大的挑战。

## 核心代码解析思路

核心代码部分主要包括以下文件

* AimlParser.py —— aiml语法解析类
* DefaultSubs.py —— 默认aiml英语替换词列表
* Kernel.py —— aiml内核，对外的统一接口
* PatternMgr.py —— 匹配规则管理类，也是程序的“大脑”
* Utils.py —— 工具函数文件
* WordSub.py —— 替换词列表管理类

为了便于理清楚思路，我们将根据之前的测试代码，对 PYAIML 一个完整的启动、问答过程进行代码跟踪分析。其中，DefaultSubs.py 中只是对英语替换词内容的定义，而 Utils.py 只是代码工具函数文件，都将不进行分析。其次，WordSub.py 中对替换词列表采用简单字典维护，替换规则也是一般的正则表达式替换，这些后面都将一笔带过。

从之前的测试代码可以看出，AMIL 一个最简单的启动、问答分为两步，在先获取 PYAIML 的 Kernel 核心对外接口的前提下，先调用 learn 函数从制定的文件中学习匹配规则，然后调用 respond 函数进行问答。因此，我们需要关注的便是 PYAIML Kernel 的 learn 以及 respond 两大过程。
