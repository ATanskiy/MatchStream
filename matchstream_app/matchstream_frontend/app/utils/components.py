from datetime import datetime

def calculate_age(dob_str: str) -> str:
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return str(age)
    except Exception:
        return ""

def profile_card_html(p: dict, photo_size_px: int = 280) -> str:
    photo_url = p.get("picture") or "https://via.placeholder.com/400?text=No+Photo"
    name = f"{p.get('first_name','')} {p.get('last_name','')}".strip()

    gender = p.get("gender", "")
    age = calculate_age(p.get("dob", ""))

    birthday = ""
    try:
        birthday = datetime.strptime(p.get("dob", ""), "%Y-%m-%d").strftime("%d %B %Y")
    except Exception:
        pass

    city = p.get("city", "")
    state = p.get("state", "")
    location = ", ".join([x for x in [city, state] if x])

    email = p.get("email", "")
    phone = p.get("phone", "")

    return f"""
    <div class="center" style="margin: 14px 0 18px 0;">
      <img src="{photo_url}" style="
        width:{photo_size_px}px;
        height:{photo_size_px}px;
        border-radius:50%;
        object-fit:cover;
        border: 3px solid rgba(255,255,255,0.08);
        box-shadow: 0 12px 32px rgba(0,0,0,0.35);
      ">
    </div>

    <div class="card">
      <div style="font-size:28px; font-weight:800;">About Me:</div>

      {"<div class='muted' style='margin-top:8px;'>⚧️ " + gender.capitalize() + "</div>" if gender else ""}

      {"<div class='muted' style='margin-top:4px;'>🎂 " + age + " years old</div>" if age else ""}

      {"<div class='muted' style='margin-top:4px;'>📅 Born on " + birthday + "</div>" if birthday else ""}

      {"<div class='muted' style='margin-top:6px;'>📍 " + location + "</div>" if location else ""}

      <div style="margin-top:12px;">
        {"✉️ " + email if email else ""}
        {"<br>📞 " + phone if phone else ""}
      </div>
    </div>
    """