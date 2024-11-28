from typing import Any

from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from loguru import logger


class TokenUsageLoggingHandler(BaseCallbackHandler):
    def __init__(
        self,
        cost_per_1m_input_tokens: float = 0.15,
        cost_per_1m_output_tokens: float = 0.60,
    ) -> None:
        """
        トークン使用量を記録するコールバックハンドラ。

        :param model_cost_per_1m_tokens: 1kトークンあたりのモデルコスト（USD単位）
        """
        self.cost_per_1m_input_tokens = cost_per_1m_input_tokens
        self.cost_per_1m_output_tokens = cost_per_1m_output_tokens

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """
        モデルの応答が完了した際のハンドラ。

        :param response: モデルからの応答オブジェクト
        """
        # トークン使用量を取得
        llm_output = response.llm_output  # LLMResultのllm_outputを取得
        if not llm_output or "token_usage" not in llm_output:
            logger.warning("トークン使用量情報が利用できません。")
            return

        usage = llm_output["token_usage"]
        prompt_tokens = usage["prompt_tokens"]
        completion_tokens = usage["completion_tokens"]
        total_tokens = usage["total_tokens"]

        # コスト計算
        input_cost_dollar = prompt_tokens * (self.cost_per_1m_input_tokens / 1_000_000)  # $0.15 / 1M tokens
        output_cost_dollar = completion_tokens * (self.cost_per_1m_output_tokens / 1_000_000)  # $0.60 / 1M tokens
        total_cost_dollar = input_cost_dollar + output_cost_dollar

        logger.info(f"Input tokens: {prompt_tokens}")
        logger.info(f"Output tokens: {completion_tokens}")
        logger.info(f"Total tokens: {total_tokens}")
        logger.info(
            f"Cost - Input: {input_cost_dollar:.6f} USD, Output: {output_cost_dollar:.6f} USD, Total: {total_cost_dollar:.6f} USD"
        )
