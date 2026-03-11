import feedparser
import google.generativeai as genai
import os

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    # 自動尋找可用模型
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = models[0] if models else 'models/gemini-1.5-flash'
    except:
        target_model = 'gemini-1.5-flash'

    model = genai.GenerativeModel(target_model)
    
    # 抓取新聞
    news_feed = feedparser.parse("https://www.cisa.gov/cybersecurity-alerts.xml")
    news_text = "\n".join([f"{e.title}: {e.summary}" for e in news_feed.entries[:3]])
    
    prompt = f"Role: C1 English Tutor. Use this news: {news_text}. Task: Rewrite in C1 level English, provide 5 academic vocabs, 1 grammar point, and 2 quiz questions. Use Traditional Chinese for explanations. Format: Markdown."
    
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        # 1. 存成 Markdown (備份與記錄用)
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(content)
            
        # 2. 存成 index.html (專屬網頁版)
        # 先處理內容的換行與標題
        display_content = content.replace('# ', '<h1>').replace('## ', '<h2>').replace('\n', '<br>')
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>每日 C1 英文學習</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css">
            <style>
                body { box-sizing: border-box; min-width: 200px; max-width: 980px; margin: 0 auto; padding: 45px; }
                @media (max-width: 767px) { body { padding: 15px; } }
            </style>
        </head>
        <body class="markdown-body">
            {article}
        </body>
        </html>
        """
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_template.format(article=display_content))
            
        print("Successfully generated index.html")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
