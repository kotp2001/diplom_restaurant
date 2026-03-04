def app(request):
    return {
        "status": 200,
        "headers": [("Content-Type", "text/html")],
        "body": "<h1>Hello from Vercel!</h1><p>If you see this, Vercel works.</p>"
    }