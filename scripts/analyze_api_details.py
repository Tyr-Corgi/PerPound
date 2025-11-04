"""
Analyze API request/response details for comprehensive comparison
Captures: request payloads, response payloads, timing, data completeness
"""

import urllib.request
import urllib.error
import json
import time
from datetime import datetime

# API Keys
BARCODE_LOOKUP_KEY = "YOUR_BARCODE_LOOKUP_API_KEY_HERE"
APIFY_KEY = "YOUR_APIFY_API_TOKEN_HERE"
GO_UPC_KEY = "c74e46d117cd569c11ae68c88bae8f00c11f66b9ca5f662dd397550a4ea5d7ce"

# Test with 3 sample products for detailed analysis
test_products = [
    {"upc": "711381332580", "name": "Stonewall Kitchen Waffle Cookie"},
    {"upc": "818290019592", "name": "Chobani Coffee Greek Yogurt"},
    {"upc": "819046000420", "name": "Inka Giant Corn Chile Picante"}
]

def test_barcode_lookup(upc):
    """Test Barcode Lookup API with detailed logging"""
    url = f"https://api.barcodelookup.com/v3/products?barcode={upc}&key={BARCODE_LOOKUP_KEY}"
    
    request_info = {
        "api": "Barcode Lookup API",
        "method": "GET",
        "url": url.replace(BARCODE_LOOKUP_KEY, "***API_KEY***"),
        "headers": {
            "Content-Type": "application/json"
        },
        "authentication": "API Key in URL parameter",
        "request_body": None
    }
    
    start_time = time.time()
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            response_time = time.time() - start_time
            response_data = json.loads(response.read().decode())
            
            return {
                "success": True,
                "request": request_info,
                "response": {
                    "status_code": response.status,
                    "response_time_ms": round(response_time * 1000, 2),
                    "content_length": len(json.dumps(response_data)),
                    "payload": response_data
                }
            }
    except Exception as e:
        response_time = time.time() - start_time
        return {
            "success": False,
            "request": request_info,
            "response": {
                "error": str(e),
                "response_time_ms": round(response_time * 1000, 2)
            }
        }

def test_upcitemdb(upc):
    """Test UPCitemdb API with detailed logging"""
    url = f"https://api.upcitemdb.com/prod/trial/lookup?upc={upc}"
    
    request_info = {
        "api": "UPCitemdb",
        "method": "GET",
        "url": url,
        "headers": {
            "Content-Type": "application/json"
        },
        "authentication": "Trial API (no key required)",
        "request_body": None
    }
    
    start_time = time.time()
    
    try:
        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        
        with urllib.request.urlopen(req) as response:
            response_time = time.time() - start_time
            response_data = json.loads(response.read().decode())
            
            return {
                "success": True,
                "request": request_info,
                "response": {
                    "status_code": response.status,
                    "response_time_ms": round(response_time * 1000, 2),
                    "content_length": len(json.dumps(response_data)),
                    "payload": response_data
                }
            }
    except Exception as e:
        response_time = time.time() - start_time
        return {
            "success": False,
            "request": request_info,
            "response": {
                "error": str(e),
                "response_time_ms": round(response_time * 1000, 2)
            }
        }

def test_go_upc(upc):
    """Test Go-UPC API with detailed logging"""
    url = f"https://go-upc.com/api/v1/code/{upc}"
    
    request_info = {
        "api": "Go-UPC",
        "method": "GET",
        "url": url,
        "headers": {
            "Authorization": "Bearer ***API_KEY***",
            "Content-Type": "application/json"
        },
        "authentication": "Bearer token in Authorization header",
        "request_body": None
    }
    
    start_time = time.time()
    
    try:
        req = urllib.request.Request(url)
        req.add_header('Authorization', f'Bearer {GO_UPC_KEY}')
        
        with urllib.request.urlopen(req) as response:
            response_time = time.time() - start_time
            response_data = json.loads(response.read().decode())
            
            return {
                "success": True,
                "request": request_info,
                "response": {
                    "status_code": response.status,
                    "response_time_ms": round(response_time * 1000, 2),
                    "content_length": len(json.dumps(response_data)),
                    "payload": response_data
                }
            }
    except Exception as e:
        response_time = time.time() - start_time
        return {
            "success": False,
            "request": request_info,
            "response": {
                "error": str(e),
                "response_time_ms": round(response_time * 1000, 2)
            }
        }

def main():
    """Run detailed API analysis"""
    print("=" * 80)
    print("API REQUEST/RESPONSE DETAILED ANALYSIS")
    print("=" * 80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_results = []
    
    for product in test_products:
        print(f"\n{'='*80}")
        print(f"PRODUCT: {product['name']} (UPC: {product['upc']})")
        print(f"{'='*80}\n")
        
        product_results = {
            "product": product,
            "apis": {}
        }
        
        # Test Go-UPC (we have a key for this)
        print("Testing Go-UPC API...")
        go_upc_result = test_go_upc(product['upc'])
        product_results["apis"]["go_upc"] = go_upc_result
        if go_upc_result["success"]:
            print(f"  Response time: {go_upc_result['response']['response_time_ms']}ms")
            print(f"  Payload size: {go_upc_result['response']['content_length']} bytes")
        else:
            print(f"  Error: {go_upc_result['response']['error']}")
        
        time.sleep(1)
        
        # Test UPCitemdb
        print("\nTesting UPCitemdb API...")
        upcitemdb_result = test_upcitemdb(product['upc'])
        product_results["apis"]["upcitemdb"] = upcitemdb_result
        if upcitemdb_result["success"]:
            print(f"  Response time: {upcitemdb_result['response']['response_time_ms']}ms")
            print(f"  Payload size: {upcitemdb_result['response']['content_length']} bytes")
        else:
            print(f"  Error: {upcitemdb_result['response']['error']}")
        
        time.sleep(1)
        
        # Note: Barcode Lookup requires a paid API key
        print("\nNote: Barcode Lookup API requires paid key (not tested)")
        print("Note: Apify requires batch processing setup (not tested)")
        
        all_results.append(product_results)
    
    # Save results
    output_file = '../json-data/api_request_response_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"Results saved to: {output_file}")
    print("\nNext step: Run generate_api_technical_report.py to create HTML report")

if __name__ == "__main__":
    main()

