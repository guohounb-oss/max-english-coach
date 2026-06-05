# Max English Coach → 中国大陆版迁移方案

---

## 改动范围：需要修改的文件

### 🔴 新增（3 个核心服务）

| 文件 | 说明 |
|------|------|
| `backend/app/services/llm_service.py` | DeepSeek V3 对话服务 |
| `backend/app/services/asr_service.py` | 阿里云 ASR 语音识别 |
| `backend/app/services/tts_service.py` | 火山引擎 TTS 语音合成（重写）|

### 🟡 修改（5 个配套文件）

| 文件 | 改什么 |
|------|--------|
| `backend/app/core/config.py` | 新增 DeepSeek/阿里云/火山引擎 配置项 |
| `backend/app/services/correction_service.py` | `OpenAIService` → `LLMService` |
| `backend/app/routes/voice.py` | 导入路径改为新服务 |
| `backend/requirements.txt` | 移除 `aiosqlite`，保持最小依赖 |
| `.env.example` | 新增三大中国服务商的 API Key 变量 |

### 🟢 保持不变（无需改动）

- `backend/app/routes/memory.py` — 记忆路由
- `backend/app/routes/dashboard.py` — 统计路由
- `backend/app/models/models.py` — 数据模型
- `backend/app/db/sqlite.py` — 数据库
- `backend/app/db/chroma.py` — 向量数据库
- `backend/app/services/prompt_service.py` — 提示词组合
- `backend/app/services/memory_service.py` — 记忆服务
- `backend/app/prompts/*.txt` — 5 个提示词模板
- `frontend/**` — **全部前端代码不变**

### ❌ 不再需要的旧文件

| 文件 | 替代 |
|------|------|
| `backend/app/services/openai_service.py` | 被 `llm_service.py` 替代 |
| `backend/app/services/whisper_service.py` | 被 `asr_service.py` 替代 |

（保留旧文件在磁盘上不影响运行，新代码不会引用它们）

---

## 成本估算

### 假设条件
- 每天使用 30 分钟
- 平均每轮对话：用户说 15 个单词 + AI 回复 40 个单词
- 每分钟约 4 轮对话

### 每月用量

| 指标 | 计算 | 结果 |
|------|------|------|
| 语音识别次数 | 30分钟 × 30天 × 每分钟4次 | **3,600 次** |
| LLM 输入 token | 每轮 400 token × 3,600 | **1,440,000 token** |
| LLM 输出 token | 每轮 200 token × 3,600 | **720,000 token** |
| TTS 字数 | 每轮 40 单词 × 3,600 | **144,000 单词 ≈ 72万字符** |

### 每月费用

| 服务 | 单价 | 月用量 | 月费用 |
|------|------|--------|--------|
| DeepSeek V3 输入 | ¥1/百万 token | 144 万 token | **¥1.44** |
| DeepSeek V3 输出 | ¥2/百万 token | 72 万 token | **¥1.44** |
| 阿里云 ASR | ¥5/千次 | 3,600 次 | **¥18.00** |
| 火山引擎 TTS | ¥2/万字符 | 72 万字符 | **¥14.40** |
| **合计** | | | **≈ ¥35.28 / 月** |

> ⚠️ 实际费用可能因使用时长、对话频率、token 长度而异。
> 重度使用（每天 2 小时）：约 **¥140 / 月**
> 轻度使用（每天 10 分钟）：约 **¥12 / 月**

---

## 对比 OpenAI API 原版成本

| 项目 | OpenAI | 中国大陆版 | 节省 |
|------|--------|-----------|------|
| LLM | GPT-4o: $5/百万 token | DeepSeek V3: ¥1/百万 token | **~85%** |
| ASR | Whisper: $0.006/分钟 | 阿里云: ¥0.005/次 | **~50%** |
| TTS | TTS-1: $15/百万字符 | 火山: ¥2/万字符 | **~85%** |
| 30分钟/天 | **≈ $45/月** | **≈ ¥35/月** | **≈ 94%** |

---

## 启动步骤

```bash
cd max-english-coach

# 1. 配置 API Key
cp .env.example backend/.env
# 编辑 backend/.env，填入 DeepSeek + 阿里云 + 火山引擎的 Key

# 2. 启动后端
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 3. 启动前端（另一个终端）
cd frontend
pnpm dev

# 4. 打开 http://localhost:3000
```
