from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from datetime import datetime
from forms import ContactForm
from werkzeug.utils import secure_filename
import os
from config import Config  # Add this line

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

# Portfolio data structure
portfolio_data = {
    'personal_info': {
        'name': 'Ronald II G. Sayago',
        'title': 'Odoo Developer',
        'about_short': 'Odoo developer with 2+ years of experience',
        'about_long': '''
        Detail-oriented  odoo developer/Technical Consultant with expertise in Python, Postgresql and Odoo Framework.
        ''',
        'location': 'Mandaluyong City, Philippines',
        'education': [
            {
                'degree': 'Electronics Engineering Technology',
                'school': 'Technological University of the Philippines - Cavite',
                'year': '2014-2017',
                'description': 'Focus on Electronics'
            },
            {
                'degree': 'Bachelor of Science in Electronics Engineering',
                'school': 'Technological University of the Philippines - Manila',
                'year': '2017-2020',
                'description': 'Focus on Information Technology'
            }
        ],
        'experience': [
            {
                'title': 'Technical Consultant',
                'company': 'Toolit INC.',
                'period': 'August 2022 - May 2024',
                'description': [
                    'Develop Custom Features for erp systems in Odoo',
                    'Handle client support',
                ]
            },
            {
                'title': 'Assistant Technical Lead',
                'company': 'Toolkit Inc.',
                'period': 'May 2024 - Present',
                'description': [
                    'Develop Custom Features for erp systems in Odoo',
                    'Handle client support',
                    'Handle the maintenance and updates on the clients cloud servers',
                    'Helps in mentoring junior developers'
                ]
            }
        ]
    },
    'skills': {
        'programming': ['Python', 'JavaScript', 'C#', 'C++','matlab'],
        'web_technologies': ['HTML5', 'CSS3', 'React', 'Flask'],
        'databases': ['PostgreSQL'],
        'tools': ['Git', 'Docker', 'Kubernetes'],
        'soft_skills': ['Problem Solving', 'Communication']
    },
    'projects': [
        {
            'name': 'Gift Registry Feature',
            'category': 'Odoo Development',
            'description': 'A comprehensive gift registry system built as an Odoo module, allowing users to create and manage gift registries for various occasions.',
            'long_description': '''
            Developed and implemented a full-featured gift registry system in Odoo that enables:
            - Users to create personalized gift registries for weddings, birthdays, and other special occasions
            - Public access to view and purchase items from registries
            - Real-time inventory tracking and order management
            - Seamless integration with existing Odoo e-commerce features
            ''',
            'technologies': ['Python', 'Odoo', 'PostgreSQL', 'XML', 'JavaScript'],
            'live_link': 'http://45.118.132.225:18691/gift_registry_list_public',
            'image': 'gift_registry.jpg' 
        }
    ],
    'blog_posts': [
  
    ],
    'contact': {
        'email': 'ronaldsayago2@gmail.com',
        'phone': '09278159941',
        'linkedin': 'https://linkedin.com/in/ronaldsayago2',
        'github': 'https://github.com/ronaldsayago2',
        'facebook': 'https://fb.com/ronaldsayago2'
    }
}

@app.route('/')
def home():
    return render_template('index.html', 
                         data=portfolio_data,
                         year=datetime.now().year)

@app.route('/about')
def about():
    return render_template('about.html',
                         data=portfolio_data,
                         year=datetime.now().year)

@app.route('/projects')
def projects():
    category = request.args.get('category', default=None)
    if category:
        filtered_projects = [p for p in portfolio_data['projects'] 
                           if p['category'] == category]
    else:
        filtered_projects = portfolio_data['projects']
    
    return render_template('projects.html',
                         projects=filtered_projects,
                         data=portfolio_data,
                         year=datetime.now().year)

@app.route('/project/<project_name>')
def project_detail(project_name):
    project = next((p for p in portfolio_data['projects'] 
                   if p['name'].lower().replace(' ', '-') == project_name), None)
    if project:
        return render_template('project_detail.html',
                             project=project,
                             data=portfolio_data,
                             year=datetime.now().year)
    return redirect(url_for('projects'))

@app.route('/blog')
def blog():
    return render_template('blog.html',
                         posts=portfolio_data['blog_posts'],
                         data=portfolio_data,
                         year=datetime.now().year)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            msg = Message(
                subject=f"Portfolio Contact: {form.subject.data}",
                sender=app.config['MAIL_USERNAME'],
                recipients=[portfolio_data['contact']['email']],
                body=f"""
                From: {form.name.data} <{form.email.data}>
                
                {form.message.data}
                """
            )
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('contact'))
        except Exception as e:
            flash('An error occurred while sending your message. Please try again.', 'error')
    
    return render_template('contact.html',
                         form=form,
                         data=portfolio_data,
                         year=datetime.now().year)


    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

