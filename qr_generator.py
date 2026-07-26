import qrcode

BASE_URL = "http://127.0.0.1:5000"

def generate_qr(table_id, table_number):
    url = f"{BASE_URL}/menu/{table_id}"
    img = qrcode.make(url)
    path = f"static/qr/table_{table_number}.png"
    img.save(path)
    return path