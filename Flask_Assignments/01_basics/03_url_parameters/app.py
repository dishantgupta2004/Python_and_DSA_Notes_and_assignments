# app.py
from flask import Flask, render_template, request, abort
from datetime import datetime
import hashlib

app = Flask(__name__)

# Sample data - in a real app, this would come from a database
videos = [
    {
        'id': 'QHx39RzA7B0',
        'title': 'Quantum Computing Explained',
        'description': 'An introduction to the principles of quantum computing and its potential applications.',
        'author': 'PhysicsExplained',
        'views': 256789,
        'uploaded': '2024-12-15',
        'tags': ['quantum', 'computing', 'technology', 'science']
    },
    {
        'id': 'Z9JQ1nXpB_g',
        'title': 'The Future of AI in Physics Research',
        'description': 'How artificial intelligence is revolutionizing physics research and accelerating discoveries.',
        'author': 'AIScience',
        'views': 182456,
        'uploaded': '2025-01-20',
        'tags': ['ai', 'physics', 'research', 'science']
    },
    {
        'id': 'X3gT67VnZ_Y',
        'title': 'Dark Matter: The Invisible Universe',
        'description': 'Exploring the mysteries of dark matter and its role in the cosmos.',
        'author': 'CosmosExplorer',
        'views': 325147,
        'uploaded': '2025-02-05',
        'tags': ['astronomy', 'dark matter', 'astrophysics', 'cosmology']
    }
]

articles = [
    {
        'id': 'breakthrough-quantum-teleportation',
        'title': 'Breakthrough in Quantum Teleportation Achieved',
        'summary': 'Scientists have successfully teleported quantum information over a record distance of 100 kilometers.',
        'content': 'In a groundbreaking experiment, researchers at the Quantum Physics Institute have achieved quantum teleportation over a distance of 100 kilometers using a new entanglement technique. This achievement marks a significant step toward quantum networks and could revolutionize secure communications. The team, led by Dr. Emma Richardson, used a novel approach involving trapped ions and superconducting qubits to maintain coherence over such distances. "This is a major milestone in quantum information science," said Dr. Richardson. The implications for quantum computing and secure communications are profound, potentially enabling quantum networks spanning continents.',
        'author': 'Samantha Chen',
        'published': '2025-03-15',
        'category': 'science'
    },
    {
        'id': 'higgs-boson-new-property',
        'title': 'New Property of Higgs Boson Discovered',
        'summary': 'Physicists at CERN have observed a previously unknown property of the Higgs boson that could reshape our understanding of particle physics.',
        'content': 'In a series of experiments at the Large Hadron Collider (LHC), physicists have discovered a new property of the Higgs boson that was not predicted by the Standard Model. The Higgs boson, famously discovered in 2012, appears to interact with dark matter particles under specific conditions, suggesting a potential bridge between ordinary matter and the mysterious dark matter that makes up approximately 27% of the universe. "This could be the connection we\'ve been searching for," said Dr. Marcus Wei, lead researcher on the project. "If confirmed, this discovery would necessitate revisions to the Standard Model and could provide a pathway to understanding dark matter." Additional experiments are planned to verify these findings.',
        'author': 'Robert Johnson',
        'published': '2025-02-28',
        'category': 'science'
    },
    {
        'id': 'fusion-breakthrough',
        'title': 'Commercial Fusion Energy Now Within Reach',
        'summary': 'A startup company claims to have achieved energy-positive fusion reaction sustainable for over an hour.',
        'content': 'FusionFuture, a startup backed by several major tech investors, announced yesterday that they have achieved a sustained fusion reaction that produced more energy than it consumed for over 60 minutes. This breakthrough, if independently verified, would represent a quantum leap forward in the development of practical fusion energy. The company used a novel approach combining magnetic confinement with inertial techniques. "We\'ve been pursuing this hybrid approach for five years, and the results have exceeded our expectations," said CEO Dr. Sophia Rodriguez. The company plans to build a demonstration power plant within three years and claims their technology could be commercially viable by 2030. Energy experts remain cautiously optimistic but emphasize the need for peer review and independent verification of these extraordinary claims.',
        'author': 'Michael Chang',
        'published': '2025-04-01',
        'category': 'technology'
    }
]

