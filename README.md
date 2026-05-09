# StockScout

StockScout 是一个本地可运行的股票投资决策辅助工程。

当前版本提供：

- 清晰的工程目录骨架
- 可配置的股票样本数据与策略参数
- 数据采集、筛选、基本面分析、技术面分析、风险控制、综合决策等 agent
- 输出到仓库 `tmp/` 目录的时间戳 CSV 报告

## 目录

- `config/`
- `src/stockscout/`
- `tests/`
- `tmp/`
- `docs/`

## 运行方式

在仓库根目录执行：

```bash
PYTHONPATH=src python -m stockscout
```

命令会输出生成的文件路径，报告字段包括：

- 当前时间
- 股票名
- 股票代码
- 当前股价
- 股票市值
- 推荐买入价格
- 推荐卖出价格

## 测试

```bash
PYTHONPATH=src python -m unittest discover -s tests
```
