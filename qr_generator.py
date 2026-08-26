import qrcode

BASE_URL = "https://naqshbandi177.pythonanywhere.com"

def generate_qr(table_id, table_number):
    url = f"{BASE_URL}/menu/{table_id}"
    img = qrcode.make(url)
    save_path = f"static/qr/table_{table_number}.png"
    db_path = f"/static/qr/table_{table_number}.png"
    img.save(save_path)
    return db_path