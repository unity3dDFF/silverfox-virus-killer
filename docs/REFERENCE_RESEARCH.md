# GitHub 同类项目参考记录

检索日期：2026-07-16。

## pirwhite/pirsrc_scan

地址：https://github.com/pirwhite/pirsrc_scan

可取思路：

- 隔离区、JSON 清单和恢复流程；
- 多特征组合、文件头/哈希、数字签名作为证据；
- 特征导入导出和可扩展扫描器结构。

本项目的调整：隔离清单采用原子写入，文件重命名为不可执行后缀；自动处置只接受已确认哈希，不把“未签名”单独视为恶意；不接入样本上传和外部多引擎 API。

## herta0426/SilverfoxCleanScript

地址：https://github.com/herta0426/SilverfoxCleanScript

可取思路：

- 银狐可能利用 WDAC 策略阻止安全软件；
- 变更策略前备份；
- 优先使用 Windows 自带 `CiTool.exe` 识别策略。

本项目的调整：WDAC 策略可能属于企业合规配置，因此只报告 `SiPolicy.p7b` 是否存在，不自动删除所有“非平台策略”；也不在线下载、解压或启动第三方急救工具。

## 采用原则

参考项目只用于提炼防御能力和风险点。未拉取或收录病毒样本；未复制远程下载后直接执行、关闭安全软件、盲删系统策略等高风险操作。
