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
    
    # 使用相容性最高的模型名稱
    model = genai.GenerativeModel('gemini-pro')
    
    news_data = get_news()
    
    prompt = f"""
    You are a professional C1 English tutor. Use this news: {news_data}
    Create a study guide in Traditional Chinese:
    1. Rewrite the news into a 300-word academic article (C1 level).
    2. 5 Advanced vocabulary with definitions and example sentences.
    3. One grammar analysis of a complex sentence.
    4. 2 Reading comprehension questions with answers.
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text if response.text else "AI generation failed but script ran."
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(content)
        print("File Daily_Study.md created successfully.")
    except Exception as e:
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(f"Error during AI generation: {str(e)}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
