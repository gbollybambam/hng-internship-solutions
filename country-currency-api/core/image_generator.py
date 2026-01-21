import os
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

IMAGE_PATH = os.path.join(settings.BASE_DIR, 'cache', 'summary.png')

def generate_summary_image(total_countries, top_5_gdp, last_refreshed_at):
    width, height = 800, 400
    bg_color = (15, 23, 42)
    text_color = (226, 232, 240) 
    header_color = (56, 189, 248) 

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font_path = "C:/Windows/Fonts/arial.ttf"
        header_font = ImageFont.truetype(font_path, 36)
        body_font = ImageFont.truetype(font_path, 18)
        small_font = ImageFont.truetype(font_path, 14)
    except IOError:
        header_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    draw.text((40, 30), "API Status Summary", font=header_font, fill=header_color)

    draw.text((40, 100), f"Total Countries Cached: {total_countries}", font=body_font, fill=text_color)

    draw.text((40, 150), "Top 5 Countries by Estimated GDP:", font=body_font, fill=header_color)

    y_position = 180
    for i, country in enumerate(top_5_gdp, 1):
        gdp_in_billions = country.estimated_gdp / 1_000_000_000
        line = f"{i}. {country.name} (${gdp_in_billions:,.2f}B)"
        draw.text((60, y_position), line, font=body_font, fill=text_color)
        y_position += 30

    formatted_time = last_refreshed_at.strftime('%Y-%m-%d %H:%M:%S UTC')
    draw.text((40, height - 40), f"Last Refresh: {formatted_time}", font=small_font, fill=text_color)

    os.makedirs(os.path.dirname(IMAGE_PATH), exist_ok=True)
    img.save(IMAGE_PATH)
    print(f"Summary image saved to {IMAGE_PATH}")