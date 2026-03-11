import feedparser
import google.generativeai as genai
import os
import datetime

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        target_model = models[0] if models else 'gemini-1.5-flash'
    except:
        target_model = 'gemini-1.5-flash'

    model = genai.GenerativeModel(target_model)
    
    # 增加多樣化的來源，避免內容重複
    feeds = [
        "https://www.economist.com/international/rss.xml",
        "https://foreignpolicy.com/feed/",
        "https://api.quantamagazine.org/feed/",
        "https://www.nytimes.com/services/xml/rss/nyt/World.xml"
    ]
    
    news_text = ""
    for url in feeds:
        try:
            f = feedparser.parse(url)
            for entry in f.entries[:2]:
                news_text += f"Topic: {entry.title}\nSummary: {entry.summary}\n\n"
        except: continue

    # 加入當前時間戳記，強制 AI 產生不重複的內容
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    prompt = f"""
    Target: FLPT Level C1+ (Score 240+).
    Timestamp: {current_time}
    Input Materials: {news_text}
    
    Instructions:
    1. Write a UNIQUE 500-word academic analysis in English. 
    2. Start with a compelling Title (Level 1 Heading).
    3. Use varied C1 sentence structures. Ensure this version is distinct from previous interpretations.
    4. Provide Chinese analysis, 8 vocabularies, and 2 inference questions at the end.
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        with open("Daily_Study.md", "w", encoding="utf-8") as f:
            f.write(content)
            
        # 修正標題與內容的轉換邏輯
        processed_content = content.replace('# ', '<h1>').replace('## ', '<h2>').replace('\n', '<br>')
        
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
                    color: #333;
                    background-color: #fff;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 650px;
                    margin: 0 auto;
                    padding: 40px 20px;
                }}
                .label {{
                    text-align: right;
                    font-size: 0.7rem;
                    font-family: sans-serif;
                    font-weight: bold;
                    color: #bbb;
                    text-transform: uppercase;
                    border-bottom: 1px solid #eee;
                    margin-bottom: 20px;
                }}
                h1 {{
                    font-size: 1.8rem;
                    color: #000;
                    font-weight: normal;
                    line-height: 1.25;
                    margin: 30px 0;
                }}
                h2 {{
                    font-size: 0.9rem;
                    font-family: sans-serif;
                    text-transform: uppercase;
                    color: #777;
                    margin-top: 40px;
                    border-bottom: 1px solid #f5f5f5;
                }}
                .article {{
                    font-size: 1.05rem;
                    text-align: justify;
                }}
                br {{ margin: 1.2em 0; display: block; content: ""; }}
                footer {{
                    text-align: center;
                    color: #ddd;
                    font-size: 0.7rem;
                    margin-top: 60px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="label">FLPT 240+ | Refreshed at {current_time}</div>
                <div class="article">
                    {processed_content}
                </div>
                <footer>
                    Updated: {current_time}
                </footer>
            </div>
        </body>
        </html>
        """
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_template)
            
        print(f"Success: Content refreshed at {current_time}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
