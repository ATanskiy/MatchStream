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
    age = calculate_age(p.get("dob", ""))

    gender = p.get("gender", "")
    dob = p.get("dob", "")
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
        border: 4px solid white;
        box-shadow: 0 14px 36px rgba(0,0,0,0.25);
      ">
    </div>

    <div class="card">
      <div style="font-size:24px; font-weight:800;">About Me:</div>

      <div style="margin-top:10px;">
        {"👤 " + gender.capitalize() if gender else ""}
      </div>

      <div style="margin-top:6px;">
        {"🎂 " + age + " years old" if age else ""}
      </div>

      <div style="margin-top:6px;">
        {"📅 Born on " + dob if dob else ""}
      </div>

      <div style="margin-top:6px;">
        {"📍 " + location if location else ""}
      </div>

      <div style="margin-top:10px;">
        {"✉️ " + email if email else ""}
      </div>

      <div style="margin-top:6px;">
        {"📞 " + phone if phone else ""}
      </div>
    </div>
    """