# Databricks notebook source
from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from .readimage import readimage

class NgsToolsTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        # 获取参数中的图片 URL
        url = tool_parameters.get("url")
        if not url:
            yield self.create_text_message("参数 'url' 不能为空")
            return

        # 如果传入的是相对路径，可拼接 base
        if not url.startswith("http"):
            base_url = "http://localhost"  # 可替换为你实际部署的前缀
            url = base_url.rstrip("/") + "/" + url.lstrip("/")

        try:
            result = readimage(url)  # 调用你的图片处理函数
            yield self.create_text_message(result["result"])

        except Exception as e:
            yield self.create_text_message(f"处理图片时出错: {str(e)}")
