import time
import datetime
import sys
import re
import random

# ===== ANSI 控制码 =====
RESET = "\033[0m"
CLEAR = "\033[2J"
HOME = "\033[H"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

# ===== 颜色 =====
BG_DARK = "\033[48;5;17m"      # 主屏背景：深蓝
BG_FIREWORKS = "\033[48;5;54m" # 烟花背景：深紫
FG_WHITE = "\033[38;5;231m"
FG_GOLD = "\033[38;5;220m"
FG_CYAN = "\033[38;5;51m"
FG_PINK = "\033[38;5;213m"
FG_RED = "\033[38;5;196m"
FG_GREEN = "\033[38;5;46m"


# # ===== 大数字模板（5行高） =====
# BIG_NUM = {
#     "0": [" ███ ","█   █","█   █","█   █"," ███ "],
#     "1": ["  █  "," ██  ","  █  ","  █  "," ███ "],
#     "2": [" ███ ","    █"," ███ ","█    ","█████"],
#     "3": ["████ ","    █"," ███ ","    █","████ "],
#     "4": ["█  █ ","█  █ ","█████","   █ ","   █ "],
#     "5": ["█████","█    ","████ ","    █","████ "],
#     "6": [" ███ ","█    ","████ ","█   █"," ███ "],
#     "7": ["█████","    █","   █ ","  █  ","  █  "],
#     "8": [" ███ ","█   █"," ███ ","█   █"," ███ "],
#     "9": [" ███ ","█   █"," ████","    █"," ███ "]
# }

# ===== 更大数字模板（9行高）用于最后10秒 =====
BIG_NUM_9 = {
    "0": [
        "  ████  ",
        " █    █ ",
        "█      █",
        "█      █",
        "█      █",
        "█      █",
        "█      █",
        " █    █ ",
        "  ████  "
    ],
    "1": [
        "   ██   ",
        "  ███   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        "   ██   ",
        " ██████ "
    ],
    "2": [
        "  ████  ",
        " █    █ ",
        "       █",
        "      █ ",
        "     █  ",
        "    █   ",
        "   █    ",
        "  █     ",
        " ███████"
    ],
    "3": [
        "  ████  ",
        " █    █ ",
        "       █",
        "     ██ ",
        "      █ ",
        "       █",
        "       █",
        " █    █ ",
        "  ████  "
    ],
    "4": [
        "     ██ ",
        "    ███ ",
        "   █ ██ ",
        "  █  ██ ",
        " █   ██ ",
        "████████",
        "     ██ ",
        "     ██ ",
        "     ██ "
    ],
    "5": [
        "███████ ",
        "█       ",
        "█       ",
        "███████ ",
        "       █",
        "       █",
        "       █",
        "█     █ ",
        " █████  "
    ],
    "6": [
        "  ████  ",
        " █    █ ",
        "█       ",
        "███████ ",
        "█      █",
        "█      █",
        "█      █",
        " █    █ ",
        "  ████  "
    ],
    "7": [
        "████████",
        "       █",
        "      █ ",
        "     █  ",
        "    █   ",
        "   █    ",
        "  █     ",
        " █      ",
        "█       "
    ],
    "8": [
        "  ████  ",
        " █    █ ",
        " █    █ ",
        "  ████  ",
        " █    █ ",
        "█      █",
        "█      █",
        " █    █ ",
        "  ████  "
    ],
    "9": [
        "  ████  ",
        " █    █ ",
        "█      █",
        "█      █",
        " █    ██",
        "  ████ █",
        "       █",
        " █    █ ",
        "  ████  "
    ]
}


def progress_bar(percent, length=36):
    filled = int(length * percent)
    bar = ""
    for i in range(length):
        if i < filled:
            bar += BG_DARK + FG_GOLD + "█" + RESET
        else:
            bar += BG_DARK + FG_WHITE + "░" + RESET
    return f"{bar} {percent*100:6.2f}%"
    
