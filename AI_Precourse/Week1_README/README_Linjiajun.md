# 第一节课的收获

​																						    林佳俊

**1.AI学习资源**

1.fast.ai  -- making neural nets uncool again
 <https://www.fast.ai/>

2.Udacity
 <https://cn.udacity.com/courses/all>

3.Stanford CS231n: Convolutional Neural Networks for Visual Recognition:
 <http://cs231n.stanford.edu/2017/>

4.deeplearning.ai：
 [https://www.deeplearning.ai](https://www.deeplearning.ai/)





**2.README文件**

README文件为用户提供安装指南，或相关简介等，也包括已知BUG， 常见问题和内容列表等。

通常使用markdown格式书写，常见于GitHub上的开源项目



**3.Markdown的基本语法**

- 设置**文本加粗**:要将文本设置为**粗体**，请用两个星号将其括起

- 设置文本斜体：要将文本设置为_斜体_，请在文本两旁添加下划线

- 代码标记：在代码文本两旁添加反撇号（`，不是单引号）

- 标题顺序： #（一级标题） ##（二级标题）依次类推

- 代码段：在文本前添加三个反撇号``` 

- 引用：在文本前添加符号>

- 分割线：三个或者三个以上的 - 或者 * 都可以。

- 无序列表：用 - + * 任何一种都可以

- 插入图片：

  ```
  ![图片alt](图片地址 ''图片title'')
  
  图片alt就是显示在图片下面的文字，相当于对图片内容的解释。
  图片title是图片的标题，当鼠标移到图片上时显示的内容。title可加可不加
  ```

- 超链接：

  ```
  [描述][链接地址]
  ```

  

**4.Git**

**4.1Git的安装**
Linux系统：`sudo apt get install git`

Windows系统：官网<https://git-scm.com/downloads>下载安装即可

安装完成后，还需要初次配置
```
$ git config --global user.name "Your Name"
$ git config --global user.email "email@example.com"
```

**4.2基本使用**
首先创建一个空文件夹，然后使用`git init`
```
mkdir learngit
git init
```

添加文件到版本库中，比如添加readme.md到上述的版本库中，并提交
```
vim readme.md
git add readme.md
git commit -m 'add readme.md'
```

**4.3其他常用命令**
* git log
* git status
* git diff

**4.4Pull Request的使用**
第一步，在项目首页点击`fork`按钮
第二步，克隆该远程仓库到自己电脑
```
git clone https://github.com/ricklin97/AI_Precourse_2019.git
```
第三步，添加readme文件，下一步提交修改并push到自己的github仓库
```
git add README_Linjiajun.md
git commit -m 'add readme.md'
git push origin rick_branch
```
第四步，登录github，在项目首页点击`new pull request`，将修改提交项目作者

  

**4.4学习资源**

[廖雪峰的git课程](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000)