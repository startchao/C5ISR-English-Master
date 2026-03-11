import feedparser
import google.generativeai as genai
import os
import datetime
import random

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = models[0] if models else 'gemini-1.5-flash'
    except:
        target_model = 'gemini-1.5-flash'

    model = genai.GenerativeModel(target_model)
    
    feeds = [
        "https://www.economist.com/international/rss.xml",
        "https://foreignpolicy.com/feed/",
        "https://www.nytimes.com/services/xml/rss/nyt/World.xml",
        "https://www.theguardian.com/world/rss"
    ]
    
    news_text = ""
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for entry in f.entries[:2]:
                news_text += f"Topic: {entry.title}\nDetail: {entry.summary}\n\n"
        except: continue

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    topic_buckets = [
        "International Relations & Diplomacy", 
        "Global Economic Trends", 
        "Technology & Cyber Security", 
        "Social Justice & Human Rights", 
        "Environmental Policy & Energy"
    ]
    selected_topic = random.choice(topic_buckets)

    # 調整 Prompt：特別強調禁止使用全大寫
    prompt = f"""
    Target: FLPT Level C1+ (Score 240+).
    Theme: {selected_topic}
    Timestamp: {current_time}
    Materials: {news_text}
    
    Instructions:
    1. Use Standard Case (Sentence case) for all headings and content. DO NOT use all caps.
    2. Write a 500-word cohesive C1 academic essay in English. Start with a Title using '# '.
    3. Provide a full Traditional Chinese translation immediately after the essay.
    4. Provide the following sections using '## ' headings:
       - Logic & Arguments (Traditional Chinese analysis)
       - Power Vocabulary (8 words with IPA, definitions, Chinese, and examples. Use standard casing for words.)
       - FLPT Reading Quiz (2 inference questions in English + Chinese explanations. Use standard casing for options.)
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        # 精確標籤與排版轉換
        processed_content = content.replace('# ', '<h1>', 1).replace('## ', '<h2>').replace('\n', '<br>')
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>C1 Advanced Study - {current_time}</title>
            <style>
                body {{
                    font-family: 'Georgia', serif;
                    line-height: 1.6;
                    color: #222;
                    background-color: #fff;
                    margin: 0; padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 35px 20px;
                }}
                .header-meta {{
                    font-family: sans-serif;
                    font-size: 0.65rem;
                    color: #999;
                    text-transform: uppercase;
                    letter-spacing: 1.5px;
                    border-bottom: 1px solid #eee;
                    margin-bottom: 20px;
                    display: flex;
                    justify-content: space-between;
                }}
                h1 {{
                    font-size: 1.6rem;
                    color: #000;
                    font-weight: normal;
                    line-height: 1.25;
                    margin-bottom: 25px;
                }}
                h2 {{
                    font-size: 0.95rem;
                    font-family: sans-serif;
                    color: #003366;
                    margin-top: 45px;
                    margin-bottom: 15px;
                    border-bottom: 1px solid #f0f0f0;
                    padding-bottom: 5px;
                }}
                /* 英文全文與中文翻譯：精緻小字 */
                .article-body {{
                    font-size: 0.98rem;
                    text-align: left;
                    color: #333;
                }}
                /* 單字區與測驗區：放大字體，方便複習 */
                h2:nth-of-type(3) ~ br, h2:nth-of-type(3) ~ div,
                h2:nth-of-type(4) ~ br, h2:nth-of-type(4) ~ div,
                .vocab-focus {{
                    font-size: 1.15rem;
                }}
                br {{ content: ""; display: block; margin: 1.2em 0; }}
                .action-btn {{
                    background: #f8f8f8; border: 1px solid #ddd; padding: 6px 12px;
                    font-size: 0.75rem; border-radius: 4px; cursor: pointer;
                    margin-bottom: 20px; font-family: sans-serif; color: #555;
                }}
                footer {{ text-align: center; color: #ccc; font-size: 0.7rem; margin-top: 80px; padding-bottom: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header-meta">
                    <span>Target: FLPT 240+ | Theme: {selected_topic}</span>
                    <span>{current_time}</span>
                </div>
                <button class="action-btn" onclick="copyContent()">📋 Copy Full Text</button>
                <div class="article-body" id="study-content">
                    {processed_content}
                </div>
                <footer>
                    NYT Styled Academic Study | Standard Case Refreshed
                </footer>
                <script>
                    function copyContent() {{
                        const text = document.getElementById('study-content').innerText;
                        navigator.clipboard.writeText(text).then(() => {{
                            alert('Copied to clipboard!');
                        }});
                    }}
                </script>
            </div>
        </body>
        </html>
        """
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_template)
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(content)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