def strip_ansi(text):
    """移除ANSI颜色码"""
    return re.sub(r'\033\[[0-9;]+m', '', text)

def center_in_box(text, box_width=50, total_width=80, bg_color=BG_DARK):
    """文本居中显示，左右有背景色"""
    clean_text = strip_ansi(text)
    text_len = len(clean_text)
    padding = (box_width - text_len) // 2
    left_padding = " " * padding
    right_padding = " " * (box_width - text_len - padding)
    side_width = (total_width - box_width) // 2
    left_bg = bg_color + " " * side_width + RESET
    right_bg = bg_color + " " * (total_width - box_width - side_width) + RESET
    return left_bg + left_padding + text + right_padding + right_bg

def display_big_number(num_str, start_row=5, fg_color=FG_GOLD, bg_color=BG_DARK):
    """在指定行显示带背景的大数字（9行高）"""
    rows = [""] * 9

    # 拼接每一行的大数字（只加前景色，不 reset）
    for digit in num_str:
        for i in range(9):
            rows[i] += fg_color + BIG_NUM_9[digit][i] + "  "

    for i in range(9):
        clean_len = len(strip_ansi(rows[i]))
        padding = (80 - clean_len) // 2

        sys.stdout.write(f"\033[{start_row + i};1H")
        sys.stdout.write(
            bg_color
            + " " * padding
            + rows[i]
            + " " * (80 - clean_len - padding)
            + RESET
        )

def show_normal_interface():
    """显示正常界面"""
    sys.stdout.write(HOME)
    sys.stdout.write(BG_DARK + " " * 80 + RESET + "\n")
    sys.stdout.write(BG_DARK + FG_GOLD + "🎆 🎆 2027 NEW YEAR COUNTDOWN 🎆 🎆".center(80) + RESET + "\n")
    sys.stdout.write(BG_DARK + " " * 80 + RESET + "\n")
    sys.stdout.write(BG_DARK + FG_WHITE + "⏳ TIME REMAINING".center(80) + RESET + "\n")
    sys.stdout.write(BG_DARK + " " * 80 + RESET + "\n")  # 倒计时占位
    sys.stdout.write(BG_DARK + " " * 80 + RESET + "\n")
    sys.stdout.write(BG_DARK + FG_WHITE + "📊 PROGRESS".center(80) + RESET + "\n")
    sys.stdout.write(BG_DARK + " " * 80 + RESET + "\n")  # 进度条占位
    sys.stdout.write(BG_DARK + FG_GOLD + "🎇 🎇 FIREWORKS SHOW 🎇 🎇".center(80) + RESET + "\n")
    for _ in range(5):
        sys.stdout.write(BG_FIREWORKS + " " * 80 + RESET + "\n")  # 烟花区域占位
    sys.stdout.flush()

def paint_full_background(bg=BG_DARK, height=25):
    sys.stdout.write(HOME)
    for row in range(1, height + 1):
        sys.stdout.write(f"\033[{row};1H{bg}{' ' * 80}{RESET}")


def show_fullscreen_countdown(seconds_left):
    sys.stdout.write(CLEAR)
    paint_full_background(BG_DARK)

    # 标题
    sys.stdout.write(
        f"\033[2;1H{BG_DARK + FG_GOLD + '🎆 🎆 2027 NEW YEAR COUNTDOWN 🎆 🎆'.center(80) + RESET}"
    )

    # 大数字
    seconds_str = f"{seconds_left:02d}"
    display_big_number(
        seconds_str,
        start_row=5,
        fg_color=FG_RED if seconds_left <= 5 else FG_GOLD
    )

    # FINAL 文本
    sys.stdout.write(
        f"\033[15;1H{BG_DARK + FG_GOLD + '🎇 🎇 FINAL COUNTDOWN 🎇 🎇'.center(80) + RESET}"
    )

    # 🔥 烟花背景：用“绝对定位”，不要 \n
    firework_bg_start = 17
    for i in range(5):
        sys.stdout.write(
            f"\033[{firework_bg_start + i};1H{BG_FIREWORKS}{' ' * 80}{RESET}"
        )

    sys.stdout.flush()


