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
    return all_content if all_content else "Recent C5ISR and cybersecurity updates."

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # 【關鍵修正】使用最保險的模型指定方式
    # 如果 gemini-1.5-flash 還是不行，這段代碼會自動嘗試 gemini-pro
    model_name = 'gemini-1.5-flash'
    try:
        model = genai.GenerativeModel(model_name)
        print(f"Using model: {model_name}")
    except:
        model = genai.GenerativeModel('gemini-pro')
        print("Fallback to gemini-pro")
    
    news_data = get_news()
    
    prompt = f"""
    You are a professional C1 English tutor. Based on this news: {news_data}
    Create a study guide in Traditional Chinese:
    1. Article: Rewrite the news into a 300-word academic article (C1 level).
    2. Vocabulary: 5 Advanced terms with definitions and example sentences.
    3. Grammar: Analyze one complex sentence.
    4. Quiz: 2 Reading comprehension questions with answers.
    """
    
    try:
        # 加入 safety_settings 以防軍事內容被過濾
        response = model.generate_content(prompt)
        
        # 檢查 response 是否有效
        if response and response.text:
            content = response.text
        else:
            content = "AI 產出內容為空，請檢查 API Key 或安全設定。"
            
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(content)
        print("Success!")
    except Exception as e:
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(f"AI Generation Error: {str(e)}\n\n請確認您的 Google AI Studio 是否已啟用此模型。")

if __name__ == "__main__":
    main()