user_profiles = [
    {
        'username': 'quantum_enthusiast',
        'name': 'Alex Johnson',
        'bio': 'Physics PhD student interested in quantum computing and cosmology',
        'joined': '2023-06-15',
        'followers': 1284
    },
    {
        'username': 'science_writer',
        'name': 'Maya Patel',
        'bio': 'Science journalist covering the latest breakthroughs in physics and astronomy',
        'joined': '2022-08-10',
        'followers': 5629
    },
    {
        'username': 'tech_innovator',
        'name': 'Carlos Rodriguez',
        'bio': 'AI researcher and quantum computing enthusiast',
        'joined': '2024-01-22',
        'followers': 894
    }
]

# Routes
@app.route('/')
def home():
    return render_template('home.html', videos=videos, articles=articles)

@app.route('/video/<video_id>')
def video_detail(video_id):
    video = next((v for v in videos if v['id'] == video_id), None)
    if video:
        # Get recommended videos (excluding the current one)
        recommended = [v for v in videos if v['id'] != video_id]
        return render_template('video.html', video=video, recommended=recommended)
    else:
        abort(404)

@app.route('/article/<article_id>')
def article_detail(article_id):
    article = next((a for a in articles if a['id'] == article_id), None)
    if article:
        # Get related articles (excluding the current one)
        related = [a for a in articles if a['id'] != article_id]
        return render_template('article.html', article=article, related=related)
    else:
        abort(404)

@app.route('/user/<username>')
def user_profile(username):
    user = next((u for u in user_profiles if u['username'] == username), None)
    if user:
        # Get user's content (for demo, just assign random videos/articles)
        user_videos = videos[:2] if username == 'quantum_enthusiast' else videos[1:]
        user_articles = articles[:1] if username == 'science_writer' else articles[1:2]
        return render_template('user.html', user=user, videos=user_videos, articles=user_articles)
    else:
        abort(404)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return render_template('search.html', results=[], query='')
    
    # Simple search implementation
    video_results = [v for v in videos if query.lower() in v['title'].lower() or 
                    query.lower() in v['description'].lower() or
                    any(query.lower() in tag.lower() for tag in v['tags'])]
    
    article_results = [a for a in articles if query.lower() in a['title'].lower() or
                      query.lower() in a['summary'].lower() or
                      query.lower() in a['content'].lower()]
    
    all_results = {'videos': video_results, 'articles': article_results}
    return render_template('search.html', results=all_results, query=query)

@app.route('/category/<category>')
def category(category):
    category_articles = [a for a in articles if a['category'] == category]
    return render_template('category.html', category=category, articles=category_articles)

# Generate a short URL from a longer ID
def generate_short_url(id_string):
    hash_object = hashlib.md5(id_string.encode())
    return hash_object.hexdigest()[:8]

# Custom template filter
@app.template_filter('format_number')
def format_number(value):
    if value >= 1000000:
        return f"{value/1000000:.1f}M"
    elif value >= 1000:
        return f"{value/1000:.1f}K"
    else:
        return str(value)

@app.template_filter('time_ago')
def time_ago(date_str):
    date_format = "%Y-%m-%d"
    past_date = datetime.strptime(date_str, date_format)
    now = datetime.now()
    delta = now - past_date
    
    if delta.days == 0:
        return "Today"
    elif delta.days == 1:
        return "Yesterday"
    elif delta.days < 7:
        return f"{delta.days} days ago"
    elif delta.days < 30:
        weeks = delta.days // 7
        return f"{weeks} {'week' if weeks == 1 else 'weeks'} ago"
    elif delta.days < 365:
        months = delta.days // 30
        return f"{months} {'month' if months == 1 else 'months'} ago"
    else:
        years = delta.days // 365
        return f"{years} {'year' if years == 1 else 'years'} ago"

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)