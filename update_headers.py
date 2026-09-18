import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

header_html = '''<div class="universal-app-header" style="position: absolute; top: 0; left: 0; width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 20px 24px; z-index: 1000; pointer-events: none; box-sizing: border-box;">
    <!-- LEFT: Ride App Logo -->
    <div style="pointer-events: auto; display: flex; align-items: center;">
        <div style="background-color: #dc2626; color: white; width: 44px; height: 44px; border-radius: 10px; display: flex; justify-content: center; align-items: center; font-weight: 900; font-size: 26px; font-family: sans-serif; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">H</div>
    </div>
    
    <!-- RIGHT: Joining Hands Logo & Home -->
    <div style="pointer-events: auto; display: flex; align-items: center; gap: 16px;">
        <div style="font-weight: 800; color: #1e293b; display: flex; align-items: center; gap: 8px; font-size: 1.2rem; background: rgba(255,255,255,0.9); padding: 8px 14px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); backdrop-filter: blur(5px);">
            <span>Joining Hands</span> <i class="fa-solid fa-handshake-angle" style="color: #f97316;"></i>
        </div>
        <button onclick="returnToLanding()" style="background: none; border: none; cursor: pointer; padding: 0; outline: none; transition: transform 0.2s; display: flex; align-items: center; justify-content: center;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'" aria-label="Go back to main screen">
            <img src="/static/images/new_home_icon.png" alt="Home" style="width: 48px; height: 48px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));">
        </button>
    </div>
</div>'''

# 1. Update Red App floating button container
html = re.sub(
    r'<div style="padding: 24px; position: absolute; top: 0; left: 0; z-index: 100;">\s*<button.*?returnToLanding.*?</button>\s*</div>',
    header_html,
    html,
    flags=re.DOTALL
)

# 2. Update Insta View floating button container
html = re.sub(
    r'<div style="position: absolute; top: 20px; left: 20px;">\s*<button.*?returnToLanding.*?</button>\s*</div>',
    header_html,
    html,
    flags=re.DOTALL
)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html headers")
