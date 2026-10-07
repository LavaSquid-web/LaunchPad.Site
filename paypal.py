# Let's create a robust starter Python backend script (Flask + PayPal Webhook Listener)
# that receives PayPal webhook notifications and automatically compiles a tenant's customized website.

script_content = '''"""
LaunchPad Sites - PayPal Webhook & Automated Tenant Provisioning Backend
Built with Flask
"""

import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Directory where tenant websites will be generated
TENANTS_DIR = os.path.join(os.getcwd(), "generated_tenants")
os.makedirs(TENANTS_DIR, exist_ok=True)

# Base HTML Template for Tenant Sites
TEMPLATE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{business_name} | Official Site</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased">
    <header class="border-b border-slate-800 py-6 px-8 flex justify-between items-center max-w-6xl mx-auto">
        <h1 class="text-xl font-bold text-cyan-400">{business_name}</h1>
        <span class="text-xs text-slate-400 font-mono">Subdomain: {subdomain}.launchpadsites.io</span>
    </header>
    <main class="max-w-4xl mx-auto px-8 py-20 text-center space-y-8">
        <h2 class="text-4xl md:text-5xl font-extrabold tracking-tight">{tagline}</h2>
        <p class="text-slate-400 text-lg max-w-2xl mx-auto">{niche} services tailored for high-growth success.</p>
        <div class="pt-4">
            <a href="mailto:{email}" class="bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold px-8 py-4 rounded-xl text-base shadow-lg transition inline-block">
                Contact {business_name}
            </a>
        </div>
    </main>
    <footer class="text-center py-8 text-xs text-slate-600 border-t border-slate-900">
        Powered by LaunchPad Sites &bull; {email}
    </footer>
</body>
</html>
"""

@app.route('/webhook/paypal', methods=['POST'])
def paypal_webhook():
    payload = request.get_json()
    if not payload:
        return jsonify({"status": "error", "message": "No payload received"}), 400

    event_type = payload.get("event_type")
    print(f"Received PayPal Webhook Event: {event_type}")

    # Handle Successful Subscription Activation
    if event_type == "BILLING.SUBSCRIPTION.ACTIVATED" or event_type == "PAYMENT.SALE.COMPLETED":
        resource = payload.get("resource", {})
        
        # Extract custom data or subscriber details
        # (In production, subscriber metadata or custom_id passes tenant settings)
        subscriber = resource.get("subscriber", {})
        shipping_name = subscriber.get("name", {}).get("full_name", "New Tenant")
        payer_email = subscriber.get("email_address", "client@example.com")
        
        # Generate safe subdomain slug
        subdomain = "".join(c.lower() for c in shipping_name if c.isalnum()) or "tenant"
        business_name = shipping_name + "'s Business"
        tagline = "Welcome to Our Official Website"
        niche = "Professional"

        # Build personalized HTML file for the tenant
        tenant_html = TEMPLATE_HTML.format(
            business_name=business_name,
            subdomain=subdomain,
            tagline=tagline,
            niche=niche,
            email=payer_email
        )

        filename = f"{subdomain}_index.html"
        filepath = os.path.join(TENANTS_DIR, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(tenant_html)

        print(f"Successfully provisioned tenant site: {filepath}")
        return jsonify({"status": "success", "subdomain": f"{subdomain}.launchpadsites.io"}), 200

    return jsonify({"status": "ignored", "event": event_type}), 200

if __name__ == '__main__':
    print("LaunchPad PayPal Webhook Listener running on port 5000...")
    app.run(port=5000, debug=True)
'''

with open("paypal_webhook_server.py", "w", encoding="utf-8") as f:
    f.write(script_content)

print("Script saved successfully.")