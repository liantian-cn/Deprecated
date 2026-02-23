# Fornsigtuna

一个简单的简繁转换工具，但不同于常见的转换工具针对字进行转换，这个工具针对詞。 比如大陆写“源代码”，台湾写“原始碼”。

使用了https://github.com/BYVoid/OpenCC的字典

比如：


简体：
```
我在Github发布了简繁转换程序Fornsigtuna的源代码，
Fornsigtuna使用了OpenCC的简繁转化表，可以转换出更加本地化的的简体和繁体。
```

简体 > 繁体(`源代码`被转换为`源代碼`)：
```
我在Github發佈了簡繁轉換程序Fornsigtuna的源代碼，
Fornsigtuna使用了OpenCC的簡繁轉化表，可以轉換出更加本地化的的簡體和繁體。
```

简体 > 台湾繁体(`源代码`被转换为`原始碼`，`發佈`变成了`釋出`):
```
我在Github釋出了簡繁轉換程式Fornsigtuna的原始碼，
Fornsigtuna使用了OpenCC的簡繁轉化表，可以轉換出更加本地化的的簡體和繁體。
```

简体 > 香港繁体(`布`被转换为`佈`)：
```
我在Github發佈了簡繁轉換程序Fornsigtuna的源代碼，
Fornsigtuna使用了OpenCC的簡繁轉化表，可以轉換出更加本地化的的簡體和繁體。
```



demo地址：[https://zh-conv.liantian.me/](https://zh-conv.liantian.me/ "https://zh-conv.liantian.me/")

Blog : https://liantian.me/post/fornsigtuna-working-on-gae-s-chinese-simplified-and-traditional-conversion-api/


![Powered by Google App Engine](https://cloud.google.com/appengine/images/appengine-noborder-120x30.gif)
