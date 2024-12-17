from flask import Flask, render_template, jsonify, request
import arxiv
import openai
import os
from dotenv import load_dotenv
from translations import translations

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

def get_language_from_request():
    lang = request.cookies.get('lang')
    if lang not in ['es', 'en']:
        lang = 'es'  # default language
    return lang

def translate_text(text, target_lang):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a translator. Translate the following text to {target_lang}."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

def translate_and_summarize(text, target_lang):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a scientific paper summarizer and translator. Summarize the following text in {target_lang} in a clear and concise way, highlighting the main contributions and findings."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content

@app.route('/')
def index():
    lang = get_language_from_request()
    return render_template('index.html', translations=translations[lang], lang=lang)

@app.route('/papers/')
def get_papers():
    category = request.args.get('category', 'cs.AI')
    max_results = int(request.args.get('max_results', 5))
    lang = get_language_from_request()
    target_lang = 'English' if lang == 'en' else 'Spanish'
    
    search = arxiv.Search(
        query=f"cat:{category}",
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    
    papers = []
    for result in search.results():
        # Translate title and summary if language is Spanish
        if lang == 'es':
            translated_title = translate_text(result.title, target_lang)
            translated_summary = translate_and_summarize(result.summary, target_lang)
        else:
            translated_title = result.title
            translated_summary = result.summary

        papers.append({
            'id': result.entry_id.split('/')[-1],
            'title': translated_title,
            'authors': [author.name for author in result.authors],
            'summary': translated_summary,
            'pdf_url': result.pdf_url,
            'original_title': result.title,
            'original_summary': result.summary
        })
    
    return jsonify(papers)

@app.route('/papers/<paper_id>/summary')
def get_paper_summary(paper_id):
    lang = get_language_from_request()
    target_lang = 'Spanish' if lang == 'es' else 'English'
    
    search = arxiv.Search(id_list=[paper_id])
    paper = next(search.results())
    
    if lang == 'es':
        translated_title = translate_text(paper.title, target_lang)
        translated_summary = translate_and_summarize(paper.summary, target_lang)
    else:
        translated_title = paper.title
        translated_summary = paper.summary
    
    return jsonify({
        'original_title': paper.title,
        'translated_title': translated_title,
        'original_summary': paper.summary,
        'translated_summary': translated_summary
    })

if __name__ == '__main__':
    app.run(debug=True)
