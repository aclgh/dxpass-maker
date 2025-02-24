# dxpass-maker
基于piloow模块的dxpass生成器

![output.png](output.png)

## 简介
`dxpass-maker` 是使用python编写的命令行工具，用于生成由玩家提供参数的dxpass。

## 安装

### 环境

- Python 3.12+
- pip

### 安装依赖

1.克隆该项目；

2.下载项目的资源文件[谷歌](https://drive.google.com/file/d/1cpShLy9mk-gNMA4hg5KfdFznY-OkrgZZ/view?usp=sharing)/[私人云盘](http://aclgh.top:5212/s/pqSb)，然后将`res`文件夹复制到项目目录中；


3.在根目录下运行命令安装所需的依赖
```sh 
pip install -r requirements.txt
```

## 使用

### 通过命令行调用
以下是一个示例：
```sh 
python dxpass_gen.py --rating 15121 --friendcode 123456789 --qr 114514 --cardchara "000601" --datets 1740323711 --aime "12345678912345678912" --virsion "1.00-0001" --nickname "maimai" --dxtype "freedom" --output "./output.png"
```
| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `--rating` | int | 15121 | 玩家dxrating |
| `--friendcode` | int | 123456789 | 玩家好友码，可选项，设为None则不生成好友码一栏 |
| `--qr` | int | None | 根据字符串生成右下角二维码，留空则使用默认值 |
| `--cardchara` | string | "000601" | dxpass人物ID |
| `--datets` | int | 1740323711 | 当前的时间戳，以生成dxpass有效期 |
| `--aime` | string | "12345678912345678912" | 下方的aime卡号，要求20位 |
| `--virsion` | string | "1.00-0001" | 下方的版本号，请按默认的格式填写 |
| `--nickname` | string | "maimai" | 玩家昵称，支持中文 |
| `--dxtype` | string | "freedom" | dxpass类型，有 "bronze" "freedom" "gold" "silver"四种|
| `--output` | string | "./output.png" | 图片输出路径 |

## 特别鸣谢
[maicard-py](https://github.com/Error063/maicard)项目提供灵感

[fxysk](https://space.bilibili.com/20026067/)提供部分素材

## TODO List

### 近期

✅ - 已完成 | 🧪 - 测试中 | 🚧 - 进行中 | ⏳ - 计划中

| 状态 | 项目                             |
| ---- | --------------------------------|
|  ⏳  | 允许传入GetUserData的返回值为参数生成dxpass   |
|  ⏳  | 加入新opt的角色资源                |
|  ⏳  | 预生成opt内官方预设dxpass          |
|  ⏳  | 实现webui可以自定义组合生成dxpass   |
|  ⏳  | 实现nonebot插件                   |
