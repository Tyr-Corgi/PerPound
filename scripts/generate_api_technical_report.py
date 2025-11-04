"""
Generate HTML technical report showing API request/response details
"""

import json
from datetime import datetime

# Load the analysis data
with open('../json-data/api_request_response_analysis.json', 'r', encoding='utf-8') as f:
    analysis_data = json.load(f)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Technical Analysis Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        header {{
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }}
        
        h1 {{
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .timestamp {{
            color: #666;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        
        .product-section {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        .product-header {{
            border-bottom: 3px solid #667eea;
            padding-bottom: 15px;
            margin-bottom: 25px;
        }}
        
        .product-title {{
            font-size: 1.8em;
            color: #333;
            font-weight: 600;
        }}
        
        .upc-code {{
            font-family: 'Courier New', monospace;
            background: #f0f0f0;
            padding: 5px 10px;
            border-radius: 5px;
            margin-top: 10px;
            display: inline-block;
        }}
        
        .api-card {{
            background: #f8f9fa;
            border-left: 5px solid;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 25px;
        }}
        
        .api-card.go-upc {{
            border-left-color: #9e9e9e;
        }}
        
        .api-card.upcitemdb {{
            border-left-color: #ff9800;
        }}
        
        .api-card.barcode-lookup {{
            border-left-color: #4caf50;
        }}
        
        .api-card.apify {{
            border-left-color: #2196f3;
        }}
        
        .api-header {{
            font-size: 1.5em;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
        }}
        
        .section-title {{
            background: #667eea;
            color: white;
            padding: 10px 15px;
            border-radius: 5px;
            font-weight: 600;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        
        .detail-grid {{
            display: grid;
            grid-template-columns: 200px 1fr;
            gap: 10px;
            margin-bottom: 15px;
        }}
        
        .detail-label {{
            font-weight: 600;
            color: #555;
        }}
        
        .detail-value {{
            color: #333;
            font-family: 'Courier New', monospace;
            background: white;
            padding: 5px 10px;
            border-radius: 3px;
            word-break: break-all;
        }}
        
        .json-payload {{
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 20px;
            border-radius: 8px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            line-height: 1.5;
            max-height: 600px;
            overflow-y: auto;
        }}
        
        .metric {{
            display: inline-block;
            background: #e3f2fd;
            color: #1976d2;
            padding: 8px 15px;
            border-radius: 20px;
            margin: 5px;
            font-weight: 600;
        }}
        
        .error {{
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #c62828;
        }}
        
        .success {{
            background: #e8f5e9;
            color: #2e7d32;
            padding: 10px 15px;
            border-radius: 5px;
            display: inline-block;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔧 API Technical Analysis Report</h1>
            <p style="font-size: 1.2em; color: #666; margin-top: 10px;">Request Payloads, Response Payloads & Performance Metrics</p>
            <div class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </header>
'''

for product_result in analysis_data:
    product = product_result['product']
    apis = product_result['apis']
    
    html += f'''
        <div class="product-section">
            <div class="product-header">
                <div class="product-title">{product['name']}</div>
                <div class="upc-code">UPC: {product['upc']}</div>
            </div>
'''
    
    for api_name, api_data in apis.items():
        api_display_name = {
            'go_upc': 'Go-UPC API',
            'upcitemdb': 'UPCitemdb',
            'barcode_lookup': 'Barcode Lookup API',
            'apify': 'Apify'
        }.get(api_name, api_name)
        
        html += f'''
            <div class="api-card {api_name.replace('_', '-')}">
                <div class="api-header">{api_display_name}</div>
'''
        
        if api_data['success']:
            response_time = api_data['response']['response_time_ms']
            payload_size = api_data['response']['content_length']
            
            html += f'''
                <div class="success">✅ Successful Response</div>
                <div>
                    <span class="metric">⏱️ {response_time}ms</span>
                    <span class="metric">📦 {payload_size:,} bytes</span>
                    <span class="metric">📊 Status: {api_data['response']['status_code']}</span>
                </div>
'''
            
            # Request Details
            request = api_data['request']
            html += '''
                <div class="section-title">📤 REQUEST DETAILS</div>
                <div class="detail-grid">
                    <div class="detail-label">Method:</div>
                    <div class="detail-value">''' + request['method'] + '''</div>
                    <div class="detail-label">URL:</div>
                    <div class="detail-value">''' + request['url'] + '''</div>
                    <div class="detail-label">Authentication:</div>
                    <div class="detail-value">''' + request['authentication'] + '''</div>
                </div>
'''
            
            # Headers
            html += '''
                <div class="section-title">📋 REQUEST HEADERS</div>
                <div class="json-payload">'''
            html += json.dumps(request['headers'], indent=2)
            html += '''</div>'''
            
            # Response Payload
            html += '''
                <div class="section-title">📥 RESPONSE PAYLOAD</div>
                <div class="json-payload">'''
            html += json.dumps(api_data['response']['payload'], indent=2)
            html += '''</div>'''
            
        else:
            # Error case
            html += f'''
                <div class="error">
                    <strong>❌ Request Failed</strong><br>
                    <div style="margin-top: 10px;">
                        Error: {api_data['response']['error']}<br>
                        Response Time: {api_data['response']['response_time_ms']}ms
                    </div>
                </div>
'''
            
            # Still show request details
            request = api_data['request']
            html += '''
                <div class="section-title">📤 REQUEST DETAILS (Attempted)</div>
                <div class="detail-grid">
                    <div class="detail-label">Method:</div>
                    <div class="detail-value">''' + request['method'] + '''</div>
                    <div class="detail-label">URL:</div>
                    <div class="detail-value">''' + request['url'] + '''</div>
                    <div class="detail-label">Authentication:</div>
                    <div class="detail-value">''' + request['authentication'] + '''</div>
                </div>
'''
        
        html += '''
            </div>
'''
    
    html += '''
        </div>
'''

html += '''
    </div>
</body>
</html>
'''

# Write the HTML file
output_file = '../api-reports/API_Technical_Report.html'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html)

print("=" * 80)
print("HTML TECHNICAL REPORT GENERATED")
print("=" * 80)
print(f"Report saved to: {output_file}")
print("\nThis report includes:")
print("  - Request URLs and methods")
print("  - Authentication details")
print("  - Request headers")
print("  - Full response payloads (JSON)")
print("  - Response times (ms)")
print("  - Payload sizes (bytes)")
print("\nOpen the file in a browser to view the formatted report!")

