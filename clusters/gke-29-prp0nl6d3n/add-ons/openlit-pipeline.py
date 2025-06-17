"""
title: OpenLIT Monitoring Filter
author: your-name
date: 2025-01-16
version: 1.0
license: MIT
description: A filter pipeline for monitoring LLM interactions with OpenLIT
requirements: openlit
"""

from typing import List, Optional, Dict, Any
import openlit
from pydantic import BaseModel, Field

class Filter:  # Note: This is "Filter", not "Pipe"
    class Valves(BaseModel):
        OPENLIT_API_KEY: str = Field(
            default="",
            description="OpenLIT API key for authentication"
        )
        OTEL_EXPORTER_OTLP_ENDPOINT: str = Field(
            default="http://otel-collector:4317",
            description="OpenTelemetry collector endpoint"
        )

    def __init__(self):
        self.valves = self.Valves()
        # List of pipeline/model IDs this filter applies to
        # Use ["*"] to apply to all models, or specify specific model IDs
        self.pipelines: List[str] = ["*"]
        
    def on_startup(self):
        # Initialize OpenLIT when the filter starts
        openlit.init(
            otlp_endpoint=self.valves.OTEL_EXPORTER_OTLP_ENDPOINT,
            api_key=self.valves.OPENLIT_API_KEY
        )

    def inlet(self, body: Dict[str, Any], user: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # This runs BEFORE the request goes to the LLM
        # OpenLIT will automatically capture the request
        return body

    def outlet(self, body: Dict[str, Any], user: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # This runs AFTER the response comes back from the LLM
        # OpenLIT will automatically capture the response
        return body
