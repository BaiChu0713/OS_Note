# HTML make a cat website
> 详情过程可参照freecodecamp，本条仅作为个人学习记录

### Step 1 标题

> html标签中的`<h>...</h>`为标题，可以从一级到六级

### Step 2 正文
`<p>...</p>`

### Step 3 注释
`<!-- something to write -->`

### Step 4 main
main 元素用于表示 HTML 文档正文的主要内容。 main 元素里的内容应该是文档中唯一的，不应该在文档的其他部分重复。

### Step 5 缩进

 h1 元素、h2 元素、注释和 p 元素嵌套在 main 元素中。 这叫作嵌套。 被嵌套的元素（子元素）应放在嵌套它的元素（父元素）的右侧两个空格处。 这种间距叫作缩进，用于使 HTML 更容易阅读。
 ```
 <html>
  <body>
   <main>
    <h1>CatPhotoApp</h1>
    <h2>Cat Photos</h2>
    <!-- TODO: Add link to cat photos -->
    <p>Everyone loves cute cats online!</p>
  </main>
 </body>
 </html>
```

### Step 6 img

使用 img 元素来为网站添加图片。
img 元素只有一个开始标签，没有结束标签。 一个没有结束标签的元素被称为空元素。
`<img src="https://cdn.freecodecamp.org/curriculum/cat-photo-app/relaxing-cat.jpg" alt="A cute orange cat lying on its back">`

HTML 属性是写在一个元素的开始标签中的特殊词汇，它们用于控制这个元素的行为。

- img 元素中的 **src** 属性明确了一个图片的 URL（图片所在的位置）

- **alt** 属性的文本（值）有两个作用
  1. 第一个作用是让屏幕阅读器可以知晓图片的内容，这会对网页的可访问性有很大提升
  2. 另一个作用是当图片无法加载时，页面需要显示的替代文本。

### Step 7 herf

要在新标签页中打开链接，你可以在锚元素（a）中使用 target 属性。

target 属性指定了在哪里打开链接文档。 target="_blank" 意思是在新标签页或窗口中打开链接的文档。

`<p>See more <a href="https://freecatphotoapp.com" target="_blank">cat photos</a> in our gallery.</p>`

在之前的步骤中，使用了锚元素将文本转换为链接。 也可以把其他类型的内容放在锚标签中，将其转换成一个链接。

### Step 8 section

section 元素用于在文档中定义各部分，如章节、标题、页脚或文档的任何其他部分。 它是一个对 SEO 和无障碍特性有帮助的语义元素。

```
<main>
  <h1>CatPhotoApp</h1>
  <section>
    <h2>Cat Photos</h2>
    <p>Everyone loves <a href="https://cdn.freecodecamp.org/curriculum/cat-photo-app/running-cats.jpg">cute cats</a> online!</p>
    <p>See more <a target="_blank" href="https://freecatphotoapp.com">cat photos</a> in our gallery.</p>
    <a href="https://freecatphotoapp.com"><img src="https://cdn.freecodecamp.org/curriculum/cat-photo-app/relaxing-cat.jpg" alt="A cute orange cat lying on its back."></a>
  </section>
</main>
```

### Step 9 ul li / ol li

- 创建一个无序项目列表，可以使用 **ul** 元素
- **li** 元素用于在有序或无序列表中创建一个列表项。

有序列表（**ol**）的代码类似于无序列表，但有序列表中的列表项在显示时会被编号
```
<ol>
  <li>flea treatment</li>
  <li>thunder</li>
  <li>other cats</li>
</ol>
```

### Step 10 figure

> figure 元素代表自包含的内容，允许您将图像与标题相关联。

`<figure><img src="https://cdn.freecodecamp.org/curriculum/cat-photo-app/lasagna.jpg" alt="A slice of lasagna on a plate."></figure>`

- `figcaption` 用于添加标题以描述 figure 元素中包含的图像。**图像标题**

### Step 11 em

> 强调一个特定的单词或短语

```
<figure>
          <img src="https://cdn.freecodecamp.org/curriculum/cat-photo-app/lasagna.jpg" alt="A slice of lasagna on a plate.">
          <figcaption>Cats <em>love</em> lasagna.</figcaption>
</figure>
```


### Step 12 Strong
>strong 元素用于指示某些文本非常重要或紧急

`<figcaption>Cats <strong>hate</strong> other cats.</figcaption>  `

## web 表单

### Step 13 form
>form 元素用于从用户获取信息，如姓名、电子邮件和其他详细信息

- action 属性指定应该将表单数据发送到哪里

- input从表单里面获得输入值
  - type属性是选择输入值的变量类型
  - name 属性，并为其赋值来表示提交的数据（输入的变量的变量名）
    - 可以同时选择两个单选按钮。 为了在选择一个单选按钮时自动取消选择另一个，两个按钮必须有值相同的 name 属性(type="radio")
  - placeholder 占位符文本，用于提示人们在输入框中输入什么样的信息
  - 防止用户在缺少所需信息时提交表单————required
  - 默认选这个————checked

`<input type="radio"> Indoor`

|type|use|
|-|-|
|radio|单选(多选一)|
|text|文本框|
|checkbox|可能有多个答案的问题|

### Step 14 button


`<button>Submit</button>`
单击没有任何属性的表单按钮的默认行为会将表单提交到表单的 action 属性中指定的位置。

type=submit时相当于提交信息

### Step 15 label

>label 元素用于帮助将 input 元素的文本与 input 元素本身关联起来

`<label><input id="outdoor" type="radio"> Outdoor</label>`

 input 元素的文本与元素本身相关联。
 可以将文本嵌套在 label 元素中，并添加与 input 元素的 id 属性具有相同值的 for 属性。
```
<input id="loving" type="checkbox" >
<label for="loving">Loving</label>
```

### Step 16 Fieldset
  - **legend** 元素充当 fieldset 元素中内容的标题。
    它为用户提供了应该在表单的该部分中输入什么的上下文

>fieldset 用于在 Web 表单中将相关的输入和标签组合在一起。

>fieldset 是块级元素，这意味着它们出现在新的一行上

### Step 17 footer

>footer 元素用于定义文档或章节的页脚。
>页脚通常包含文档作者信息、版权数据、使用条款链接、联系信息等

位置通常在`</main>`后面

### Step 18 head

>head 元素用于包含文档的元数据，如标题、样式表链接和脚本。
>元数据是没有直接显示在页面上的页面信息

- title 元素决定了浏览器在页面的标题栏或选项卡中显示的内容
- meta 元素来设置浏览器行为(eg.charset设置属性值为 utf-8，这告诉浏览器本网页使用什么字符编码)

### Step 19 html

页面的全部内容都嵌套在 html 元素中。 html 元素是 HTML 页面的根元素，包含页面上的所有内容。

你还可以通过给 html 元素添加 lang 属性来指定页面的语言。

将值为 en 的 lang 属性添加到开始 html 标签以指定页面的语言为英语。

### Step 20 开头
`<!DOCTYPE html>`被称为声明，确保浏览器尝试满足行业规范。

`<!DOCTYPE html> `告诉浏览器该文档是一个 HTML5 文档，是最新版的 HTML。
