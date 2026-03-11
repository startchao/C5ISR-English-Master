import feedparser
import google.generativeai as genai
import os

# 1. 安全設定：避免國防資安術語被誤擋
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

def get_news():
    # 改用更穩定的來源測試
    feeds = ["https://www.cisa.gov/cybersecurity-alerts.xml"]
    all_content = ""
    try:
        for url in feeds:
            f = feedparser.parse(url)
            for entry in f.entries[:3]:
                all_content += f"Title: {entry.title}\nSummary: {entry.summary}\n\n"
    except Exception as e:
        print(f"Error fetching news: {e}")
    return all_content if all_content else "No news found today."

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    news_data = get_news()
    
    prompt = f"""
    Role: Expert English Tutor for C1 Level (CEFR).
    Task: Use the following cybersecurity/defense news to create a study sheet.
    Context: {news_data}
    
    Requirements (Traditional Chinese):
    1. Rewrite into a 400-word academic article (C1 Level).
    2. List 5 key technical/academic terms with definitions.
    3. Analyze 1 complex sentence structure.
    4. Provide 2 reading comprehension questions.
    """
    
    try:
        response = model.generate_content(prompt, safety_settings=safety_settings)
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(f"# Daily C5ISR English Study\n\n{response.text}")
        print("Success: Daily_Study.md generated.")
    except Exception as e:
        print(f"AI Generation Error: {e}")

if __name__ == "__main__":
    main()
