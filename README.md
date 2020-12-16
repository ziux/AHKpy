# AHKpy
使用python调用autohotkey程序

## 使用
```python
ahk = AHK()
ahk.mouse.move((413, 413))
ahk.mouse.click()
```
## 原理
在实例化AHK类之后,会起一个ahk的进程,并通过io文件与python进程通讯

当使用ahk的操作方法时,由python进程对ahk进程下达相应的命令
