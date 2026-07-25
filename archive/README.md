# 归档说明

这里存放已经退出主运行链路的兼容入口和旧 Tk 功能窗口。

当前唯一用户入口是：

```text
AA启动.bat → webapp.py → pywebview + ui/
```

归档文件不应被主程序导入，也不应作为新功能的修改目标。保留它们只是为了旧快捷方式和历史代码追溯；确认不再需要兼容后，可以在单独的清理版本中删除整个 `archive/`。

运行时生成的 `__pycache__/`、`tests/__pycache__/`、`.drawru-imgter-main.lock` 和 `.drawru-imgter-status.json` 不进入归档，已从工作区清理。
