from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import json
import re
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok", "message": "AI Service running"}), 200

@app.route('/analyze', methods=['POST'])
def analyze_review():
    try:
        # convert the incoming request JSON data to a Python dictionary to handle the review text 
        data = request.get_json(silent=True) or {}
        review_text = data.get('text', '')
        if not review_text:
            return jsonify({"error": "No text provided"}), 400
        
        # Prepare the prompt for the AI model
        prompt = f"""
        Analyze the following customer review and return ONLY JSON:
        ---
        {review_text}
        ---
        The JSON must include exactly these keys:
        sentiment: "positive", "neutral" or "negative"
        spam: true or false
        score: number between 0 and 1
        problems: array of short strings of issues (can be empty)
        goodPoints: array of short strings of positives (can be empty)

        ONLY output JSON. No extra text or formatting like ```json fences.
        """
        # calling the OpenAI API to get response 
        resp = client.responses.create(
            model="gpt-4o",
            input=prompt,
            temperature=0
        )

        # Extract the output text from the response and cleaning it if necessary
        result_text = resp.output_text.strip()
        clean_text = re.sub(r"^```json\s*|\s*```$", "", result_text, flags=re.MULTILINE)

        try:
            result = json.loads(clean_text)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid JSON from model", "raw": result_text}), 500

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/summary', methods=['POST'])
def summarize_reviews():
    try:
        data = request.get_json(silent=True) or {}
        
        problems = data.get('problems', [])
        good_points = data.get('goodPoints', [])
        
        # print(f"Problems: {problems}")
        # print(f"Good points: {good_points}")
        # print(f"Problems count: {len(problems)}, Good points count: {len(good_points)}")

        if not problems and not good_points:
            return jsonify({"summary": "No reviews available yet."})

        # Limit data to avoid token issues
        limited_problems = problems[:50]
        limited_good_points = good_points[:50]

        prompt = f"""
        Summarize the following customer feedback into clear insights.
        Problems reported: {limited_problems}
        Good points mentioned: {limited_good_points}

        Return STRICT JSON with:
        summary: a short text summarizing the top complaints and top praises.
        """

        resp = client.responses.create(
            model="gpt-4o",
            input=prompt,
            temperature=0
        )

        result_text = resp.output_text.strip()
        
        # Clean the response
        clean_text = re.sub(r"^```json\s*|\s*```$", "", result_text, flags=re.MULTILINE)

        result = json.loads(clean_text)
        
        return jsonify(result)
        
    except json.JSONDecodeError as e:
        return jsonify({
            "summary": f"Analysis complete: {len(problems)} issues, {len(good_points)} positives found."
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/suggestions', methods=['POST'])
def improvement_suggestions():
    try:
        data = request.get_json(silent=True) or {}
        problems = data.get('problems', [])
        good_points = data.get('goodPoints', [])

        if not problems and not good_points:
            return jsonify({"suggestions": ["No reviews available to analyze."]})

        prompt = f"""
        You are an AI that outputs ONLY JSON.
        Based on the following customer feedback, suggest actionable steps to improve the service.

        Problems reported: {problems}
        Good points mentioned: {good_points}

        Return STRICT JSON in this format:
        {{
          "suggestions": ["...", "...", "..."]
        }}
        """

        resp = client.responses.create(
            model="gpt-4o",
            input=prompt,
            temperature=0
        )

        result_text = resp.output_text.strip()
        print("[/suggestions] Raw AI response:", result_text)  # 👈 log AI output

        clean_text = re.sub(r"^```json\s*|\s*```$", "", result_text, flags=re.MULTILINE)

        try:
            result = json.loads(clean_text)
            return jsonify(result)
        except json.JSONDecodeError as e:
            print("[/suggestions] JSON decode error:", str(e))
            return jsonify({
                "suggestions": ["Suggestions are not available at this moment."]
            })

    except Exception as e:
        print("[/suggestions] Fatal error:", str(e))  # 👈 log fatal errors
        return jsonify({
            "suggestions": ["Suggestions are not available at this moment."]
        }), 200  # 👈 don’t send 500, send safe fallback




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
