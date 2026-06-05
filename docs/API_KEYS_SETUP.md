# 中国大陆 API 服务商注册指南

## 一、DeepSeek V3（LLM 大模型对话）

### 注册流程
1. 打开 https://platform.deepseek.com
2. 使用手机号注册/登录
3. 右上角 → **API Keys** → 点击 **创建 API Key**
4. 复制 key（形如 `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`）
5. 设置到环境变量：`DEEPSEEK_API_KEY=sk-xxxxxxxx`

### 充值
- 控制台 → 充值 → 支付宝/微信
- 最低充值：¥10
- 新用户赠送 ¥10 额度

### 价格
| 项目 | 价格 |
|------|------|
| 输入（缓存命中）| ¥0.1 / 百万 token |
| 输入（缓存未命中）| ¥1 / 百万 token |
| 输出 | ¥2 / 百万 token |

---

## 二、阿里云智能语音交互（ASR 语音识别）

### 注册流程
1. 打开 https://nls-portal.console.aliyun.com
2. 登录阿里云账号（需要实名认证，支持中国大陆身份证/企业认证）
3. 进入 **智能语音交互** → **项目管理** → **创建项目**
4. 项目名称随意填，场景选 **一句话识别**
5. 创建后，复制 **AppKey**

### 获取 AccessKey
1. 阿里云控制台 → 右上角头像 → **AccessKey 管理**
2. **创建 AccessKey** → 手机验证码 → 获取 `AccessKey ID` 和 `AccessKey Secret`
3. 设置环境变量：
   ```
   ALIYUN_ACCESS_KEY_ID=LTAI5xxxxxxxxxxxx
   ALIYUN_ACCESS_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ALIYUN_ASR_APP_KEY=xxxxxxxxxxxxxxxx
   ```

### 开通服务
- 智能语音交互 → 全部项目 → 点击项目 → **服务管理** → **一句话识别** → **开通**
- 首次开通有 3 个月免费试用（每月 5000 次）

### 价格
| 项目 | 价格 |
|------|------|
| 一句话识别 | ¥5.00 / 千次 |

---

## 三、火山引擎语音合成（TTS 语音合成）

### 注册流程
1. 打开 https://console.volcengine.com
2. 使用手机号注册（需要企业或个人实名认证）
3. 进入 **语音技术** → **语音合成**
4. **应用管理** → **创建应用** → 填写应用名称
5. 获取 **APP ID** 和 **Access Token**

### 设置环境变量
```
VOLCANO_APP_ID=xxxxxxxxxxxx
VOLCANO_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VOLCANO_VOICE=en_female_amanda
```

### 可选英文发音人
| 发音人 | 风格 |
|--------|------|
| en_female_amanda | 美式女声（推荐，最自然）|
| en_female_tracey | 英式女声 |
| en_male_jayden | 美式男声 |
| en_male_alex | 美式男声 |

### 价格
| 项目 | 价格 |
|------|------|
| 标准合成 | ¥2.00 / 万字符 |
| 精品合成（推荐发音人）| ¥5.00 / 万字符 |

首次开通赠送 ¥15 免费额度。

---

## 四、环境变量完整配置

在 `backend/.env` 文件中配置：

```bash
# DeepSeek
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 阿里云 ASR
ALIYUN_ACCESS_KEY_ID=LTAI5xxxxxxxxxxxx
ALIYUN_ACCESS_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ALIYUN_ASR_APP_KEY=xxxxxxxxxxxxxxxx

# 火山引擎 TTS
VOLCANO_APP_ID=xxxxxxxxxxxx
VOLCANO_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
VOLCANO_VOICE=en_female_amanda
```
