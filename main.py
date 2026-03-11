import feedparser
import google.generativeai as genai
import os

# 從 GitHub Secrets 讀取 API Key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def get_news():
    # 抓取 CISA (資安) 與 Defense One (國防科技)
    feeds = ["https://www.cisa.gov/cybersecurity-alerts.xml", "https://www.defenseone.com/rss/all/"]
    all_content = ""
    for url in feeds:
        f = feedparser.parse(url)
        for entry in f.entries[:2]: # 每個來源取前兩則
            all_content += f"Title: {entry.title}\nSummary: {entry.summary}\n\n"
    return all_content

def main():
    news_data = get_news()
    prompt = f"""
    You are an expert English tutor specializing in C1 Level Academic English and Military/Cybersecurity domains (C5ISR).
    Based on these news summaries: {news_data}
    
    Please generate a comprehensive study sheet in Traditional Chinese:
    1. **C1 Level Article**: Rewrite the news into a cohesive 400-word article using advanced C1 vocabulary and complex sentence structures.
    2. **Academic Vocabulary**: List 8 advanced words related to C5ISR, Network Security, or Communications with definitions and example sentences.
    3. **Grammar Analysis**: Pick 2 complex sentences from the rewritten text and explain their syntax (e.g., inversion, subjunctive mood).
    4. **C1 Quiz**: 3 Multiple-choice questions testing inference and nuance, with detailed explanations.
    """
    response = model.generate_content(prompt)
    
    with open("Daily_Study.md", "w", encoding="utf-8") as f:
        f.write(f"# 每日 C5ISR 英文進階學習\n\n{response.text}")

if __name__ == "__main__":
    main()
