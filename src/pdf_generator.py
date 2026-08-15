from pathlib import Path
from playwright.sync_api import sync_playwright


def html_to_pdf(html_path, pdf_path):
    html_path = Path(html_path).resolve()
    pdf_path = Path(pdf_path).resolve()

    pdf_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with sync_playwright() as p:

        browser = p.chromium.launch()

        page = browser.new_page(
            viewport={
                "width": 800,
                "height": 1123
            }
        )

        page.goto(
            html_path.as_uri(),
            wait_until="networkidle"
        )

        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            margin={
                "top": "0",
                "right": "0",
                "bottom": "0",
                "left": "0"
            }
        )

        browser.close()

    print(f"PDF generated: {pdf_path}")