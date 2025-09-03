from flask import Flask
import csv

app = Flask(__name__)

# ===== 读取 CSV 链接 =====
def read_links():
    links = []
    try:
        with open('links.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                links.append(row['link'])
    except Exception as e:
        print("读取 CSV 失败:", e)
    return links

@app.route("/")
def index():
    return "<h2>🌐 Selamat datang! Klik <a href='/view'>di sini</a> untuk melihat tautan promosi.</h2>"

@app.route("/view")
def view():
    links = read_links()
    if not links:
        return "<h2>❌ Tautan promosi belum tersedia</h2>"

    html_links = "".join([
        f"""
        <div class="card">
            <h3>🔗 Tautan Promosi</h3>
            <p id="link-{i}">{link}</p>
            <button class="button" onclick="copyLink('link-{i}')">📋 Salin Tautan</button>
        </div>
        """ for i, link in enumerate(links)
    ])

    return f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tautan Promosi</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #eef9ff;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 20px;
                margin: 0;
            }}
            h2 {{
                color: #0077cc;
                margin-bottom: 15px;
                text-align: center;
            }}
            .container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 15px;
                width: 90%;
                max-width: 500px;
                margin: auto;
            }}
            .card {{
                width: 100%;
                background: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                text-align: center;
            }}
            .card h3 {{
                color: #333;
                margin-bottom: 10px;
            }}
            .card p {{
                font-size: 16px;
                color: #555;
                word-break: break-all;
                margin-bottom: 12px;
            }}
            button.button {{
                width: 100%;
                padding: 14px;
                background: #0077cc;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            }}
            button.button:hover {{
                background: #005fa3;
            }}
            footer {{
                margin-top: 20px;
                font-size: 14px;
                color: #666;
                text-align: center;
            }}
        </style>
        <script>
            function copyLink(id) {{
                var copyText = document.getElementById(id).innerText;
                navigator.clipboard.writeText(copyText).then(function(){{
                    alert('✅ Tautan disalin!');
                }});
            }}
        </script>
    </head>
    <body>
        <h2>🌐 Daftar Tautan Promosi</h2>
        <div class="container">
            {html_links}
        </div>
        <footer>🔄 Jika ada masalah, silakan hubungi admin.</footer>
    </body>
    </html>
    """
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
