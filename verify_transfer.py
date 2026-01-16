import json
import hashlib
import os

# Purple Agent's local output (what it saved to disk during isolated test)
purple_json_path = r"C:\Users\User\Downloads\workspace\MOOCAgentic\deep-researcher-a2a-purple-agent\research_output.json"
purple_pdf_path = r"C:\Users\User\Downloads\workspace\MOOCAgentic\deep-researcher-a2a-purple-agent\research_output.pdf"

# Green Agent's received files (extracted from Docker container)
green_json_path = r"C:\Users\User\Downloads\workspace\MOOCAgentic\research-audit-leaderboard\green_received.json"
green_pdf_path = r"C:\Users\User\Downloads\workspace\MOOCAgentic\research-audit-leaderboard\green_received.pdf"

print("=== Purple Agent Local Output ===")
purple_json_hash = None
purple_pdf_hash = None

if os.path.exists(purple_json_path):
    with open(purple_json_path, 'r', encoding='utf-8') as f:
        purple_json = json.load(f)
    print(f"✓ JSON exists: {len(json.dumps(purple_json))} characters")
    print(f"  Slides: {len(purple_json.get('slides', []))}")
    purple_json_hash = hashlib.md5(json.dumps(purple_json, sort_keys=True).encode()).hexdigest()
    print(f"  MD5: {purple_json_hash}")
else:
    print("✗ JSON file not found")

if os.path.exists(purple_pdf_path):
    with open(purple_pdf_path, 'rb') as f:
        purple_pdf = f.read()
    print(f" PDF exists: {len(purple_pdf)} bytes")
    purple_pdf_hash = hashlib.md5(purple_pdf).hexdigest()
    print(f"  MD5: {purple_pdf_hash}")
else:
    print("✗ PDF file not found")

print("\n=== Green Agent Received Files ===")
green_json_hash = None
green_pdf_hash = None

if os.path.exists(green_json_path):
    with open(green_json_path, 'r', encoding='utf-8') as f:
        green_json = json.load(f)
    print(f"✓ JSON exists: {len(json.dumps(green_json))} characters")
    print(f"  Slides: {len(green_json.get('slides', []))}")
    green_json_hash = hashlib.md5(json.dumps(green_json, sort_keys=True).encode()).hexdigest()
    print(f"  MD5: {green_json_hash}")
else:
    print("✗ JSON file not found")

if os.path.exists(green_pdf_path):
    with open(green_pdf_path, 'rb') as f:
        green_pdf = f.read()
    print(f"✓ PDF exists: {len(green_pdf)} bytes")
    green_pdf_hash = hashlib.md5(green_pdf).hexdigest()
    print(f"  MD5: {green_pdf_hash}")
else:
    print("✗ PDF file not found")

print("\n=== Comparison Results ===")
if purple_json_hash and green_json_hash:
    if purple_json_hash == green_json_hash:
        print("✅ JSON MATCH: Files are identical!")
    else:
        print("❌ JSON MISMATCH: Files differ")
        print(f"   Purple MD5: {purple_json_hash}")
        print(f"   Green MD5:  {green_json_hash}")

if purple_pdf_hash and green_pdf_hash:
    if purple_pdf_hash == green_pdf_hash:
        print("✅ PDF MATCH: Files are identical!")
    else:
        print("❌ PDF MISMATCH: Files differ")
        print(f"   Purple MD5: {purple_pdf_hash}")
        print(f"   Green MD5:  {green_pdf_hash}")


if os.path.exists(purple_pdf_path):
    with open(purple_pdf_path, 'rb') as f:
        purple_pdf = f.read()
    print(f"✓ PDF exists: {len(purple_pdf)} bytes")
    pdf_hash = hashlib.md5(purple_pdf).hexdigest()
    print(f"  MD5: {pdf_hash}")
else:
    print("✗ PDF file not found")

print("\n=== Docker Compose Test Verification ===")
print("Note: In docker compose, files are transmitted via API, not saved to disk")
print("The Green Agent receives files directly from Purple Agent's HTTP response")
print("We need to check the docker logs to see what was transmitted...")
