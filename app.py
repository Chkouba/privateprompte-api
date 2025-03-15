@app.route('/chatgpt-proxy/<path:subpath>', methods=['GET', 'POST'])
def chatgpt_proxy(subpath=""):
    base_url = "https://chat.openai.com"
    headers = {
        "User-Agent": request.headers.get("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"),
        "Accept": request.headers.get("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    }

    try:
        if request.method == 'GET':
            response = requests.get(f"{base_url}/{subpath}", headers=headers, timeout=10)
        else:
            response = requests.post(f"{base_url}/{subpath}", headers=headers, data=request.get_data(), timeout=10)

        # Réécriture des URLs internes
        content = response.content.decode('utf-8')
        content = content.replace('https://chat.openai.com', f'{request.host_url}chatgpt-proxy')
        
        return Response(
            content,
            status=response.status_code,
            headers={
                "Content-Type": response.headers["Content-Type"],
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )

    except Exception as e:
        return str(e), 500
