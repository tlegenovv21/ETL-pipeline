from .base import BaseExtractor, logger
from faker import Faker
import random
import datetime

fake = Faker()

class LogGenerator(BaseExtractor):
    def __init__(self):
        super().__init__("Synthetic Logs")
    
    def extract(self, count=50):
        """
        Generates 'count' fake apache-style access logs.
        Returns a list of log strings.
        """
        logger.info(f"Generating {count} synthetic logs...")
        logs = []
        
        methods = ["GET", "POST", "PUT", "DELETE"]
        endpoints = ["/login", "/home", "/api/data", "/contact", "/admin"]
        codes = [200, 201, 400, 401, 404, 500]

        for _ in range(count):
            ip = fake.ipv4()
            dt = datetime.datetime.now().strftime("%d/%b/%Y:%H:%M:%S")
            method = random.choice(methods)
            endpoint = random.choice(endpoints)
            status = random.choice(codes)
            size = random.randint(100, 5000)
            
            # Format: IP - - [Date] "METHOD Endpoint HTTP/1.1" Status Size
            log_entry = f'{ip} - - [{dt}] "{method} {endpoint} HTTP/1.1" {status} {size}'
            logs.append(log_entry)
            
        return logs