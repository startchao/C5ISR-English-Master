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
    
    # 擴展新聞來源：涵蓋財經、科技、法律與地緣政治
    feeds = [
        "https://www.economist.com/international/rss.xml",
        "https://foreignpolicy.com/feed/",
        "https://www.nytimes.com/services/xml/rss/nyt/World.xml",
        "https://search.cnbc.com/rs/search/view.xml?partnerId=2000&keywords=global+economy",
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
    
    # 【核心更新】主題輪替機制：避免每天都太哲學
    topic_buckets = [
        "Global Economic Resilience & Financial Shifts",
        "Geopolitical Strategy & International Relations",
        "Emerging Technology, AI Ethics & Cybersecurity",
        "Rule of Law, Human Rights & Social Justice",
        "Climate Action, Energy Transition & Global Policy"
    ]
    selected_topic = random.choice(topic_buckets)

    prompt = f"""
    Target: FLPT Level C1+ (Score 240+).
    Primary Focus: {selected_topic}
    Timestamp: {current_time}
    Materials: {news_text}
    
    Instructions:
    1. Start with a bold headline using '# '.
    2. Write a 500-word academic analysis in the style of an 'Analytical News Feature'. 
    3. IMPORTANT: Avoid overly abstract or philosophical jargon. Focus on factual analysis, strategic trends, and real-world implications.
    4. Use C1 Advanced English (complex syntax, high-level collocations).
    5. After the essay, include:
       - '## Logic & Key Arguments' (Traditional Chinese)
       - '## Power Vocabulary' (8 words with IPA, definitions, Chinese, and examples)
       - '## FLPT Reading Quiz' (2 inference questions in English + Chinese explanations)
    """
    
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        # 標題與排版修正：確保大標題出現
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
                    font-family: 'Georgia', 'Times New Roman', serif;
                    line-height: 1.6;
                    color: #1a1a1a;
                    background-color: #ffffff;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 620px;
                    margin: 0 auto;
                    padding: 50px 20px;
                }}
                .header-meta {{
                    font-family: -apple-system, sans-serif;
                    font-size: 0.7rem;
                    font-weight: 700;
                    color: #999;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    border-bottom: 1px solid #f0f0f0;
                    margin-bottom: 30px;
                    display: flex;
                    justify-content: space-between;
                }}
                h1 {{
                    font-size: 2.1rem;
                    color: #000;
                    font-weight: normal;
                    line-height: 1.15;
                    margin-bottom: 35px;
                    text-align: left;
                }}
                h2 {{
                    font-size: 0.85rem;
                    font-family: -apple-system, sans-serif;
                    text-transform: uppercase;
                    color: #444;
                    margin-top: 45px;
                    margin-bottom: 15px;
                    border-bottom: 1px solid #f0f0f0;
                    letter-spacing: 0.05em;
                }}
                .content {{
                    font-size: 1.05rem;
                    text-align: left; /* 保持紐時的不規則右邊緣，更有呼吸感 */
                    color: #333;
                }}
                br {{ content: ""; display: block; margin: 1.3em 0; }}
                footer {{
                    text-align: center;
                    color: #ccc;
                    font-size: 0.7rem;
                    margin-top: 80px;
                    font-family: sans-serif;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header-meta">
                    <span>Target: 240+ | Theme: {selected_topic}</span>
                    <span>{current_time}</span>
                </div>
                <div class="content">
                    {processed_content}
                </div>
                <footer>
                    FLPT Professional Series | Topic-Rotated Content
                </footer>
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
