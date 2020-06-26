import sys
import time

##LED操作クラス
class led:

    def __init__(self, port, mode):
        l = led_sys(port)
        self.l = l                   # LED下位クラスのインスタンス
        self.available = l.available # 操作可能か
        self.mode = mode             # 点灯モード(1:点滅2:徐々に
        self.state = 0               # モード内でのシーケンス番号(0〜19)
        self.debugcount = 0          # debug

    def __del__(self):
        del self.l

    # 操作部分とのI/F
    # 約100ms分点灯して制御を上に返す
    def blink(self):
        if self.mode == 1:
            self.blink_mode1()
        elif self.mode == 2:
            self.blink_mode2()
        else:
            pass
    # モード変更
    def change_mode(self):
        self.state = 0
        if self.mode == 1:
            self.mode = 2
        else:
            self.mode = 1

    #モードセット
    def set_mode(self, mode):
        if self.mode == mode:
            pass
        else:
            self.state = 0
            self.mode = mode

    # クラス内部処理
    # 点滅モード1
    def blink_mode1(self):
        #state = 0〜9は点灯、10〜19は消灯
        if self.state > 9 :
            duty  = 0
        else:
            duty = 100
        self.light_led(duty)

        if self.state == 19:
            self.state = 0
            self.debugcount = self.debugcount + 1
        else:
            self.state = self.state + 1

    # 点滅モード2
    def blink_mode2(self):
        #state = 0〜9はだんだん明るく、10が最大。10〜19はだんだん暗く、0が消灯
        if self.state > 9:
            duty = 100 - (self.state - 10) * 10
        else:
            duty = 10 * self.state
            
        self.light_led(duty)

        if self.state == 19:
            self.state = 0
            self.debugcount = self.debugcount + 1
        else:
            self.state = self.state + 1

    # LED下位クラスとのI/F
    def light_led(self, duty):
        if self.available == True:
            loop_count = 0
            while loop_count < 10:
                self.l.light(duty)
                loop_count = loop_count + 1
        else:
            pass

            
##LED下位クラス
##TODO:後で置き換える
class led_sys:
    msec = 1.0/1000.0             # ミリ秒計算用
    gpiobase ="/sys/class/gpio/"  # 制御ファイルの場所
    wait_mag = 0.96               # ぴったり10ms sleepすると他処理のため若干重くなるため少し短かく

    # 初期化
    def __init__(self, port):
        self.port = ""
        self.available = False
        try:
            with open(led_sys.gpiobase + "export", "w") as f:
                print(str(port), end='', file=f, flush=True)
            time.sleep(100*led_sys.msec)
            self.port = str(port)
            with open(led_sys.gpiobase + "gpio" + self.port + "/direction", "w") as f:
                print("out", end='', file=f, flush=True)
            self.available = True
            time.sleep(100*led_sys.msec)

        except Exception as e:
            print("init error:" + str(e), file=sys.stderr)

    # 後始末
    def __del__(self):
        if self.port != "":
            try:
                with open(led_sys.gpiobase + "unexport", "w") as f:
                    print(self.port, end='', file=f, flush=True)
                
            except Exception as e:
                print("del error: " + str(e), file=sys.stderr)
        else:
            pass

    #LED明滅
    #全体を10msとして、duty比(%)でON/OFFを細かく分ける
    def light(self, duty):
        if duty < 0:
            duty = 0
        elif duty > 100:
            duty = 100
        else:
            pass
        # Turn On
        if duty != 0:
            sleepmsec = 10.0 * duty / 100.0 * led_sys.wait_mag
            try:
                with open(led_sys.gpiobase + "gpio" + self.port + "/value", "w") as f:
                    print("1", end='', file=f, flush=True)
                    time.sleep(sleepmsec * led_sys.msec)
            except Exception as e:
                print(str(e), file=sys.stderr)
        else:
            pass
        # Turn Off
        if duty != 100:
            sleepmsec = 10.0 * (100 - duty) / 100.0 * led_sys.wait_mag
            try:
                with open(led_sys.gpiobase + "gpio" + self.port + "/value", "w") as f:
                    print("0", end='', file=f, flush=True)
                    time.sleep(sleepmsec * led_sys.msec)
            except Exception as e:
                print(str(e), file=sys.stderr)
        else:
            pass




