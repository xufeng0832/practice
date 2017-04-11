exl.write(0, 0, "Device_ID")    # 定义A1 内容(code18)
exl.write(0, 1, "Acquisition_parameters")    # 定义B1 内容(code19)
...依次类推

code20  line_num定义从第几行开始写入

code33 exl.write(line_num, 0, Device_ID) # Device_ID内容
code34 exl.write(line_num, 1, Acquisition_parameters)

code36 最终文件名称