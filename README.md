# StockScout

StockScout 是一个本地可运行的股票投资决策辅助工程。

当前版本提供：

- 清晰的工程目录骨架
- 可配置的股票样本数据与策略参数
- 数据采集、筛选、基本面分析、技术面分析、风险控制、综合决策等 agent
- 输出到仓库 `tmp/` 目录的时间戳 CSV 报告
- 面向股票筛选场景的 `StockScout-agent.md` 与配套 skill 说明

## 目录

- `config/`
- `src/stockscout/`
- `tests/`
- `tmp/`
- `docs/`
- `skills/`
- `StockScout-agent.md`

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

## 自定义筛选 Agent

- `StockScout-agent.md`：定义一个按股票筛选员思路工作的自定义 agent
- `skills/stock-screening.skill.md`：沉淀标准化筛选流程
- `tmp/`：保留给后续 agent 分析结果落盘使用

示例输出：

```text
股票代码: AAPL
当前日期: 2026-05-09
当前价格: 150.00
建议买入价格: 145.50
建议卖出价格: 165.00
```
