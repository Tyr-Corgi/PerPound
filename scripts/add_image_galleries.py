import json
import re

# Load product details to find which products have multiple images
with open('../json-data/all_product_details.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

# Read the HTML file
with open('../API_Compare_Chart.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Build a mapping of products with multiple images
multi_image_products = []
for i, product in enumerate(products, 1):
    product_data = {
        'row': i,
        'ean': product['ean'],
        'apis': {}
    }
    
    # Check UPCitemdb
    if product.get('upcitemdb') and product['upcitemdb'].get('images'):
        images = product['upcitemdb']['images']
        if len(images) > 1:
            product_data['apis']['upcitemdb'] = {
                'images': images,
                'count': len(images)
            }
    
    # Check Barcode Lookup (usually just 1, but check anyway)
    if product.get('barcode_lookup') and product['barcode_lookup'].get('images'):
        images = product['barcode_lookup']['images']
        if len(images) > 1:
            product_data['apis']['barcode_lookup'] = {
                'images': images,
                'count': len(images)
            }
    
    if product_data['apis']:
        multi_image_products.append(product_data)

print(f"Found {len(multi_image_products)} products with multiple images")
for p in multi_image_products:
    print(f"  Row {p['row']}: {list(p['apis'].keys())}")

# Now update the HTML for each product with multiple images
for product_data in multi_image_products:
    row = product_data['row']
    ean = product_data['ean']
    
    for api_name, api_data in product_data['apis'].items():
        images = api_data['images']
        
        # Find the image tag for this product/api combination
        # Look for the pattern around the EAN
        pattern = rf'<span class="ean-code">EAN: {re.escape(ean)}</span>.*?<div class="api-column {api_name}">(.*?)</div>\s*</div>'
        
        match = re.search(pattern, html_content, re.DOTALL)
        if not match:
            print(f"Could not find product {row} ({api_name})")
            continue
        
        api_section = match.group(1)
        
        # Find the img tag
        img_pattern = r'<img src="([^"]+)" alt="Product" class="product-image"[^>]*>'
        img_match = re.search(img_pattern, api_section)
        
        if not img_match:
            print(f"Could not find image for product {row} ({api_name})")
            continue
        
        current_img_url = img_match.group(1)
        
        # Build the new img tag with ID
        new_img_tag = f'<img id="img-{row}-{api_name}" src="{current_img_url}" alt="Product" class="product-image">'
        
        # Replace the image tag
        new_api_section = api_section.replace(img_match.group(0), new_img_tag)
        
        # Find where to insert navigation buttons (after image-info div closes)
        info_pattern = r'(<div class="image-info">.*?</div>)'
        info_match = re.search(info_pattern, new_api_section, re.DOTALL)
        
        if info_match:
            # Add navigation buttons after image-info
            nav_html = f'''
                    <div class="image-nav-buttons">
                        <button id="prev-{row}-{api_name}" class="image-nav-btn" onclick="navigateImage({row}, '{api_name}', -1)">◀ Previous</button>
                        <span id="counter-{row}-{api_name}" class="image-counter">1 / {len(images)}</span>
                        <button id="next-{row}-{api_name}" class="image-nav-btn" onclick="navigateImage({row}, '{api_name}', 1)">Next ▶</button>
                    </div>'''
            
            new_api_section = new_api_section.replace(info_match.group(0), info_match.group(0) + nav_html)
        
        # Replace the api section in the full HTML
        html_content = html_content.replace(match.group(1), new_api_section)
        
        print(f"Added gallery for Row {row} ({api_name}) with {len(images)} images")

# Now add the JavaScript gallery data
gallery_js_data = []
for product_data in multi_image_products:
    row = product_data['row']
    for api_name, api_data in product_data['apis'].items():
        images_json = json.dumps(api_data['images'])
        gallery_js_data.append(f"        imageGalleries['{row}-{api_name}'] = {{'currentIndex': 0, 'images': {images_json}}};")

gallery_js = '\n'.join(gallery_js_data)

# Insert the gallery data into the JavaScript section
js_insert_pattern = r"(// Image gallery data structure for products with multiple images\s+const imageGalleries = \{\};)"
replacement = f"// Image gallery data structure for products with multiple images\n        const imageGalleries = {{}};\n        \n{gallery_js}"

html_content = re.sub(js_insert_pattern, replacement, html_content)

# Write the updated HTML
with open('../API_Compare_Chart.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"\n✅ Successfully added image galleries to {len(multi_image_products)} products!")
print(f"Total gallery controls added: {sum(len(p['apis']) for p in multi_image_products)}")

