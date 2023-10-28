import os

OPENAI_API_KEY = "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"

MODEL_PATH = {
    "embed_model": {
        "text-embedding-ada-002": OPENAI_API_KEY,
    },
    "llm_model": {},
}

LANGCHAIN_LLM_MODEL = {
    "OpenAI": {
        "model_name": "gpt-3.5-turbo",
        "api_base_url": "https://api.openai.com/v1",
        "api_key": OPENAI_API_KEY,
        "openai_proxy": "",
    },

EMBEDDING_MODEL = "text-embedding-ada-002"  # 可以尝试最新的嵌入式sota模型：bge-large-zh-v1.5


# Embedding 模型运行设备。设为"auto"会自动检测，也可手动设定为"cuda","mps","cpu"其中之一。
EMBEDDING_DEVICE = "auto"

# LLM 名称
LLM_MODEL = "OpenAI"

# LLM 运行设备。设为"auto"会自动检测，也可手动设定为"cuda","mps","cpu"其中之一。
LLM_DEVICE = "auto"

# 历史对话轮数
HISTORY_LEN = 3

# LLM通用对话参数
TEMPERATURE = 0.7
# TOP_P = 0.95 # ChatOpenAI暂不支持该参数