# ===== 烟花帧 =====
FIREWORKS_RAW = [
    [
        f"{FG_PINK}✨{RESET}",
        f"{FG_PINK}*         ✨{RESET}",
        f"{FG_PINK}*{RESET}",
        f"{FG_PINK}✨         *{RESET}",
        f"{FG_PINK}✨{RESET}"
    ],
    [
        f"{FG_CYAN}✨     ✨{RESET}",
        f"{FG_CYAN}*        ✨        *{RESET}",
        f"{FG_CYAN}✨        ✨{RESET}",
        f"{FG_CYAN}*        ✨        *{RESET}",
        f"{FG_CYAN}✨     ✨{RESET}"
    ],
    [
        f"{FG_GOLD}✨   *   ✨{RESET}",
        f"{FG_GOLD}✨  ✨{RESET}",
        f"{FG_GOLD}*   ✨ ✨   *{RESET}",
        f"{FG_GOLD}✨  ✨{RESET}",
        f"{FG_GOLD}✨   *   ✨{RESET}"
    ],
    [
        f"{FG_PINK}💥{RESET}",
        f"{FG_PINK}💥         💥{RESET}",
        f"{FG_PINK}💥{RESET}",
        f"{FG_PINK}💥         💥{RESET}",
        f"{FG_PINK}💥{RESET}"
    ],
    [   # 粉色小型烟花
        f"{FG_PINK}   ✨   {RESET}",
        f"{FG_PINK} *  ✨  * {RESET}",
        f"{FG_PINK}   *   {RESET}",
        f"{FG_PINK} ✨  *  ✨ {RESET}",
        f"{FG_PINK}   ✨   {RESET}"
    ],
    [   # 蓝色大型烟花
        f"{FG_CYAN}   ✨   ✨   {RESET}",
        f"{FG_CYAN} *      ✨      * {RESET}",
        f"{FG_CYAN}✨    ✨   ✨    ✨{RESET}",
        f"{FG_CYAN} *      ✨      * {RESET}",
        f"{FG_CYAN}   ✨   ✨   {RESET}"
    ],
    [   # 金色立体烟花
        f"{FG_GOLD}   ✨   *   ✨   {RESET}",
        f"{FG_GOLD} *    ✨ ✨ ✨    * {RESET}",
        f"{FG_GOLD}✨   ✨   ✨   ✨ {RESET}",
        f"{FG_GOLD} *    ✨ ✨ ✨    * {RESET}",
        f"{FG_GOLD}   ✨   *   ✨   {RESET}"
    ],
    [   # 粉色爆炸型烟花
        f"{FG_PINK}   💥   {RESET}",
        f"{FG_PINK} 💥  *  💥 {RESET}",
        f"{FG_PINK}   *   {RESET}",
        f"{FG_PINK} 💥  ✨  💥 {RESET}",
        f"{FG_PINK}   💥   {RESET}"
    ],
    [   # 黄色流星烟花
        f"{FG_GOLD}   ✨   {RESET}",
        f"{FG_GOLD}  *  ✨  *  {RESET}",
        f"{FG_GOLD} *   ✨   * {RESET}",
        f"{FG_GOLD}  *  ✨  *  {RESET}",
        f"{FG_GOLD}   ✨   {RESET}"
    ],
    [   # 彩色旋转烟花
        f"{FG_CYAN}  ✨ ✨  {RESET}",
        f"{FG_PINK} *     * {RESET}",
        f"{FG_GOLD}✨   💥   ✨{RESET}",
        f"{FG_CYAN} *     * {RESET}",
        f"{FG_PINK}  ✨ ✨  {RESET}"
    ]
]

# ===== 目标时间 =====
TOTAL_COUNTDOWN = 30  # 30秒总倒计时
target_time = datetime.datetime.now() + datetime.timedelta(seconds=TOTAL_COUNTDOWN)

