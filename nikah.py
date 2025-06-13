from flask import Flask, render_template_string, url_for
from pyngrok import ngrok
import qrcode
import io
import base64
import threading

app = Flask(__name__)

# QR Code Generator
def generate_qr_code(data):
    qr = qrcode.QRCode(version=1, box_size=8, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('ascii')

# Route utama
@app.route("/")
def index():
    lokasi = "https://www.google.com/maps/place/Tirtayasa,+Banten,+Indonesia"
    qr_base64 = generate_qr_code(lokasi)
    
    anime_img = url_for('static', filename='anime.jpg')
    ornament_img = url_for('static', filename='ornament1.png')

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Undangan Pernikahan Bayu & Husniyah</title>
        <style>
            body {{
                background: linear-gradient(#fffaf4, #ffe4e1);
                font-family: 'Arial', sans-serif;
                text-align: center;
                padding: 20px;
                color: #5a3e36;
            }}
            .card {{
                background: white;
                padding: 30px;
                margin: auto;
                max-width: 700px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                border-radius: 15px;
            }}
            img.anime {{
                width: 180px;
                border-radius: 20px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }}
            img.ornament {{
                width: 100px;
                margin-top: 20px;
            }}
            .qr img {{
                width: 180px;
                border-radius: 10px;
                margin-top: 20px;
            }}
            .btn {{
                display: inline-block;
                margin-top: 30px;
                background: #d97d54;
                color: white;
                padding: 12px 30px;
                border-radius: 30px;
                text-decoration: none;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <img src="{anime_img}" class="anime" alt="Gambar Anime" />
            <h1>Undangan Pernikahan</h1>
            <h2>Bayu Putra Tama & Husniyah</h2>
            <p>Dengan bahagia, kami mengundang Anda untuk hadir di hari istimewa kami.</p>
            <p><strong>Tanggal:</strong> 30 Juni 2027</p>
            <p><strong>Lokasi:</strong> Tirtayasa, Banten</p>
            
            <img src="{ornament_img}" class="ornament" alt="Ornamen" />

            <div class="qr">
                <p>Scan QR untuk petunjuk lokasi:</p>
                <img src="data:image/png;base64,{qr_base64}" alt="QR Lokasi" />
            </div>

            <a href="https://wa.me/6281234567890?text=Halo%20saya%20ingin%20konfirmasi%20hadir%20di%20pernikahan%20Bayu%20dan%20Husniyah" class="btn">Konfirmasi Kehadiran</a>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

# Jalankan ngrok di background
def start_ngrok():
    try:
        url = ngrok.connect(5000)
        print(f"[🌐] Undangan online tersedia di: {url}")
    except Exception as e:
        print(f"[❌] Gagal konek ke ngrok: {e}")

# Main entry point
if __name__ == "__main__":
    threading.Thread(target=start_ngrok).start()
    app.run(host="0.0.0.0", port=5000)

