import requests
from typing import Dict, Any
from urllib.parse import urlencode, unquote
import os
import sys
import ssl


from config.settings import settings

ssl._create_default_https_context = ssl._create_unverified_context
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ApiService:
    
    def __init__(self):
        self.base_url = settings.api_base_url
        self.service_key = settings.service_key
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
            'Connection': 'keep-alive'
        })
    
    def get_data(self, page_no: int = 1, num_of_rows: int = 10, **kwargs) -> Dict[str, Any]:
        service_key = unquote(self.service_key)
        params = {
            'serviceKey': service_key,
            'pageNo': page_no,
            'numOfRows': num_of_rows,
            **kwargs
        }
        
        try:
            http_url = self.base_url.replace('https://', 'http://')
            response = self.session.get(
                http_url, 
                params=params, 
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            raise Exception(f"🔴 Fail(API): {str(e)}") 