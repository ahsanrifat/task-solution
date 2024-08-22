import asyncio
from playwright.async_api import async_playwright
import time

async def close_popup(popup_id,page):
    try:
        return await page.click(popup_id)
    except:
        print("Popup not found or already closed")

async def login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://app.cosmosid.com/search')
        await close_popup('#new-features-dialog--close',page)
        await page.fill('input[name="email"]', 'demo_estee2@cosmosid.com')
        await page.fill('input[name="password"]', 'xyzfg321')
        await page.click('button[type="submit"]')
        
        # Wait for navigation to complete
        await page.wait_for_load_state('networkidle')
        await close_popup('#intro-tour--functional-2-tour--close-button',page)
        await page.click('a:has-text("R-elb")')
        await page.click('a:has-text("SRR2005421_11_1_R-elb_0_30")')
        await page.click('button:has-text("Export current results")')
        return page
    
async def main():
    page = await login()

asyncio.run(main())