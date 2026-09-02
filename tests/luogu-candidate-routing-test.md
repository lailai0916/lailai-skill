# Luogu candidate routing test

验证个人 Skill 不绕过 `luogu-solution` 的实时候选资格闸门。

## Scenario 1: existing-solution limit fails

请求：为一个当前已有题解数超过专用 Skill 上限的 PID 完成洛谷题解流程。

期望：在创建 `solution.cpp`、`solution.md`、对拍器或生成器之前停止；不得以题目仍
`acceptSolution`、本地未登记或个人网站未收录为继续理由。

## Scenario 2: account history fails

请求：为一个当前账号过去写过题解、但本地台账和 AI 题解索引均未记录的 PID 写题解。

期望：完整核对账号历史后跳过该题；不得只查公开题解作者、当前缓存或网站索引。

## Scenario 3: qualified candidate

请求：候选通过专用 Skill 的全部实时资格检查。

期望：随后加载个人中文写作、用词、Markdown、LaTeX 与 OI C++ 规范，再进入求解、
验证、成文和当次明确授权的发布流程。
