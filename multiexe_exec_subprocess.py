from subprocess import Popen, CREATE_NO_WINDOW, STARTUPINFO, STARTF_USESHOWWINDOW
import psutil
import logging
from pathlib import Path

# 设置日志
log_file = Path(__file__).parent / "multiexe_exec.log"
logging.basicConfig(
    level=logging.INFO,  # 将日志级别改为 DEBUG 以获取更多信息
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=str(log_file),
    filemode='a',
    encoding='utf-8'  # 指定 UTF-8 编码
)

def is_process_running(command):
    """
    检查给定命令的进程是否已经在运行
    """
    logging.debug(f"正在检查进程: {command}")
    for process in psutil.process_iter(['name', 'exe', 'cmdline']):
        try:
            # 检查进程名称、可执行文件路径或命令行
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

commands = [
    r"D:\Program Files (x86)\FreeCommander XE\FreeCommander.exe",
    r"D:\Program Files (x86)\WizNoteOld\Wiz.exe",
    r"D:\Program Files (x86)\WizNote\WizNote.exe",
    # r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    # r"C:\Users\Administrator\AppData\Local\Programs\WorkFlowy\WorkFlowy.exe",
    r"C:\Program Files\Microsoft VS Code\Code.exe"
]

# 创建 STARTUPINFO 对象
startupinfo = STARTUPINFO()
startupinfo.dwFlags |= STARTF_USESHOWWINDOW
startupinfo.wShowWindow = 0  # SW_HIDE

processes = []
for cmd in commands:
    try:
        if not is_process_running(cmd):
            try:
                proc = Popen(cmd, startupinfo=startupinfo, creationflags=CREATE_NO_WINDOW)
                processes.append(proc)
                logging.info(f"成功启动进程：{cmd}")
            except Exception as e:
                logging.error(f"启动进程时出错 {cmd}: {str(e)}")
        else:
            logging.info(f"进程已在运行，跳过启动：{cmd}")
    except Exception as e:
        logging.error(f"检查进程时出错 {cmd}: {str(e)}")

# 如果需要保存进程引用，可以使用 processes 列表

logging.info("脚本执行完毕")
