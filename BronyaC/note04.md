##### 250315
#### 头部

<meta name="BronyaC" content="HTML笔记">


|Kind|use|
|-----|-------|
|`<title>`|定义了不同文档的标题|
|`<base>`|HTML文档中所有的链接标签的默认链接|
|`<link>`|定义文档与外部的联系|
|`<style>`|定义HTML文档的样式文件引用地址|
|`<meta>`|指定网页的描述，关键词，文件的最后修改时间，作者，和其他元数据|

<hr>

### CSS
##### 250318
<i>Cascading Style Sheets</i>

|type|use|
|-----|-----|
|background-color|背景颜色|
|font-family|字体|
|color|颜色|
|font-size|字体大小|
|text-align|文字对齐|



<body>
<h2 style="background-color:#FFFFCD;text-align:center;color:#292421">这是一个标题</h2>
<p style="background-color:#808A87;">这是一个段落。</p>
<h1 style="font-family:verdana;">一个标题</h1>
<p style="font-family:arial;color:red;font-size:20px;">一个段落。</p>
</body>

CSS修饰标签的样式，有 "内联" 和 "外引" 两种方式。

对于大部分标签，以上两种方法均可，且修改父级标签，子级标签特性也会改变。但某些标签确无法通过修改父级标签来改变子级标签特性，如a标签，修改其颜色特性，必须直接修改 a 标签的特性才可。

<a herf="https://www.runoob.com/html/html-css.html">具体参考</a>
