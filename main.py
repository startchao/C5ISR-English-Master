import feedparser
import google.generativeai as genai
import os

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = models[0] if models else 'gemini-1.5-flash'
    except:
        target_model = 'gemini-1.5-flash'

    model = genai.GenerativeModel(target_model)
    
    # 精選高階新聞源
    feeds = [
        "https://www.economist.com/international/rss.xml",
        "https://foreignpolicy.com/feed/",
        "https://api.quantamagazine.org/feed/"
    ]
    
    news_text = ""
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for entry in f.entries[:1]:
                news_text += f"Topic: {entry.title}\nContext: {entry.summary}\n\n"
        except: continue

    # 修正後的 Prompt：強制要求先產出英文長文，再進行中文解析
    prompt = f"""
    Target: FLPT Level C1+ (Goal: Score 240+).
    Topic Materials: {news_text}
    
    Please structure the response as follows to ensure English immersion with Chinese support:

    1. [English Essay] 
       Write a 400-word academic essay based on the topics. 
       - Level: C1 Advanced. 
       - Requirement: Use sophisticated vocabulary and complex sentence structures (e.g., conditional sentences, inversion, and passive voice).

    2. [Chinese Analysis - 文章結構與邏輯]
       Briefly explain the essay's logical flow and transition markers in Traditional Chinese.

    3. [Vocabulary & Phrases - 核心詞彙與短句]
       List 8 Power Vocabularies/Phrases from the essay.
       - Format: Word/Phrase + IPA + Part of Speech.
       - Chinese Definition + English Explanation.
       - A real-world example sentence.

    4. [FLPT Quiz - 模擬測驗]
       2 Multiple-choice questions in English based on the essay. 
       - Focus on INFERENCE (reading between the lines). 
       - Provide answers and detailed explanations in Traditional Chinese at the end.
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(content)
            
        # 轉換成 HTML 並美化
        display_content = content.replace('# ', '<h1>').replace('## ', '<h2>').replace('\n', '<br>')
        
        html_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>FLPT C1 Advanced Study</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css">
            <style>
                body {{ box-sizing: border-box; min-width: 200px; max-width: 900px; margin: 0 auto; padding: 20px; }}
                .markdown-body {{ padding: 30px; background: #fff; }}
                h1 {{ color: #1a73e8; border-bottom: 3px solid #1a73e8; }}
                h2 {{ color: #202124; background: #f1f3f4; padding: 8px; border-radius: 4px; }}
                .essay-box {{ line-height: 1.8; font-size: 1.1em; color: #3c4043; }}
            </style>
        </head>
        <body class="markdown-body">
            <div style="text-align:right; font-weight:bold; color:#1a73e8;">Target: FLPT 240+</div>
            {article}
        </body>
        </html>
        """
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_template.format(article=display_content))
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
