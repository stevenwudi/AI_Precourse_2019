# 课程收获

## git及github的使用
### 名词概念
- `Workspace` 工作区
- `Stage` 暂存区
- `Repository` 仓库区
- `Remote` 远程仓库
- `origin` 远程库默认名称
- `HEAD` 当前版本（上个版本用HEAD^表示）
### 常用命令
- 初始化设置
> `git config --global` 全局参数设置  
`git config --global user.name "Your Name"`  
`git config --global user.email "email@example.com"`

- 初始化仓库

> `git init`

- 克隆仓库

> `git clone`

- 添加文件或目录到暂存区

> `git add`

- 比较差异

> `git diff [filename]` 比较的是工作区文件与暂存区文件的差异  
`git diff --cached [filenam]` 比较的是暂存区的文件与上一个commit的差异  
`git diff HEAD -- [filename]` 比较的是工作区与当前分支最新commit之间的差异

- 查看文件状态

> `git status`

- 暂存区提交到仓库区

> `git commit -m [message]`

- 查看当前分支的版本历史

> `git log`

- 关于分支

> `git checkout [branch]` 切换分支  
`git checkout -b [branch]` 创建并切换到该分支  
`git checkout -b [branch] [remote]/[branch]` 需要从远程库的分支上开发时  
`git branch -d [branch]` 删除分支

- 关于撤销

> `git checkout -- [filename]`  工作区`filename`的修改撤销  
`git reset [filename]` 重置暂存区的指定文件，与上一次commit保持一致，工作区不变  
`git reset --hard`  重置暂存区与工作区，与上一次commit保持一致  
`git reset --hard commitID` 回退到某个版本（`commitID`是版本号）

- 合并

> `git merge [branch]` 合并指定分支(`[branch]`)到当前分支

- 远程仓库操作

> `git remote add [remote] [url]` 增加一个新的远程仓库，并命名 (一般是origin)  
`git push [remote] [branch]` 将(`[branch]`)分支推送到远程库  
`git pull [remote] [branch]` 取回远程仓库的变化，并与本地分支合并

- more

> 还有许多其他命令、以及复杂的参数，暂未完全理解掌握，有待补充

## markdown常用标记

- 使用`#`的不同数量，可表示1-6级标题
- 在每行加上4个空格或者一个制表符表示代码区块，需要和普通段落之间存在空行，而文本中的代码则使用反撇号`\``标注
- `*`或者`_`表示斜体
- `**`或者`__`表示粗体
- `·`、`+`、`-`标记无序列表，标记后面最少要有一个空格，必须和前方段落之间存在空行
- 分割线最常使用就是三个或以上`*`，还可以使用`-`和`_`

# 更多想做的

- 学习计算机视觉相关的知识
- 实现一个关于**手势识别**的深度学习项目