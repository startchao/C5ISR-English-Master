import feedparser
import google.generativeai as genai
import os

def main():
    # 1. API 設定
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = models[0] if models else 'gemini-1.5-flash'
    except:
        target_model = 'gemini-1.5-flash'

    model = genai.GenerativeModel(target_model)
    
    # 2. 精選高階新聞來源 (經濟、外交、科學)
    feeds = [
        "https://www.economist.com/international/rss.xml",
        "https://foreignpolicy.com/feed/",
        "https://api.quantamagazine.org/feed/"
    ]
    
    news_text = ""
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for entry in f.entries[:2]:
                news_text += f"Topic: {entry.title}\nSummary: {entry.summary}\n\n"
        except: continue

    if len(news_text) < 100:
        news_text = "Global strategic stability, the evolution of academic discourse, and technological ethics."

    # 3. 針對 FLPT 240+ 深度閱讀設計的指令
    prompt = f"""
    Target: FLPT Level C1+ (Score 240+).
    Input Materials: {news_text}
    
    Task: Write ONE contiguous 500-word academic analysis in English. 
    Requirements:
    - Use C1 Advanced vocabulary and complex sentence structures (inversion, subjunctive, etc.).
    - Focus on a professional, news-magazine tone.
    - Organize into 3-4 clear paragraphs.

    After the essay, provide the following in Traditional Chinese:
    1. A brief logic analysis of the essay.
    2. 8 Power Vocabularies (Word + IPA + Definition + Chinese Meaning + Example).
    3. 2 Inference-based multiple-choice questions in English with Chinese explanations.
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        # 儲存 Markdown 備份
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(content)
            
        # 4. 生成 HTML - 紐約時報極簡字體排版版
        display_content = content.replace('# ', '<h1>').replace('## ', '<h2>').replace('\n', '<br>')
        
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>C1 Advanced: Daily Immersion</title>
            <style>
                /* 極簡報紙風格 CSS */
                body {{
                    font-family: 'Georgia', 'Times New Roman', serif;
                    line-height: 1.65;
                    color: #333333;
                    background-color: #ffffff;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 660px; /* 限制寬度提升閱讀專注力 */
                    margin: 0 auto;
                    padding: 40px 20px;
                }}
                .label {{
                    text-align: right;
                    font-size: 0.7rem;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
                    font-weight: 700;
                    color: #aaa;
                    text-transform: uppercase;
                    letter-spacing: 0.1em;
                    border-bottom: 1px solid #eee;
                    margin-bottom: 30px;
                }}
                h1 {{
                    font-size: 1.8rem;
                    color: #000;
                    font-weight: normal;
                    line-height: 1.2;
                    margin: 20px 0;
                }}
                h2 {{
                    font-size: 0.85rem;
                    font-family: sans-serif;
                    text-transform: uppercase;
                    color: #666;
                    letter-spacing: 0.05em;
                    margin-top: 40px;
                    border-bottom: 1px solid #f0f0f0;
                }}
                .article {{
                    font-size: 1.08rem; /* 標準報紙數位版大小 */
                    text-align: justify; /* 左右對齊 */
                    color: #222;
                }}
                br {{
                    content: "";
                    display: block;
                    margin: 1.4em 0; /* 增加段落間距 */
                }}
                footer {{
                    text-align: center;
                    color: #ccc;
                    font-size: 0.7rem;
                    margin-top: 60px;
                    font-family: sans-serif;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="label">Target: FLPT 240+ | C1 Advanced</div>
                <div class="article">
                    {article}
                </div>
                <footer>
                    &copy; 2026 FLPT Academic Study | NYT Inspired Layout
                </footer>
            </div>
        </body>
        </html>
        """
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_template.format(article=display_content))
            
        print("Success: Updated with Minimalist Newspaper Style.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
