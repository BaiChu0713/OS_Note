# Step 1 Style


# Step 2 类型选择器

```
<style>
  h1{
  text-align:center;
  }
</style>
```

可以通过在 style 元素中指定元素并为其设置属性来向元素添加样式

|style|Use|
|-|-|
|text_align|字体位置|
|backround-color|背景颜色|
|width|宽度（可以用px或者百分比|
|margin-left|左边距|
|margin-right|右边距（类）|
|padding-left|外沿距离（页面)|
|border|元素的外沿|
|background-image|背景图片，可以是本地的也可以是url(eg.`background-image:url(https://cdn.freecodecamp.org/curriculum/css-cafe/beans.jpg)`)|
|font-family|字体|





如果状态相似，可以将它们替换为一个选择器列表

# Step 3 css文件

> 由于会有更多的样式，因此最好将所有样式放在一个单独的文件中并链接到它

在css文件中，不需要加style标签
```
h1, h2, p {
      text-align: center;
}
```

在源文件中添加一个link链接到css文件

`<link rel="stylesheet" href="styles.css">`

同时为了普适性，可以在mata属性中制作屏幕长宽比适中

`<meta name="viewport" content="width=device-width, initial-scale=1.0"/>`

# Step 4 diy

div 元素主要用于设计布局目的，这与迄今为止使用的其他内容元素不同。

div元素可以设置id以方便应用后面的id选择器

它处于 body 内

```
<div id="menu">
      <main>
        <h1>CAMPER CAFE</h1>
        <p>Est. 2020</p>
        <section>
          <h2>Coffee</h2>
        </section>
      </main>
</div>
```
# Step 5 id选择器

id 选择器来选取具有 id 属性的特定元素

将 # 符号直接放在元素的 id 值前面，就形成了 id 选择器。

# Step 6 css注释

css内注释格式：`/* xxx */`

# Step 7 类选择器

那类选择器属性就是class=xxx（对比id选择器在html中选择id=xxx

```
.menu {
  width: 80%;
  background-color: burlywood;
  margin-left: auto;
  margin-right: auto;
}
```

# Step 8 article

>article 元素通常包含具有相关信息的多个元素。
```
<article class="item">
            <p class="flavor">French Vanilla</p>
            <p class="price">3.00</p>
          </article>
          <article>
            <p>Caramel Macchiato</p>
            <p>3.75</p>
</article>
```

p 元素嵌套在具有 item 属性的 article 元素中。

可以使用名为 item 的类嵌套在元素中任意位置的所有 p 元素的样式，如下所示：

```
.item p{
  display:inline-block;
}
```

# Step last 成品（x）
```
styles.css

body {
  background-image: url(https://cdn.freecodecamp.org/curriculum/css-cafe/beans.jpg);
  font-family: sans-serif;
  padding: 20px;
}

h1 {
  font-size: 40px;
  margin-top: 0;
  margin-bottom: 15px;
}

h2 {
  font-size: 30px;
}

.established {
  font-style: italic;
}

h1, h2, p {
  text-align: center;
}

.menu {
  width: 80%;
  background-color: burlywood;
  margin-left: auto;
  margin-right: auto;
  padding: 20px;
  max-width: 500px;
}

img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}

hr {
  height: 2px;
  background-color: brown;
  border-color: brown;
}

.bottom-line {
  margin-top: 25px;
}

h1, h2 {
  font-family: Impact, serif;
}

.item p {
  display: inline-block;
  margin-top: 5px;
  margin-bottom: 5px;
  font-size: 18px;
}

.flavor, .dessert {
  text-align: left;
  width: 75%;
}

.price {
  text-align: right;
  width: 25%;
}

/* FOOTER */

footer {
  font-size: 14px;
}

.address {
  margin-bottom: 5px;
}

a {
  color: black;
}

a:visited {
  color: black;
}

a:hover {
  color: brown;
}

a:active {
  color: brown;
}
```

```
index.html

<h2>Desserts</h2>
<img src="https://cdn.freecodecamp.org/curriculum/css-cafe/pie.jpg" alt="pie icon">
<article class="item">
  <p class="dessert">Donut</p><p class="price">1.50</p>
</article>
<article class="item">
  <p class="dessert">Cherry Pie</p><p class="price">2.75</p>
</article>
<article class="item">
  <p class="dessert">Cheesecake</p><p class="price">3.00</p>
</article>
<article class="item">
  <p class="dessert">Cinnamon Roll</p><p class="price">2.50</p>
</article>
</section>
</main>
<hr class="bottom-line">
<footer>
<p>
<a href="https://www.freecodecamp.org" target="_blank">Visit our website</a>
</p>
<p class="address">123 Free Code Camp Drive</p>
</footer>
</div>
</body>
</html>

```


# Step x css网页搭配

## 补色

请注意，红色和青色彼此相邻非常明亮。如果这种对比在网站上被过度使用，可能会分散注意力，如果将其放置在互补色背景上，则会使文本难以阅读。

## 颜色表示方法

十六进制颜色值以 # 字符开头，从 0-9 和 A-F 取六个字符。 第一对字符代表红色，第二对代表绿色，第三对代表蓝色。 例如，#4B5320。

在 .green 类选择器中，将 background-color 属性设置为十六进制颜色代码，其值 00 表示红色，FF 表示绿色，00 表示蓝色

or `rgb(x,x,x)`

or `hsl(色轮(0-240),饱和度,亮度)`

opacity——透明度======相当于rgba(a,b,c,透明度)
