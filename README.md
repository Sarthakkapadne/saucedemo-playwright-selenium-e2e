# 🎭 SauceDemo Playwright + Selenium E2E Automation Suite

[![CI Status](https://github.com/Sarthakkapadne/saucedemo-playwright-selenium-e2e/actions/workflows/ci.yml/badge.svg)](https://github.com/Sarthakkapadne/saucedemo-playwright-selenium-e2e/actions)
[![Tests Passing](https://img.shields.io/badge/tests-25%20passed-brightgreen.svg)](https://github.com/Sarthakkapadne/saucedemo-playwright-selenium-e2e)
[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-green.svg)](https://playwright.dev/)
[![Selenium](https://img.shields.io/badge/Selenium-4.20+-orange.svg)](https://www.selenium.dev/)
[![Allure Report](https://img.shields.io/badge/Allure-Reports%20Integrated-ff69b4.svg)](https://allurereport.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An enterprise-grade, dual-engine End-to-End (E2E) Test Automation Framework designed for the industry-standard **SauceDemo (Swag Labs)** e-commerce application. Built with **Page Object Model (POM)** architecture, cross-engine orchestration (**Playwright + Selenium WebDriver**), automated **Allure & HTML reporting** with failure screenshot attachments, and fully automated **GitHub Actions CI/CD**.

---

## 🏛️ Architecture & Highlights

```
saucedemo-playwright-selenium-e2e/
├── config/
│   ├── settings.py           # Centralized environment configuration & credentials
├── pages/                    # Page Object Model (POM) Abstractions
│   ├── base_page.py          # Playwright base page with resilient auto-waits
│   ├── login_page.py         # Login screen interactions & error banner assertions
│   ├── inventory_page.py     # Product listing, sorting, item adding/removing
│   ├── item_detail_page.py   # Product details inspection & navigation
│   ├── cart_page.py          # Shopping cart verification & item management
│   ├── checkout_page.py      # Checkout Step 1 (Info), Step 2 (Pricing), Complete
│   └── selenium_pages/       # Dedicated Selenium WebDriver POM implementation
│       ├── base_selenium_page.py     # Explicit WebDriverWait & stale-retry logic
│       ├── login_selenium_page.py    # Selenium authentication
│       ├── inventory_selenium_page.py# Selenium catalog management
│       ├── cart_selenium_page.py     # Selenium cart management
│       └── checkout_selenium_page.py # Selenium checkout & price verification
├── tests/                    # 25 Comprehensive Test Scenarios
│   ├── test_login_playwright.py          # 5 authentication test cases
│   ├── test_inventory_cart_playwright.py # 6 sorting, catalog & cart test cases
│   ├── test_checkout_playwright.py       # 4 checkout & price arithmetic cases
│   ├── test_login_selenium.py            # 4 Selenium authentication & SLA cases
│   ├── test_cart_selenium.py             # 3 Selenium cart & badge cases
│   └── test_checkout_selenium.py         # 3 Selenium checkout & cancellation cases
├── reports/                  # Generated HTML reports, Allure results & failure screenshots
├── conftest.py               # Fixtures, cross-browser setup, Allure failure hooks
├── pytest.ini                # Test marker configurations (smoke, regression, e2e)
├── run_tests.py              # Interactive CLI runner for suites and browsers
├── requirements.txt          # Python dependencies
└── .github/workflows/ci.yml  # GitHub Actions CI matrix workflow
```

---

## 🧪 25-Case Test Matrix

| Test ID | Engine | Suite / Tag | Test Description | Severity | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-E2E-01** | Playwright | `smoke`, `e2e` | Valid login with `standard_user` redirects to inventory catalog | Blocker | ✅ Passed |
| **TC-E2E-02** | Playwright | `regression` | Locked out user displays appropriate error banner | Critical | ✅ Passed |
| **TC-E2E-03** | Playwright | `regression` | Problem user login and inventory catalog render | Normal | ✅ Passed |
| **TC-E2E-04** | Playwright | `regression` | Empty username validation displays required field error | Normal | ✅ Passed |
| **TC-E2E-05** | Playwright | `regression` | Invalid password validation displays mismatch error | Critical | ✅ Passed |
| **TC-E2E-06** | Playwright | `smoke` | Adding multiple products dynamically updates cart badge count | Critical | ✅ Passed |
| **TC-E2E-07** | Playwright | `regression` | Removing product from catalog resets cart badge | Normal | ✅ Passed |
| **TC-E2E-08** | Playwright | `regression` | Sort catalog by Price: Low to High verifies ascending order | Normal | ✅ Passed |
| **TC-E2E-09** | Playwright | `regression` | Sort catalog by Price: High to Low verifies descending order | Normal | ✅ Passed |
| **TC-E2E-10** | Playwright | `regression` | Sort catalog by Name: Z to A verifies reverse alphabetical order | Normal | ✅ Passed |
| **TC-E2E-11** | Playwright | `regression` | Navigate to item detail page, verify price/desc & add to cart | Critical | ✅ Passed |
| **TC-E2E-12** | Playwright | `smoke`, `e2e` | Complete E2E checkout journey with subtotal + tax = total math | Blocker | ✅ Passed |
| **TC-E2E-13** | Playwright | `regression` | Checkout Step 1: Missing First Name validation error | Normal | ✅ Passed |
| **TC-E2E-14** | Playwright | `regression` | Checkout Step 1: Missing Postal Code validation error | Normal | ✅ Passed |
| **TC-E2E-15** | Playwright | `regression` | Cancel checkout returns user to cart with items intact | Normal | ✅ Passed |
| **TC-E2E-16** | Selenium | `smoke` | Valid login using Selenium WebDriver with explicit wait | Blocker | ✅ Passed |
| **TC-E2E-17** | Selenium | `regression` | Locked out user error banner verification via Selenium | Critical | ✅ Passed |
| **TC-E2E-18** | Selenium | `regression` | Empty credentials validation via Selenium | Normal | ✅ Passed |
| **TC-E2E-19** | Selenium | `regression` | Performance glitch user login latency monitored under SLA (<7s) | Normal | ✅ Passed |
| **TC-E2E-20** | Selenium | `smoke` | Add item to cart and assert cart counter badge in Selenium | Critical | ✅ Passed |
| **TC-E2E-21** | Selenium | `regression` | Remove item from cart page and verify empty cart state | Normal | ✅ Passed |
| **TC-E2E-22** | Selenium | `regression` | Continue Shopping navigation returns to inventory catalog | Normal | ✅ Passed |
| **TC-E2E-23** | Selenium | `smoke`, `e2e` | Complete checkout transaction and order receipt via Selenium | Blocker | ✅ Passed |
| **TC-E2E-24** | Selenium | `regression` | Missing Last Name input validation on checkout form | Normal | ✅ Passed |
| **TC-E2E-25** | Selenium | `regression` | Cancel at Step Two overview returns user back to inventory | Normal | ✅ Passed |

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.12)
- Google Chrome installed (for Selenium & Playwright)
- `uv` (recommended) or standard `pip`

### 2. Setup Environment
```bash
git clone https://github.com/Sarthakkapadne/saucedemo-playwright-selenium-e2e.git
cd saucedemo-playwright-selenium-e2e

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
python -m playwright install chromium
```

### 3. Run Tests via CLI Runner
```bash
# Run all 25 test cases (Playwright + Selenium)
python run_tests.py

# Run only Smoke tests
python run_tests.py --suite=smoke

# Run only Playwright suite
python run_tests.py --engine=playwright

# Run only Selenium suite
python run_tests.py --engine=selenium

# Run in headed mode (visible browser window)
python run_tests.py --headed
```

### 4. Direct Pytest Execution
```bash
# Run with HTML report
pytest --html=reports/report.html --self-contained-html

# Run with Allure results
pytest --alluredir=reports/allure-results
```

### 5. View Test Reports
- **Pytest HTML Report**: Open `reports/report.html` in any browser.
- **Allure Report**:
  ```bash
  allure serve reports/allure-results
  ```

---

## 🔄 CI/CD Pipeline
Automated via `.github/workflows/ci.yml` on every `push` and `pull_request` to `main`:
1. Environment provisioning (Ubuntu Latest, Python 3.12, Chromium).
2. Headless execution of all 25 E2E test cases.
3. Automatic screenshot capture on failure.
4. Generates and uploads Pytest HTML & Allure test artifact packages.

---

## 👨‍💻 Author
**Sarthak Kapadne**  
QA Engineer & Test Automation Specialist  
- GitHub: [@Sarthakkapadne](https://github.com/Sarthakkapadne)  
- LinkedIn: [sarthak-kapadne](https://linkedin.com/in/sarthak-kapadne)  
- Email: [sarthakkapadne6086@gmail.com](mailto:sarthakkapadne6086@gmail.com)
