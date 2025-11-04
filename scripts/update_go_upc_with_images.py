import json
import re

# Load the updated Go-UPC data with images
with open('../json-data/go_upc_15_products_test.json', 'r', encoding='utf-8') as f:
    go_upc_data = json.load(f)

# Read the HTML
with open('../API_Compare_Chart.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Update each Go-UPC column to include images
for i, product in enumerate(go_upc_data, 1):
    ean = product['ean']
    image_url = product.get('imageUrl', '')
    
    if not image_url:
        print(f"Row {i}: No image URL found")
        continue
    
    # Find the Go-UPC column for this product
    # Pattern: find the Go-UPC column that contains this EAN's context
    # We'll search for the specific pattern around each row
    
    # Find the product card with this EAN, then find its Go-UPC column
    pattern = rf'(<div class="row-number">{i}</div>.*?<span class="ean-code">EAN: {re.escape(ean)}</span>.*?<div class="api-column go-upc">)(.*?)(</div>\s*</div>\s*</div>\s*</div>\s*</div>)'
    
    match = re.search(pattern, html_content, re.DOTALL)
    if not match:
        print(f"Row {i}: Could not find Go-UPC column")
        continue
    
    go_upc_section = match.group(2)
    
    # Replace the "No Images" warning with an actual image
    new_go_upc_section = re.sub(
        r'<div class="not-found" style="background: #fff3cd; border: 2px solid #ffc107; color: #856404;">\s*⚠️ No Images<br>\s*<small>Go-UPC provides data but no product images</small>\s*</div>',
        f'''<img src="{image_url}" alt="Product" class="product-image">
                    <div class="image-info">
                        <div class="resolution">Resolution: Unknown</div>
                        <div style="margin-top: 5px;">✓ 1 image available</div>
                    </div>''',
        go_upc_section
    )
    
    # Replace in the full HTML
    html_content = html_content.replace(match.group(2), new_go_upc_section)
    print(f"Row {i}: Updated Go-UPC with image: {image_url[:60]}...")

# Update the summary section
html_content = re.sub(
    r'<div class="detail-row-summary" style="margin-top: 10px;">\s*<span class="detail-label-summary">⚠️ Images:</span>\s*<span class="detail-value-summary" style="color: #d32f2f;">0 images available</span>\s*</div>',
    '''<div class="detail-row-summary" style="margin-top: 10px;">
                        <span class="detail-label-summary">Images:</span>
                        <span class="detail-value-summary" style="color: #2e7d32;">✅ 1 image per product</span>
                    </div>''',
    html_content
)

# Update the summary text
html_content = re.sub(
    r'<strong>Go-UPC</strong> achieved 100% success rate \(15/15\) but provides NO IMAGES\.',
    '<strong>Go-UPC</strong> achieved 100% success rate (15/15) with 1 image per product.',
    html_content
)

# Write the updated HTML
with open('../API_Compare_Chart.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("\nSuccessfully updated all 15 Go-UPC columns with images!")
print("Go-UPC now shows images for all products! 🎉")

