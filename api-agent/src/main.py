import os
import ssl
import json
import sys
from dotenv import load_dotenv

from services.service import ApiService
from utils.parser import Parser
from models.response import Response

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
ssl._create_default_https_context = ssl._create_unverified_context

try:
    api_service = ApiService()
    data = api_service.get_data(page_no=1, num_of_rows=5)
    
    parser = Parser()
    response = parser.parse_json(data)
    
    
    output_file = "api_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"🟢 Success")
    
except Exception as e:
    print(f"🔴 Fail: {str(e)}")