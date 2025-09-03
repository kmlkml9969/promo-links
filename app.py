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
        <title>Tautan Promosi</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #eef9ff, #d6f0ff);
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 30px;
                margin: 0;
            }}
            h2 {{
                color: #0077cc;
                margin-bottom: 20px;
            }}
            .container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px;
                width: 100%;
                max-width: 900px;
            }}
            .card {{
                background: white;
                border-radius: 16px;
                padding: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                text-align: center;
                transition: transform 0.2s;
            }}
            .card:hover {{
                transform: translateY(-5px);
            }}
            .card h3 {{
                color: #333;
            }}
            .card p {{
                font-size: 14px;
                color: #555;
                margin: 10px 0;
                word-break: break-all;
            }}
            button.button {{
                display: inline-block;
                margin-top: 10px;
                padding: 10px 18px;
                background: #0077cc;
                color: white;
                border: none;
                border-radius: 8px;
                font-weight: bold;
                cursor: pointer;
                transition: background 0.3s;
            }}
            button.button:hover {{
                background: #005fa3;
            }}
            footer {{
                margin-top: 30px;
                font-size: 14px;
                color: #666;
            }}
        </style>
        <script>
            function copyLink(id) {{
                var copyText = document.getElementById(id).innerText;
                navigator.clipboard.writeText(copyText).then(function() {{
                    alert('✅ Tautan disalin ke clipboard!');
                }}, function(err) {{
                    alert('❌ Gagal menyalin tautan');
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
