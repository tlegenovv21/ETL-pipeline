from .base import BaseTransformer
import re

class LogTransformer(BaseTransformer):
    def transform(self, log_string):
        if not log_string:
            return None
            
        # Regex to parse the synthetic Apache-style log
        pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?) (.*?) HTTP/1.1" (\d+) (\d+)')
        match = pattern.match(log_string)
        
        if match:
            specific_metadata = {
                "ip_address": match.group(1),
                "timestamp": match.group(2),
                "http_method": match.group(3),
                "endpoint": match.group(4),
                "status_code": int(match.group(5)),
                "size_bytes": int(match.group(6))
            }
            
            # Return using the unified schema
            return self.unify_metadata(
                raw_id=match.group(2), # Use timestamp as a rough ID
                source_type="synthetic_logs",
                data_type="log",
                content=log_string,
                metadata=specific_metadata
            )
        return None