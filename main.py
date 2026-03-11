import feedparser
import google.generativeai as genai
import os

def get_news():
    feeds = ["https://www.cisa.gov/cybersecurity-alerts.xml", "https://www.defenseone.com/rss/all/"]
    all_content = ""
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for entry in f.entries[:2]:
                all_content += f"Title: {entry.title}\nSummary: {entry.summary}\n\n"
        except:
            continue
    return all_content if all_content else "Recent C5ISR and cybersecurity updates."

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # 修正重點：使用正確的模型名稱
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    news_data = get_news()
    
    prompt = f"""
    You are a professional C1 English tutor. Use this news: {news_data}
    Create a study guide in Traditional Chinese:
    1. Article: Rewrite the news into a 300-word academic article (C1 level).
    2. Vocabulary: 5 Advanced terms with definitions and example sentences.
    3. Grammar: Analyze one complex sentence from the text.
    4. Quiz: 2 Reading comprehension questions with answers.
    """
    
    try:
        response = model.generate_content(prompt)
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Success!")
    except Exception as e:
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
