import asyncio
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from pydantic import BaseModel, Field
import math

class CrawlerFeedbackPayload(BaseModel):
    url: str
    metric: float
    agent_id: Optional[str] = None
    timestamp: Optional[float] = Field(default_factory=datetime.now.timestamp)

class CrawlerNetwork:
    def __init__(self, name: str = "main", buffer_size: int = 500):
        self.name = name
        self.global_weights: Dict[str, float] = {}
        self.meta_scores: Dict[str, float] = {}
        self.buffer_size = buffer_size
        self.buffer: asyncio.Queue = asyncio.Queue(maxsize=buffer_size)
        self.learning_cycle_delay: int = 60
        self.last_learn_time: float = 0.0

    async def ingest_feedback(self, payload: CrawlerFeedbackPayload):
        url = payload.url
        metric = payload.metric
        agent_id = payload.agent_id
        
        current_val = self.global_weights.get(url, 0.0)
        current_meta = self.meta_scores.get(url, 1.0)
        
        if agent_id:
            source_score = self.global_weights.get(f"{url}:{agent_id}", 0.0)
            self.global_weights[f"{url}:{agent_id}"] = source_score
        
        # Exponential Moving Average for smoothing
        smoothing_factor = 0.2
        self.global_weights[url] = (current_val * (1 - smoothing_factor) + metric * smoothing_factor)
        
        # Dynamic metadata update for freshness
        self.meta_scores[url] = (self.meta_scores.get(url, 1) * 0.95) + (0.05 if metric > 1 else 0.01)

    async def compute_priority_scores(self, top_n: int = 5) -> List[str]:
        scored: List[tuple] = list(self.global_weights.items())
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s[0].split(':')[0] for s in scored if s[1] > 0.5][:top_n]

    async def run(self, feed_func: Optional[Callable] = None):
        while True:
            try:
                if feed_func:
                    await asyncio.wait_for(feed_func(self.name), timeout=1.0)
                
                if len(self.global_weights) > 10:
                    top_urls = await self.compute_priority_scores(3)
                    self.meta_scores["top_performers"] = top_urls
                
                if self.meta_scores.get("top_performers"):
                    self.meta_scores["top_performers_count"] = len(top_urls)
                    
            except asyncio.TimeoutError:
                pass

    async def get_learning_schedule(self, limit: int = 100) -> List[str]:
        all_keys = list(self.global_weights.keys())
        all_keys.sort(key=lambda x: self.global_weights[x], reverse=True)
        return all_keys[:limit]

    def __call__(self):
        return self

def main():
    network = CrawlerNetwork()
    
    async def fetcher():
        for i in range(100):
            url = f"https://example.com/page/{i}"
            metric = math.log(i + 1)
            payload = CrawlerFeedbackPayload(url=url, metric=metric)
            await network.buffer.put(payload)
            await network.ingest_feedback(payload)
    
    asyncio.run(fetcher())
    asyncio.run(network.run())

    print(f"Network: {network.name}")
    print(f"Top URLs: {await network.compute_priority_scores()}")

if __name__ == "__main__":
    asyncio.run(CrawlerNetwork().run())