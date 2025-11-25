from playwright.sync_api import Page, expect, sync_playwright

def verify_redesign(page: Page):
    # 1. Arrange: Go to the blog homepage.
    page.goto("http://localhost:4000/")

    # 2. Act: Check for new design elements.

    # Check Hero Section
    expect(page.locator(".hero-title")).to_contain_text("Hi, I'm Jacob")

    # Check Card Grid
    expect(page.locator(".grid").first).to_be_visible()

    # Check Header Layout (Nav should be present)
    expect(page.locator(".site-header")).to_be_visible()

    # 3. Screenshot: Capture the new home page
    page.screenshot(path="/app/verification/redesign_home.png", full_page=True)

    # 4. Navigate to Projects Page
    page.click("text=Projects")
    expect(page).to_have_url("http://localhost:4000/projects/")

    # 5. Screenshot: Capture the projects page
    page.screenshot(path="/app/verification/redesign_projects.png", full_page=True)

    # 6. Navigate to a Blog Post
    page.goto("http://localhost:4000/blog/")
    # Taking screenshot of blog index (which uses post list usually, or home layout?)
    # Wait, my blog link points to /blog/ but I didn't update `blog.html` explicitly in the "Layout Overhaul" step plan details,
    # but I did update `main.scss` global styles.
    # Let's check if /blog/ layout exists.
    # I verified `docs/_layouts/blog.html` exists in previous turn.
    # I should update `blog.html` to use the new grid system too if it doesn't already.
    # But let's verify what it looks like first.

    page.screenshot(path="/app/verification/redesign_blog_index.png", full_page=True)


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1200, "height": 800})
        try:
            verify_redesign(page)
            print("Verification script ran successfully.")
        except Exception as e:
            print(f"Verification failed: {e}")
        finally:
            browser.close()
