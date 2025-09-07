# AI Services for ReviewAI

This directory contains the Python microservice responsible for AI-powered review analysis (sentiment, spam detection, and suggestions) in the ReviewAI platform.

---

## Features
- Sentiment analysis of user reviews
- Spam detection
- Suggestions and summary generation
- Integrates with OpenAI API

---

## Tech Stack
- **Language:** Python 3
- **Framework:** Flask
- **AI:** OpenAI API

---

## Setup Instructions

1. Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```sh
   pip install -r requirement.txt
   ```
3. Configure your `.env` file with the OpenAI API key and other secrets.
4. Run the Flask app:
   ```sh
   python app.py
   ```

---

## Live Demo
[https://priyanshu8346.github.io/reviews_app_frontend/](https://priyanshu8346.github.io/reviews_app_frontend/)

---

## Related Repositories
- **AI Service:** [https://github.com/priyanshu8346/ai_services_reviewAI](https://github.com/priyanshu8346/ai_services_reviewAI)
- **Backend:** [https://github.com/priyanshu8346/Reviews_app](https://github.com/priyanshu8346/Reviews_app)
- **Frontend:** [https://github.com/priyanshu8346/reviews_app_frontend](https://github.com/priyanshu8346/reviews_app_frontend)

---

## License
MIT License
