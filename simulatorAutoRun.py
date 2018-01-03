# _*_ coding: utf-8 _*_

print('Hello, Python.')

import os
import time
import random

# 文件日志写入
file_path = '{path}/{file_name}.txt'.format(path=os.getcwd(),file_name='log')
document = open(file=file_path, mode='a', encoding='utf-8')

# 设备id 可通过命令行执行 instruments -s 获取
device_id = 'F1FCFDD1-8691-411D-8C96-B38BB13EB551'
# Bundle Identifier
app_identifier = 'com.analysys.FanzhouLocalized'
# 工程编译后对应的.app文件放置的路径
app_path = '/Users/analysyseguan/Desktop/千帆对数/工程文件/EGMonitor_SDK_Demo.app'
# 多次打开关闭app
open_close_times = 3
# 默认时间间隔
time_interval = 30


def write_log(log_info=''):
    document.write('{date} : {log}\n'.format(date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), log=log_info))


def begin_loop():
    """
    开始安装卸载循环
    :return:
    """
    while True:
        write_log('安装app')
        os.system('xcrun simctl install {device_id} {app_path}'.format(device_id=device_id, app_path=app_path))
        write_log('app安装完成，等待启动。。。')

        time.sleep(time_interval)


        ## 多次打开关闭app（业务需要）

        for index in range(1, open_close_times+1):

            write_log('启动app')
            os.system('xcrun simctl launch {device_id} {app_identifier}'.format(device_id=device_id, app_identifier=app_identifier))
            write_log('app已启动，等待关闭。。。')

            # app在前台使用时间随机
            random_value = random.randint(time_interval, 3*time_interval)
            write_log('休眠时长:{0}'.format(random_value))
            time.sleep(random_value)

            write_log('关闭app')
            os.system('xcrun simctl terminate {device_id} {app_identifier}'.format(device_id=device_id, app_identifier=app_identifier))
            write_log('app已关闭')

            # print('完成第',index,'次循环')
            if index != open_close_times:
                write_log('开始第 {0} 次循环，等待app重新启动。。。'.format(index+1))

                # app再次启动时时间随机
                random_value = random.randint(time_interval, 2 * time_interval)
                write_log('休眠时长:{}'.format(random_value))
                time.sleep(random_value)
            else:
                write_log('等待app卸载。。。')

            document.flush()


        time.sleep(time_interval)

        write_log('卸载app')
        os.system('xcrun simctl uninstall {device_id} {app_identifier}'.format(device_id=device_id, app_identifier=app_identifier))
        write_log('app已卸载，本次循环已完成!')

        write_log('---------------------------------------------')
        document.flush()

        time.sleep(time_interval)



if __name__ == '__main__':

    write_log('启动模拟器')
    os.system('xcrun simctl boot {device_id}'.format(device_id=device_id))
    write_log('模拟器启动完成，等待安装app。。。')

    # 首次启动模拟器较慢,sleep
    time.sleep(time_interval * 4)

    begin_loop()
