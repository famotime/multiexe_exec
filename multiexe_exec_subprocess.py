from subprocess import Popen, CREATE_NO_WINDOW
import psutil
import logging
from pathlib import Path
import win32process
import win32con

# 设置日志
log_file = Path(__file__).parent / "multiexe_exec.log"
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=str(log_file),
    filemode='a',
    encoding='utf-8'
)

def is_process_running(command):
    """
    检查给定命令的进程是否已经在运行
    """
    logging.debug(f"正在检查进程: {command}")
    for process in psutil.process_iter(['name', 'exe', 'cmdline']):
        try:
            if process.info['name']:
                if Path(command).name.lower() in process.info['name'].lower():
                    logging.debug(f"进程名匹配: {process.info['name']}")
                    return True
            if process.info['exe']:
                if command.lower() in process.info['exe'].lower():
                    logging.debug(f"可执行文件路径匹配: {process.info['exe']}")
                    return True
            if process.info['cmdline']:
                if any(command.lower() in cmd.lower() for cmd in process.info['cmdline'] if cmd):
                    logging.debug(f"命令行匹配: {process.info['cmdline']}")
                    return True
        except Exception as e:
            logging.debug(f"检查进程时出现异常: {str(e)}")
    logging.debug(f"未找到匹配的进程: {command}")
    return False

def read_commands_from_file(file_path):
    """
    从文件中读取命令列表
    """
    commands = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    commands.append(line)
    except Exception as e:
        logging.error(f"读取命令文件时出错: {str(e)}")
    return commands

# 从文件中读取命令
commands_file = Path(__file__).parent / "commands.txt"
commands = read_commands_from_file(commands_file)

processes = []
for cmd in commands:
    try:
        if not is_process_running(cmd):
            try:
                # 使用 Windows API 来创建隐藏的进程
                startup_info = win32process.STARTUPINFO()
                startup_info.dwFlags = win32process.STARTF_USESHOWWINDOW
                startup_info.wShowWindow = win32con.SW_HIDE

                proc_info = win32process.CreateProcess(
                    None,
                    cmd,
                    None,
                    None,
                    0,
                    win32con.CREATE_NO_WINDOW,
                    None,
                    None,
                    startup_info
                )
                processes.append(proc_info)
                logging.info(f"成功启动进程：{cmd}")
            except Exception as e:
                logging.error(f"启动进程时出错 {cmd}: {str(e)}")
        else:
            logging.info(f"进程已在运行，跳过启动：{cmd}")
    except Exception as e:
        logging.error(f"检查进程时出错 {cmd}: {str(e)}")

logging.info("脚本执行完毕")
