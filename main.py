import feedparser
import google.generativeai as genai
import os

def get_news():
    # 抓取 CISA 與 Defense One 新聞
    feeds = ["https://www.cisa.gov/cybersecurity-alerts.xml", "https://www.defenseone.com/rss/all/"]
    all_content = ""
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for entry in f.entries[:2]:
                all_content += f"Title: {entry.title}\nSummary: {entry.summary}\n\n"
        except:
            continue
    return all_content if all_content else "Recent cybersecurity and defense infrastructure updates."

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # 修正：改用最穩定的模型名稱 gemini-pro
    model = genai.GenerativeModel('gemini-pro')
    
    news_data = get_news()
    
    prompt = f"""
    You are a professional English tutor. Please use the following news to create a C1-level English study guide in Traditional Chinese:
    News: {news_data}
    
    Format:
    1. A rewrite of the news in advanced C1 English (about 300 words).
    2. 5 Key academic/technical vocabulary with Chinese definitions and example sentences.
    3. One grammar point analysis (complex sentence).
    4. 2 Reading comprehension questions.
    """
    
    try:
        response = model.generate_content(prompt)
        # 確保檔案一定會產生
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Successfully generated Daily_Study.md")
    except Exception as e:
        # 萬一 AI 真的失敗，產生一個錯誤說明檔，避免 Commit 報錯
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(f"Generation failed: {str(e)}")
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
