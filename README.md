# MultiExe 进程管理器

MultiExe 是一个 Python 脚本，用于批量管理和启动多个可执行文件。它能够检查指定的进程是否已经在运行，如果没有运行则以隐藏窗口的方式启动它们。

## 功能特点

- 自动检查并启动指定的可执行文件
- 避免重复启动已运行的进程
- 以隐藏窗口方式启动进程，不干扰用户界面
- 详细的日志记录，包括成功启动和错误信息
- 使用 `psutil` 库进行高效的进程检查
- 使用 Windows API 创建隐藏进程

## 依赖项

- Python 3.x
- psutil 库
- pywin32 库

## 安装

1. 克隆此仓库：
   ```bash
   git clone https://github.com/your-username/multiexe-process-manager.git
   ```

2. 安装所需的依赖：
   ```bash
   pip install psutil pywin32
   ```

## 使用方法

1. 编辑 `commands.txt` 文件，添加您想要管理的可执行文件路径，每行一个。
2. 运行脚本：
   ```bash
   python multiexe_exec_subprocess.py
   ```

## 配置

您可以通过编辑 `commands.txt` 文件来自定义要管理的可执行文件。例如：

```
D:\Program Files (x86)\FreeCommander XE\FreeCommander.exe
D:\Program Files (x86)\WizNoteOld\Wiz.exe
D:\Program Files (x86)\WizNote\WizNote.exe
C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
C:\Program Files\Microsoft VS Code\Code.exe


## 日志

脚本运行时会生成一个日志文件 `multiexe_exec.log`，记录了所有的操作和错误信息。您可以查看此文件以了解脚本的运行状况。

## 文件说明

- `multiexe_exec_subprocess.py`: 主脚本文件
- `commands.txt`: 存储要管理的可执行文件路径
- `multiexe_exec.log`: 日志文件

## 注意事项

- 请确保您有权限运行指定的可执行文件。
- 某些应用程序可能需要管理员权限才能启动。
- 脚本使用 `CREATE_NO_WINDOW` 标志来隐藏启动的进程窗口，这可能不适用于所有类型的应用程序。
