# WELLTH

A modern fitness and wellness marketing platform built with HTML, CSS, and JavaScript.

---

## Overview

WELLTH is a multi-page marketing website for a fitness and wellness brand. It presents pricing plans, trainer profiles, and platform features in a clean, professional aesthetic — designed to convert visitors into members.

---

## Pages

| Page | File | Description |
|------|------|-------------|
| Home | `index.html` | Hero section, features overview, and call-to-action |
| Pricing | `pricing.html` | Monthly/annual billing toggle, plan cards, FAQ accordion |
| Trainers | `trainers.html` | Trainer profiles with specialty filters |

---

## Features

- **Billing toggle** — Switch between monthly and annual pricing with live price updates
- **FAQ accordion** — Expandable questions and answers on the pricing page
- **Trainer filters** — Filter trainer cards by specialty (strength, yoga, cardio, etc.)
- **Responsive layout** — Mobile-friendly across all pages
- **Pastel aesthetic** — Soft color palette with clean typography; no emoji in the UI

---

## Tech Stack

- HTML5
- CSS3 (custom properties, flexbox, grid), Bootstrap
- JavaScript 

---

## Project Structure

```
wellth/
├── wellth-home.html
├── wellth-workout.html
├── wellth-professionals.html
├── wellth-meals.html
├── wellth-budgeting.html
├── wellth-login.html
├── css/
│   └── style.css
├── js/
│   └── main.js
└── assets/
    └── meals
    └── professionals
    └── worouts


```


## Getting Started


```bash
# Using Python
python -m http.server 8000

Then visit `http://localhost:8000` in your browser.

---

## Design Notes

- Color palette uses soft pastels with high-contrast text for readability
- Typography relies on Google Fonts set as the root-level default in CSS
- UI is intentionally minimal — no icons, no emoji, professional tone throughout

---

## Status

Active development.
