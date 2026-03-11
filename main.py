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
        "https://www.nytimes.com/services/xml/rss/nyt/World.xml"
    ]
    
    news_text = ""
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for entry in f.entries[:2]:
                news_text += f"Topic: {entry.title}\nDetail: {entry.summary}\n\n"
        except: continue

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    topic_buckets = ["Global Economy", "Geopolitics", "Tech & Cyber", "Social Justice", "Climate Policy"]
    selected_topic = random.choice(topic_buckets)

    prompt = f"""
    Target: FLPT Level C1+ (Score 240+).
    Theme: {selected_topic}
    Timestamp: {current_time}
    Materials: {news_text}
    
    Please structure your response precisely in this order:

    1. # [English Essay Title]
       (Write a 500-word cohesive C1 academic essay in English. No bullet points in this section.)

    2. ## [Full Chinese Translation - 全文中文翻譯]
       (Provide a complete and faithful Traditional Chinese translation of the essay above.)

    3. ## [Logic & Arguments - 邏輯解析]
       (Brief Traditional Chinese analysis of the essay structure.)

    4. ## [Power Vocabulary - 核心單字]
       (8 words with IPA, definitions, Chinese, and examples.)

    5. ## [FLPT Quiz - 模擬測驗]
       (2 inference questions in English + Chinese explanations.)
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        # 精確標籤轉換邏輯
        processed_content = content.replace('# ', '<h1>', 1).replace('## ', '<h2>').replace('\n', '<br>')
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>C1 Advanced Immersion</title>
            <style>
                body {{
                    font-family: 'Georgia', serif;
                    line-height: 1.55;
                    color: #222;
                    background-color: #fff;
                    margin: 0; padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 30px 20px;
                }}
                .header-meta {{
                    font-family: sans-serif;
                    font-size: 0.65rem;
                    color: #999;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                    border-bottom: 1px solid #eee;
                    margin-bottom: 15px;
                    display: flex;
                    justify-content: space-between;
                }}
                h1 {{
                    font-size: 1.5rem; /* 大幅縮小標題 */
                    color: #000;
                    font-weight: normal;
                    line-height: 1.2;
                    margin-bottom: 20px;
                }}
                h2 {{
                    font-size: 0.85rem;
                    font-family: sans-serif;
                    text-transform: uppercase;
                    color: #003366;
                    margin-top: 30px;
                    margin-bottom: 10px;
                    border-bottom: 1px solid #f0f0f0;
                }}
                /* 英文全文與中文翻譯使用較小字體 */
                .content {{
                    font-size: 0.95rem; 
                    text-align: left;
                    color: #333;
                }}
                /* 單字解析部分使用較大字體 */
                h2:nth-of-type(3) ~ br, h2:nth-of-type(3) ~ .content, 
                h2:contains("Power Vocabulary") ~ br {{
                    font-size: 1.1rem;
                }}
                /* 針對單字部分的特殊 CSS */
                .vocab-section {{
                    font-size: 1.1rem;
                    background-color: #f9f9f9;
                    padding: 10px;
                    border-radius: 4px;
                }}
                br {{ content: ""; display: block; margin: 1.1em 0; }}
                .action-btn {{
                    background: #eee; border: none; padding: 5px 10px;
                    font-size: 0.7rem; border-radius: 3px; cursor: pointer;
                    margin-bottom: 15px; font-family: sans-serif;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header-meta">
                    <span>FLPT 240+ | Theme: {selected_topic}</span>
                    <span>{current_time}</span>
                </div>
                <button class="action-btn" onclick="copyContent()">📋 Copy for Review</button>
                <div class="content" id="study-content">
                    {processed_content}
                </div>
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
