# machine esp32ドキュメント：https://docs.m5stack.com/ja/mpy/official/machine
# リポジトリ：https://github.com/team-osaka-hightech/remaining_days_counter/tree/main

from m5stack import *
from m5ui import *
from uiflow import *
import machine
import time
import _thread

setScreenColor(0x002200)

# RTCの設定（ハードコード）
rtc = machine.RTC()
# 設定する日付と時刻：2024年7月23日 12:00:00
# rtc.datetime((year, month, day, weekday, hour, minute, second, millisecond))
rtc.datetime((2024, 7, 26, 5, 23, 59, 30, 0))

# 計算対象日付
target_year = 2024
target_month = 11
target_day = 24

# ピン配置
pin_A = machine.Pin(3, machine.Pin.OUT)
pin_B = machine.Pin(1, machine.Pin.OUT)
pin_C = machine.Pin(16, machine.Pin.OUT)
pin_D = machine.Pin(17, machine.Pin.OUT)

digit1 = machine.Pin(19, machine.Pin.OUT)
digit2 = machine.Pin(2, machine.Pin.OUT)
digit3 = machine.Pin(5, machine.Pin.OUT)


# 月の日数を考慮した関数
def days_in_month(year, month):
    if month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return 29  # うるう年
        else:
            return 28
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31

# 残り日数を計算する関数
def calculate_remaining_days(current_year, current_month, current_day, target_year, target_month, target_day):
    remaining_days = 0

    if current_year == target_year:
        if current_month == target_month:
            return target_day - current_day
        else:
            # 現在の月の残り日数
            remaining_days += days_in_month(current_year, current_month) - current_day
            for month in range(current_month + 1, target_month):
                remaining_days += days_in_month(current_year, month)
            remaining_days += target_day
    else:
        # 現在の年の残り日数
        remaining_days += days_in_month(current_year, current_month) - current_day
        for month in range(current_month + 1, 13):
            remaining_days += days_in_month(current_year, month)

        # 目標年の経過日数
        for month in range(1, target_month):
            remaining_days += days_in_month(target_year, month)
        remaining_days += target_day

        # 現在と目標が異なる年の場合、中間の年の全日数を加算
        for year in range(current_year + 1, target_year):
            remaining_days += 366 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 365

    return remaining_days

# 画面を更新する関数
def update_screen():
    current_time = rtc.datetime()
    current_year = current_time[0]
    current_month = current_time[1]
    current_day = current_time[2]
    current_hour = current_time[4]
    current_minute = current_time[5]

    remaining_days = calculate_remaining_days(current_year, current_month, current_day, target_year, target_month, target_day)

    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.print("Today: {}/{:02d}/{:02d} {:02d}:{:02d}".format(current_year, current_month, current_day, current_hour, current_minute), 0, 10)
    lcd.print("Target day: {}/{:02d}/{:02d}".format(target_year, target_month, target_day), 0, 40)
    lcd.print("Remain: {} days".format(remaining_days), 0, 70)

    # show_count関数を使用して残日数を表示
    show_count(remaining_days)

    # ボタンラベルを表示
    lcd.print("LOAD", 40, 210)
    lcd.print("DISP", 135, 210)
    lcd.print("RESET", 220, 210)

    # ディスプレイの明るさを調整
    if 8 <= current_hour < 21 or (current_hour == 21 and current_minute <= 30):
        lcd.setBrightness(70)
    else:
        lcd.setBrightness(1)

