"""
Check the raw Go-UPC API response to see if images are included
"""

import urllib.request
import json

GO_UPC_API_KEY = "c74e46d117cd569c11ae68c88bae8f00c11f66b9ca5f662dd397550a4ea5d7ce"

# Test with one UPC
upc = "711381332580"  # Stonewall Kitchen

print(f"Testing UPC: {upc}")
print("=" * 80)

url = f"https://go-upc.com/api/v1/code/{upc}"

req = urllib.request.Request(url)
req.add_header('Authorization', f'Bearer {GO_UPC_API_KEY}')

with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())
    
    # Print the entire response prettily
    print(json.dumps(data, indent=2))
    
    # Check specifically for images
    print("\n" + "=" * 80)
    print("CHECKING FOR IMAGES:")
    print("=" * 80)
    
    if 'product' in data:
        product = data['product']
        print(f"Product keys: {list(product.keys())}")
        
        if 'images' in product:
            images = product['images']
            print(f"\nImages found: {len(images)}")
            for i, img in enumerate(images, 1):
                print(f"  Image {i}: {img}")
        else:
            print("\nNo 'images' key in product data")
            
        # Check for image_url or imageUrl or similar
        for key in product.keys():
            if 'image' in key.lower():
                print(f"\nFound image-related key: {key} = {product[key]}")

