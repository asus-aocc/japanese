import anthropic
import json
import os
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
today = datetime.now(JST)
date_str = today.strftime("%Y年%-m月%-d日")
date_iso = today.strftime("%Y/%m/%d")

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def ask(prompt: str, max_tokens: int = 2000) -> dict:
    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    text = msg.content[0].text.strip()
    # Strip markdown fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0].strip()
    return json.loads(text)


# ── 1. ニュース・トレンド・会話ネタ・新用法 ──────────────────────────────────
print("Generating news / trends / chat / usage...")
main_prompt = f"""今日は{date_str}（日本時間）です。日本語学習者（台湾人・JLPT N3〜N2）向けに以下のコンテンツをJSON形式のみで返答してください。日本語テキストはすべて<ruby>漢字<rt>よみ</rt></ruby>形式でルビを付けること。マークダウン・コードブロック不要。

{{
  "news": [
    {{
      "category": "カテゴリ（例：経済・社会・テクノロジー・スポーツ・エンタメ）",
      "headline": "見出し(ruby付き)",
      "summary": "要約2〜3文(ruby付き)",
      "vocab": [{{"word": "語(ruby付き)", "meaning": "中国語訳"}}],
      "difficulty": "N3またはN2またはN1",
      "source": "想定ソース名",
      "published_at": "推定配信日時（例：{date_iso} 08:30）"
    }}
  ],
  "trends": [
    {{
      "platform": "X/Instagram/YouTube/TikTok",
      "topic": "トピック(ruby付き)",
      "description": "説明2文(ruby付き)",
      "hashtags": ["#例"],
      "reactions": "反応の傾向",
      "posted_at": "投稿日時（例：{date_iso} 10:00）"
    }}
  ],
  "chat": [
    {{
      "situation": "場面（例：居酒屋・職場・SNS）",
      "prompt": "会話フレーズ(ruby付き)",
      "tip": "コツ（中国語）",
      "example_reply": "自然な返答例(ruby付き)",
      "useful_phrases": ["使える表現(ruby付き)"]
    }}
  ],
  "usage": {{
    "expression": "今日覚えたい表現(ruby付き)",
    "meaning": "意味・使い方（中国語で説明）",
    "examples": [{{"ja": "例文(ruby付き)", "zh": "中国語訳"}}],
    "common_mistakes": [{{"wrong": "誤り(ruby付き)", "correct": "正解(ruby付き)", "reason": "理由（中国語）"}}],
    "nuance": "ニュアンス（中国語）",
    "related": ["関連表現(ruby付き)"]
  }}
}}

news4件・trends3件・chat3件・examples3件・common_mistakes2件。
今日の実際の季節感・時事（{date_str}）を反映し、なるべくリアルな最新トピックにすること。"""

main_data = ask(main_prompt, 2000)

# ── 2. エンタメ ──────────────────────────────────────────────────────────────
print("Generating entertainment...")
ent_prompt = f"""今日は{date_str}です。日本語学習者（台湾人・JLPT N3〜N2）向けに今月の日本エンタメ情報をJSON形式のみで返答してください。日本語テキストは<ruby>漢字<rt>よみ</rt></ruby>形式で。マークダウン不要。

{{
  "music": [
    {{
      "title": "曲名(ruby付き)",
      "artist": "アーティスト",
      "desc": "説明（中国語2文）",
      "genre": "ジャンル",
      "status": "🔥 人気急上昇 など",
      "date": "{date_iso}",
      "learn": "日本語学習ポイント(ruby付き)"
    }}
  ],
  "variety": [...同じ形式...],
  "drama":   [...同じ形式、titleはruby付き、artistの代わりにinfoフィールドに放送局・主演...],
  "movie":   [...同じ形式、infoに配給・公開情報...],
  "book":    [...同じ形式、artistの代わりにauthorフィールド...],
  "mag":     [...同じ形式、artistの代わりにpublisherフィールド...]
}}

music3件・variety2件・drama3件・movie2件・book3件・mag2件。
今月（{date_str}）の実際の話題作・ランキング情報を反映すること。"""

ent_data = ask(ent_prompt, 2000)

# ── 3. 組み合わせて保存 ───────────────────────────────────────────────────────
output = {
    "generated_at": today.strftime("%Y/%m/%d %H:%M JST"),
    "date_label": today.strftime("%Y年%-m月%-d日（%a）"),
    **main_data,
    "entertainment": ent_data,
}

out_path = os.path.join(os.path.dirname(__file__), "content.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Done! Saved to {out_path}")
print(f"  news:    {len(output.get('news', []))} items")
print(f"  trends:  {len(output.get('trends', []))} items")
print(f"  chat:    {len(output.get('chat', []))} items")
print(f"  ent cats: {list(output.get('entertainment', {}).keys())}")
