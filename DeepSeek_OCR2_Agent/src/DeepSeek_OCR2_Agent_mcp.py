from fastmcp import FastMCP
from PIL import Image, ImageDraw, ImageFont
import base64
import io

mcp = FastMCP(name="DeepSeek_OCR2_Agent")

@mcp.tool()
async def draw_architecture_v2(commands: list) -> list:
    """
    Advanced drawing tool for architectural diagrams.
    Supports: 'rect' (solid/dashed), 'token_strip', 'label', 'arrow'.
    """
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGB', (1200, 800), color='white')
    draw = ImageDraw.Draw(img)

    for cmd in commands:
        t = cmd.get('type')
        c = cmd.get('coords') # [x1, y1, x2, y2]
        color = cmd.get('color', 'black')
        
        if t == 'rect':
            fill = cmd.get('fill', None)
            draw.rectangle(c, outline=color, fill=fill, width=2)
        elif t == 'token_strip':
            # Draws a row of colored blocks representing tokens
            x_start, y_start = c[0], c[1]
            colors = ['#FFD700', '#FFFACD', '#FFD700', '#B8860B'] # The yellow/gold palette
            for i, clr in enumerate(colors):
                draw.rectangle([x_start + (i*40), y_start, x_start + (i*40) + 30, y_start + 40], fill=clr)
        elif t == 'arrow':
            draw.line(c, fill=color, width=3)
            # Simple arrowhead logic
            draw.polygon([c[2], c[3], c[2]-10, c[3]-5, c[2]-10, c[3]+5], fill=color)
        elif t == 'text':
            draw.text((c[0], c[1]), cmd.get('text'), fill=color)

    # Convert to Base64
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return [{"type": "image", "data": base64.b64encode(buf.read()).decode('utf-8'), "mimeType": "image/png"}]
