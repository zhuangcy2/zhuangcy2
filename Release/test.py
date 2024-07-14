import ctypes
import tkinter as tk
from tkinter import simpledialog, messagebox

# 使用DLL文件的完整路径
dll_path = r'E:\PythonCode\jiguang\Release\MarkEzd.dll'
try:
    ezcad = ctypes.WinDLL(dll_path)
except OSError as e:
    print(f"加载DLL失败: {e}")
    exit(1)

# 定义返回值和参数类型
try:
    ezcad.lmc1_Initial.argtypes = [ctypes.c_char_p]
    ezcad.lmc1_Initial.restype = ctypes.c_int
    ezcad.lmc1_SetDevCfg.argtypes = [ctypes.c_int]
    ezcad.lmc1_SetDevCfg.restype = ctypes.c_int
    ezcad.lmc1_LoadEzdFile.argtypes = [ctypes.c_char_p]
    ezcad.lmc1_LoadEzdFile.restype = ctypes.c_int
    ezcad.lmc1_ChangeTextByName.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    ezcad.lmc1_ChangeTextByName.restype = ctypes.c_int
    ezcad.lmc1_Mark.restype = ctypes.c_int
    ezcad.lmc1_Close.restype = ctypes.c_int
except AttributeError as e:
    print(f"设置函数参数和返回值类型时出错: {e}")
    exit(1)

# 初始化控制卡
try:
    result = ezcad.lmc1_Initial(b'')
    if result != 0:
        print("初始化失败，错误代码：", result)
    else:
        print("初始化成功")
except AttributeError as e:
    print(f"函数 lmc1_Initial 不存在: {e}")
except OSError as e:
    print(f"初始化控制卡失败: {e}")

# 弹出输入框并获取用户输入
def get_user_input():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    user_input = simpledialog.askstring("输入框", "请输入标刻数据：")
    if user_input:
        return user_input.encode('gbk')  # 假设需要GBK编码
    else:
        messagebox.showerror("错误", "输入不能为空")
        exit(1)

# 设置设备参数
try:
    param = 0  # 根据实际需要设置参数
    result = ezcad.lmc1_SetDevCfg(param)
    if result != 0:
        print("设置设备参数失败，错误代码：", result)
    else:
        print("设置设备参数成功")
except AttributeError as e:
    print(f"函数 lmc1_SetDevCfg 不存在: {e}")
except OSError as e:
    print(f"调用函数时发生错误: {e}")

# 加载文件并进行标刻
try:
    file_path = b'E:\\PythonCode\\jiguang\\Release\\test.ezd'  # 模板文件路径
    result = ezcad.lmc1_LoadEzdFile(file_path)
    if result != 0:
        print("加载文件失败，错误代码：", result)
    else:
        print("加载文件成功")

        # 获取用户输入并进行标刻
        user_input = get_user_input()

        # 假设模板文件中有一个对象名为 'TextObject'
        object_name = b'TextObject'  # 根据实际对象名称调整
        result = ezcad.lmc1_ChangeTextByName(object_name, user_input)
        if result != 0:
            print("设置文本失败，错误代码：", result)
        else:
            print("设置文本成功")

            # 开始标刻
            result = ezcad.lmc1_Mark()
            if result != 0:
                print("标刻失败，错误代码：", result)
            else:
                print("标刻成功")
except AttributeError as e:
    print(f"函数 lmc1_LoadEzdFile 不存在: {e}")
except OSError as e:
    print(f"加载文件时发生错误: {e}")

# 关闭控制卡
try:
    result = ezcad.lmc1_Close()
    if result != 0:
        print("关闭控制卡失败，错误代码：", result)
    else:
        print("关闭控制卡成功")
except AttributeError as e:
    print(f"函数 lmc1_Close 不存在: {e}")
except OSError as e:
    print(f"关闭控制卡时发生错误: {e}")
