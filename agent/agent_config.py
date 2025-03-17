from dataclasses import dataclass

@dataclass
class AgentConfig:
    name: str = "TradeMateAI"
    model_type: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 1000 