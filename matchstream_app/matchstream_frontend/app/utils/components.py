from datetime import datetime

def calculate_age(dob_str: str) -> str:
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return str(age)
    except Exception:
        return ""

def profile_card_html(p: dict, photo_size_px: int = 260) -> str:
    photo_url = p.get("picture") or "https://via.placeholder.com/400?text=No+Photo"
    name = f"{p.get('first_name','')} {p.get('last_name','')}".strip()
    age = calculate_age(p.get("dob", ""))
    city = p.get("city", "")
    state = p.get("state", "")
    location = ", ".join([x for x in [city, state] if x])

    email = p.get("email", "")
    phone = p.get("phone", "")

    return f"""
    <div class="center" style="margin: 10px 0 16px 0;">
      <img src="{photo_url}" style="
        width:{photo_size_px}px;
        height:{photo_size_px}px;
        border-radius:50%;
        object-fit:cover;
        border: 3px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 28px rgba(0,0,0,0.35);
      ">
    </div>

    <div class="card">
      <div style="font-size:28px; font-weight:800;">{name}</div>
      <div class="muted" style="margin-top:4px;">
        {"🎂 " + age + " years old" if age else ""}
        {" · 📍 " + location if location else ""}
      </div>
      <div style="margin-top:10px;">
        {"✉️ " + email if email else ""}
        {"<br>📞 " + phone if phone else ""}
      </div>
    </div>
    """