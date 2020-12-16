# AHKpy
使用python调用autohotkey程序
适配 ahk版本 1.1.26.01
## 使用
```python
ahk = AHK()
ahk.mouse.move((413, 413))
ahk.mouse.click()
state = ahk.key.get_key_state("a")
# 需要获取结果的函数调用会返回一个event对象(类似于异步中Future对象,由threading.Condition实现)
print(state.result()) # 通过result()方法获取结果,会有等待阻塞

```
## 原理
在实例化AHK类之后,会起一个ahk的进程,并通过io文件与python进程通讯

当使用ahk的操作方法时,由python进程对ahk进程下达相应的命令