# ===== 目标时间：2027 年 1 月 1 日 00:00:00 =====
# target_time = datetime.datetime(2027, 1, 1, 0, 0, 0)
# # ===== 计算总倒计时秒数 =====
# now = datetime.datetime.now()
# TOTAL_COUNTDOWN = int((target_time - now).total_seconds())

start_time = datetime.datetime.now()

# ===== 初始化 =====
sys.stdout.write(CLEAR + HIDE_CURSOR)
sys.stdout.flush()
frame = 0
normal_interface_shown = False

try:
    while True:
        now = datetime.datetime.now()
        remaining = target_time - now
        remaining_seconds = int(remaining.total_seconds())
        
        # 检查是否已到结束时间
        if remaining_seconds < 0:
            break
            
        # 判断显示模式
        if remaining_seconds > 10:
            # 显示正常界面（前20秒）
            if not normal_interface_shown:
                show_normal_interface()
                normal_interface_shown = True
            
            # 计算时间
            days = remaining.days
            hours, rem = divmod(remaining.seconds, 3600)
            minutes, seconds = divmod(rem, 60)
            elapsed = (TOTAL_COUNTDOWN - remaining_seconds)
            percent = min(elapsed / TOTAL_COUNTDOWN, 1)

            # ===== 更新倒计时 =====
            sys.stdout.write("\033[5;1H")
            sys.stdout.write(BG_DARK + FG_CYAN + f"{days:03d} Days   {hours:02d} Hours   {minutes:02d} Minutes   {seconds:02d} Seconds".center(80) + RESET)

            # ===== 更新进度条 =====
            sys.stdout.write("\033[8;1H")
            sys.stdout.write(progress_bar(percent).center(80))

            # ===== 更新烟花 =====
            current_firework = FIREWORKS_RAW[frame % len(FIREWORKS_RAW)]
            start_row = 10
            for i, line in enumerate(current_firework):
                row = start_row + i
                sys.stdout.write(f"\033[{row};1H")
                sys.stdout.write(center_in_box(line, box_width=25, total_width=80, bg_color=BG_FIREWORKS))
        else:
            # 最后10秒：全屏大数字显示
            show_fullscreen_countdown(remaining_seconds)
            
            # ===== 更新烟花 =====
            current_firework = FIREWORKS_RAW[frame % len(FIREWORKS_RAW)]
            start_row = 17  # 调整烟花起始行
            for i, line in enumerate(current_firework):
                row = start_row + i
                sys.stdout.write(f"\033[{row};1H")
                sys.stdout.write(center_in_box(line, box_width=25, total_width=80, bg_color=BG_FIREWORKS))
        
        sys.stdout.flush()
        frame += 1
        time.sleep(1)

    # ===== 倒计时结束 =====
    sys.stdout.write(CLEAR)
    paint_full_background(BG_DARK)
    
    # 标题
    sys.stdout.write(f"\033[2;1H{BG_DARK + FG_GOLD + '🎆 🎆 2027 NEW YEAR COUNTDOWN 🎆 🎆'.center(80) + RESET}")
    
    # 显示 "00"
    display_big_number("00", start_row=5, fg_color=FG_GREEN)
    
    # 欢迎文字
    sys.stdout.write(f"\033[15;1H{BG_DARK + FG_GOLD + '🎉🎉🎉   WELCOME TO 2027   🎉🎉🎉'.center(80) + RESET}")
    sys.stdout.write(f"\033[16;1H{BG_DARK + FG_CYAN + '✨✨✨   HAPPY NEW YEAR!   ✨✨✨'.center(80) + RESET}")
    
    # 烟花
    start_row = 18
    for i, line in enumerate(FIREWORKS_RAW[0]):
        sys.stdout.write(f"\033[{start_row + i};1H")
        sys.stdout.write(center_in_box(line, box_width=25, total_width=80, bg_color=BG_FIREWORKS))
    
    sys.stdout.flush()
    time.sleep(3)

finally:
    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.flush()