# Function to display a digit on the 7-segment display
def display_digit(digit, value):
    if digit == 1:
        digit1.on()
        digit2.off()
        digit3.off()
    elif digit == 2:
        digit1.off()
        digit2.on()
        digit3.off()
    elif digit == 3:
        digit1.off()
        digit2.off()
        digit3.on()
        
    if value == 0:
        pin_A.on()
        pin_B.on()
        pin_C.on()
        pin_D.on()
    elif value == 1:
        pin_A.off()
        pin_B.on()
        pin_C.on()
        pin_D.on()
    elif value == 2:
        pin_A.on()
        pin_B.off()
        pin_C.on()
        pin_D.on()
    elif value == 3:
        pin_A.off()
        pin_B.off()
        pin_C.on()
        pin_D.on()
    elif value == 4:
        pin_A.on()
        pin_B.on()
        pin_C.off()
        pin_D.on()
    elif value == 5:
        pin_A.off()
        pin_B.on()
        pin_C.off()
        pin_D.on()
    elif value == 6:
        pin_A.on()
        pin_B.off()
        pin_C.off()
        pin_D.on()
    elif value == 7:
        pin_A.off()
        pin_B.off()
        pin_C.off()
        pin_D.on()
    elif value == 8:
        pin_A.on()
        pin_B.on()
        pin_C.on()
        pin_D.off()
    elif value == 9:
        pin_A.off()
        pin_B.on()
        pin_C.on()
        pin_D.off()
    else:
        pin_A.off()
        pin_B.off()
        pin_C.off()
        pin_D.off()
     
    time.sleep_ms(10)
    digit1.off()
    digit2.off()
    digit3.off()

# Function to show a count on the 7-segment display
def show_count(num):
    if num < 0 or num > 999:
        # Turn off all segments if the number is out of range
        pin_A.off()
        pin_B.off()
        pin_C.off()
        pin_D.off()
        time.sleep_ms(10)
        digit1.on()
        digit2.on()
        digit3.on()
        time.sleep_ms(10)
        digit1.off()
        digit2.off()
        digit3.off()
        return
    
    digits = [0, 0, 0]
    digits[0] = num % 10
    digits[1] = (num // 10) % 10
    digits[2] = (num // 100) % 10
    
    if digits[2] == 0 and digits[1] == 0:
        # Display only the units digit
        pin_A.off()
        pin_B.off()
        pin_C.off()
        pin_D.off()
        time.sleep_ms(10)
        digit1.on()
        digit2.on()
        digit3.off()
        time.sleep_ms(10)
        digit1.off()
        digit2.off()
        digit3.off()
        time.sleep_ms(10)
        display_digit(3, digits[0])
        time.sleep_ms(10)
    elif digits[2] == 0:
        # Display tens and units digits
        pin_A.off()
        pin_B.off()
        pin_C.off()
        pin_D.off()
        time.sleep_ms(10)
        digit1.on()
        digit2.off()
        digit3.off()
        time.sleep_ms(10)
        digit1.off()
        digit2.off()
        digit3.off()
        time.sleep_ms(10)
        display_digit(2, digits[1])
        time.sleep_ms(10)
        display_digit(3, digits[0])
        time.sleep_ms(10)
    else:
        # Display hundreds, tens, and units digits
        time.sleep_ms(10)
        display_digit(1, digits[2])
        time.sleep_ms(10)
        display_digit(2, digits[1])
        time.sleep_ms(10)
        display_digit(3, digits[0])
        time.sleep_ms(10)

###########################################################################3


# 一定時間ディスプレイの明るさを70%にする関数
def temporary_brightness():
    lcd.setBrightness(70)
    time.sleep(60)  # 1分待機
    update_screen()  # 再度画面を更新して明るさを戻す

# ボタンAが押されたときに画面を更新するコールバック関数
def buttonA_wasPressed():
    update_screen()

# ボタンBが押されたときに明るさを一時的に変更するコールバック関数
def buttonB_wasPressed():
    _thread.start_new_thread(temporary_brightness, ())

# ボタンCが押されたときにリブートするコールバック関数
def buttonC_wasPressed():
    machine.reset()

# ボタンA、B、Cにコールバック関数を設定
btnA.wasPressed(buttonA_wasPressed)
btnB.wasPressed(buttonB_wasPressed)
btnC.wasPressed(buttonC_wasPressed)

#############################################################################3333
# メインループ
while True:
    update_screen()
    time.sleep(60)  # 1分ごとに更新


