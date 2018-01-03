#! /bin/bash

# 设备id 可通过命令行执行 instruments -s 获取
device_id='F1FCFDD1-8691-411D-8C96-B38BB13EB551'
# 工程编译后对应的.app文件放置的路径
app_path='/Users/analysyseguan/Desktop/千帆对数/工程文件/EGMonitor_SDK_Demo.app'
# Bundle Identifier
app_identifier='com.analysys.FanzhouLocalized'

echo 启动模拟器
xcrun simctl boot $device_id
echo 模拟器启动完成

sleep 60*2 #等待几分钟之后再启动app

echo 安装app
xcrun simctl install $device_id $app_path
echo 安装完成

## 多次打开关闭app（业务需要）
count=3
for ((i=0; i<$count; i++)); do

sleep 30 #等待30s启动app

echo 启动应用程序
xcrun simctl launch $device_id $app_identifier
echo app启动完成

sleep 30 #等待30s后退出app

echo 开始关闭应用程序
xcrun simctl terminate $device_id $app_identifier
echo 已关闭应用

##	$(($i+1))
time=i
((time+=1))
echo 完成第 $time 次循环

((time+=1))
if [ "$time" -ne "$(($count+1))" ]; then
echo 开始第 $time 次循环
fi

done



sleep 10 #等待30s后卸载app

echo 卸载app
xcrun simctl uninstall $device_id $app_identifier
echo app已卸载

