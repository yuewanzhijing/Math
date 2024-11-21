
# -*- coding: utf-8 -*-
# pip3 install pyserial
import serial
import serial.tools.list_ports
import time

'''
    三色灯测试文件
'''

class COM:
    def __init__(self, port, baud):
        self.port = port
        self.baud = int(baud)
        self.open_com = None
        self.real_time_data = ''

    def open(self):
        try:
            self.open_com = serial.Serial(self.port, 9600,8,"E",1)
        except Exception as e:
            print(
                '[RS232] 開啟端口失敗:{}/{}'.format(self.port, self.baud))
            print('[RS232] 原因:{}'.format(e))

    def close(self):
        if self.open_com is not None and self.open_com.isOpen:
            self.open_com.close()

    def send_data(self, data):
        if self.open_com is None:
            self.open()
        success_bytes = self.open_com.write(data)
        return success_bytes

    def get_data(self, time_out_sec=4):
        all_data = ''
        if self.open_com is None:
            self.open()
        start_time = time.time()
        while True:
            data = self.open_com.read(self.open_com.inWaiting())
            data = str(data, "utf-8")
            if data != '':
                all_data = all_data + data
                self.real_time_data = all_data
            elif len(all_data.replace("\\", "").replace("#", "")) == 8:
                break
            elif time.time() - time_out_sec > start_time:
                break
        return all_data


def getallport():
    port_list = list(serial.tools.list_ports.comports())
    if len(port_list) == 0:
        print("[RS232]无可用串口!")
        return None
    else:
        return port_list


if __name__ == "__main__":
    '''
        1.打開USB串口root權限
            sudo usermod -aG dialout ubuntu
        2.根據需要使用相關功能 （每個功能之間是獨立的，可同步使用）
            01 05 00 00 ff 00 8C 3A 打开红灯(常亮)       01 05 00 00 00 00 CD CA 关闭红色
            01 05 00 01 ff 00 DD FA 打开黄灯(常亮)       01 05 00 01 00 00 9C 0A 关闭黄灯
            01 05 00 02 ff 00 2D FA 打开绿灯(常亮)       01 05 00 02 00 00 6C 0A 关闭绿灯
            01 05 00 03 ff 00 7C 3A 打开蜂鸣器(一直响)   01 05 00 03 00 00 3D CA 关闭蜂鸣器

            01 05 00 00 f0 00 89 CA 红灯闪烁(2Hz)
            01 05 00 00 f1 00 88 5A 红灯闪烁(1Hz)
            01 05 00 00 f2 00 88 AA 红灯闪烁(0.5Hz)
            01 05 00 00 f3 00 89 3A 红灯闪烁(0.25Hz)

            01 05 00 01 f0 00 D8 0A 黄灯闪烁(2Hz)
            01 05 00 01 f1 00 D9 9A 黄灯闪烁(1Hz)
            01 05 00 01 f2 00 D9 6A 黄灯闪烁(0.5Hz)
            01 05 00 01 f3 00 D8 FA 黄灯闪烁(0.25Hz)

            01 05 00 02 f0 00 28 0A 绿灯闪烁(2Hz)
            01 05 00 02 f1 00 9F B7 绿灯闪烁(1Hz)
            01 05 00 02 f2 00 29 6A 绿灯闪烁(0.5Hz)
            01 05 00 02 f3 00 28 FA 绿灯闪烁(0.25Hz)

            01 05 00 03 f0 00 79 CA 蜂鸣器模式1(2Hz)
            01 05 00 03 f1 00 78 5A 蜂鸣器模式2(1Hz)
            01 05 00 03 f2 00 78 AA 蜂鸣器模式2(0.5Hz)
            01 05 00 03 f3 00 79 3A 蜂鸣器模式2(0.25Hz)
    '''
    arr = getallport()
    print(arr)
    # 注意修改端口编号
    # com = COM(arr[0].device,9600)
    # com.send_data(bytes.fromhex("01 05 00 02 ff 00 2D FA"))

    # com.send_data(bytes.fromhex("01 05 00 03 f0 00 79 CA"))
    # com.send_data(bytes.fromhex("01 05 00 00 f0 00 89 CA"))
    # time.sleep(2)
    # com.send_data(bytes.fromhex("01 05 00 00 00 00 CD CA"))
    # com.send_data(bytes.fromhex("01 05 00 03 00 00 3D CA"))
    
