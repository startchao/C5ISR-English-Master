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
    topic_buckets = ["Strategic Geopolitics", "Economic Resilience", "Technological Ethics", "Social Justice"]
    selected_topic = random.choice(topic_buckets)

    # 調整 Prompt：強制要求解析部分中英夾雜，並嚴禁全大寫
    prompt = f"""
    Target: FLPT Level C1+ (Score 240+).
    Topic: {selected_topic}
    Instructions:
    1. Write a 500-word C1 academic essay (Standard casing). Start with '# TITLE'.
    2. Full Chinese Translation.
    3. ## Logic & Analysis: Use code-switching (Traditional Chinese + English key terms). Explain arguments clearly.
    4. ## Power Vocabulary: Word + IPA + Definition + Chinese + Example. (Standard Case)
    5. ## FLPT Quiz: 2 inference questions. Explanations must be bilingual (中英對照).
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        # 標題轉換與換行處理
        processed_content = content.replace('# ', '<h1>', 1).replace('## ', '<h2>').replace('\n', '<br>')
        
        # 增加隨機數防快取
        cache_buster = random.randint(1, 100000)

        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>C1 Study - {current_time}</title>
            <style>
                body {{ font-family: 'Georgia', serif; line-height: 1.6; color: #222; background-color: #fff; margin: 0; padding: 0; }}
                .container {{ max-width: 620px; margin: 0 auto; padding: 35px 20px; }}
                .header-meta {{ font-family: sans-serif; font-size: 0.65rem; color: #999; text-transform: uppercase; letter-spacing: 1.5px; border-bottom: 1px solid #eee; margin-bottom: 20px; display: flex; justify-content: space-between; }}
                h1 {{ font-size: 1.6rem; color: #000; font-weight: normal; margin-bottom: 25px; }}
                h2 {{ font-size: 0.95rem; font-family: sans-serif; color: #003366; margin-top: 45px; border-bottom: 1px solid #f0f0f0; padding-bottom: 5px; }}
                .article-body {{ font-size: 0.98rem; text-align: left; color: #333; }}
                .vocab-focus {{ font-size: 1.15rem; }}
                /* 強調中英夾雜的視覺層次 */
                h2 ~ div {{ font-size: 1.1rem; }}
                br {{ content: ""; display: block; margin: 1.2em 0; }}
                .action-btn {{ background: #f8f8f8; border: 1px solid #ddd; padding: 6px 12px; font-size: 0.75rem; border-radius: 4px; cursor: pointer; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <div class="container" id="cb-{cache_buster}">
                <div class="header-meta">
                    <span>Target: 240+ | Theme: {selected_topic}</span>
                    <span>{current_time}</span>
                </div>
                <button class="action-btn" onclick="location.reload(true)">🔄 Force Refresh</button>
                <div class="article-body" id="study-content">
                    {processed_content}
                </div>
                <script>
                    function copyContent() {{
                        const text = document.getElementById('study-content').innerText;
                        navigator.clipboard.writeText(text).then(() => alert('Copied!'));
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
