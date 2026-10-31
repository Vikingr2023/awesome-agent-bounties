# HarnessClaw 体验测评 —— 代码审查工作流场景

## 使用上下文

我在一个中小型 TypeScript 项目中试用了 HarnessClaw 的 agent 调度能力，目标是把日常的 PR review 流程自动化：给定一个 diff，让主 agent 派生子 agent 分别做 (1) 安全扫描、(2) 风格/命名检查、(3) 测试覆盖分析，最后由主 agent 汇总成 review 评论。

## 安装与首次配置

安装过程基本顺畅，`yarn install` 后按文档启动 dev 窗口即可。首次配置 MCP 时需要手动编辑配置文件，文档里对字段说明略 terse，建议补充一个最小可运行示例。子 agent 调度需要在配置里开启对应权限，这一步我在 issue 评论区才找到说明，略绕。

## 实际使用片段

子 agent 调度的产出示例（安全扫描子 agent 回复摘录）：

[HarnessClaw sub-agent: security-scan]
- src/auth/token.ts:42  jwt.verify 使用了 HS256 默认密钥，建议显式指定算法并校验 iss/aud
- src/api/upload.ts:18  未限制文件大小，存在 DoS 风险
- 无高危 SQL 注入点（ORM 参数化查询）

主 agent 汇总后生成的 review 评论结构清晰，能直接贴到 PR。对比 Claude Code 单 agent 串行分析，HarnessClaw 的并行子 agent 明显更快，且各维度报告互不干扰。

## 优点

- 子 agent 调度降低上下文污染，每个子 agent 只看自己负责的维度。
- MCP 集成后可直接拉取仓库信息，减少手动粘贴 diff。

## 痛点

- 配置项分散，缺少「一键启用常用 skill」的入口。
- 子 agent 失败时主 agent 的重试策略不够透明，日志里只看到最终汇总，看不到重试次数。
- 长 session 下 `~/.harnessclaw/db/harnessclaw.db` 增长较快，建议提供清理/归档命令。

## 期待

- 提供 skill 市场的一键安装与版本回滚。
- 支持 review 结果直接推送为 PR comment（当前需手动复制）。

## 总结

整体体验优于我之前用的单 agent 方案，尤其在多维度并行分析场景。配置与可观测性还有提升空间，但核心调度能力可靠，值得继续投入。