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
        'title': 'Assistant Technical Lead',
        'about_short': 'Odoo Developer with 2+ years of experience',
        'about_long': '''Dedicated and detail-oriented Technical Consultant with over two years of experience specializing in Odoo ERP systems. Skilled in designing and developing custom Odoo modules, particularly for purchase, sales, and inventory customizations, to meet diverse client business needs. Experienced in creating and customizing detailed PDF and Excel reports, managing cloud-deployed databases, and providing comprehensive post-deployment support. Strong expertise in Python, XML, JavaScript and PostgreSQL, enabling efficient customization and integration of ERP solutions.''',

        'location': 'Urban Pad, Kings road, Samat Street, Mandaluyong City, Philippines',
        
        
        
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
        'programming': ['Python', 'JavaScript', 'C#', 'C++', 'MATLAB','XML','Bash Script'],
        'web_technologies': ['HTML5', 'CSS', 'Flask', 'Flutter','AJAX', 'jQuery'],
        'databases': ['PostgreSQL'],
        'tools': ['Git', 'Github Desktop', 'PG Admin', 'Pentaho', 'Navicat'],
        'frameworks_and_libraries': [
            'Odoo Framework',
            'TensorFlow',
            'Keras',
            'OpenCV',
            'YOLO'
        ],
        'odoo_expertise': [
            'Custom Module Development',
            'PDF/Excel Report Creation',
            'Database Management',
            'Cloud Deployment',
            'Website Development',
        ],
        'soft_skills': [
            'Problem Solving',
            'Technical Leadership',
            'Client Support',
            'System Troubleshooting',
            'Team Mentoring'
        ]
    },
    
    
    
    'odoo_modules': [
        {
            'name': 'Sales Incentives Module',
            'clients': ['AVSC', 'IAJW'],
            'description': 'Automated sales incentive calculation and distribution system that tracks sales performance and computes commissions based on configurable rules.',
            'features': [
                'Dynamic incentive calculation based on sales metrics',
                'Customizable commission structures',
                'Auto generation and computation of vendor bills to agents',
                'Automated payment processing integration',
                'Detailed and customized reporting'
            ],
            'technologies': ['Python', 'Odoo', 'PostgreSQL', 'XML'],
            'status': 'Deployed and Active'
        },
        {
            'name': 'Request For Payment Module',
            'clients': ['Auro', 'Gruppo', 'Fortune Inc.','DLSU-D'],
            'description': 'Streamlined payment request management system that handles the entire workflow from request initiation to approval and processing.',
            'features': [
                'Multi-level and configurable approval workflow',
                'Budget tracking and validation',
                'Integration with accounting module',
                'Audit trail and history tracking'
            ],
            'technologies': ['Python', 'Odoo', 'PostgreSQL', 'XML'],
            'status': 'Deployed and Active'
        },
        
        
        
        {
            'name': 'Cash Advance Module',
            'clients': ['Auro', 'Gruppo', 'Fortune Inc.','Senco/Istudio Inc.'],
            'description': 'Cash Advance request management system for company employees.',
            'features': [
                'Multi-level approval workflow',
                'Document attachment support',
                'Auto Generation and Computation of Journal Entries',
                'Budget tracking and validation',
                'Integration with accounting module',
                'Audit trail and history tracking'
            ],
            'technologies': ['Python', 'Odoo', 'PostgreSQL', 'XML'],
            'status': 'Deployed and Active'
        },
        {
            'name': 'Purchase Requisition Module',
            'clients': ['Vistaland'],
            'description': 'Comprehensive purchase requisition system that manages procurement requests from initiation to fulfillment.',
            'features': [
                'Automated approval routing',
                'Inventory level integration',
                'Budget tracking and validation',
                'Vendor management',
                'Budget checking and validation',
                'Purchase order generation'
            ],
            'technologies': ['Python', 'Odoo', 'PostgreSQL', 'XML'],
            'status': 'Deployed and Active'
        },
        {
            'name': 'Project PRS Module',
            'clients': ['Vistaland'],
            'description': 'Project-specific purchase requisition system tailored for construction and development projects.',
            'features': [
                'Project-based budgeting',
                'Material requirement planning',
                'Cost center tracking',
                'Budget tracking and validation',
                'Project milestone integration',
            ],
            'technologies': ['Python', 'Odoo', 'PostgreSQL', 'XML'],
            'status': 'Deployed and Active'
        },
        {
            'name': 'Request To Transfer Module',
            'clients': ['Sevilla Inc.'],
            'description': 'Inventory transfer management system that handles internal stock movements and transfers between locations.',
            'features': [
                'Real-time inventory tracking',
                'Transfer approval workflow',
                'Location management',
                'Transfer history and tracking'
            ],
            'technologies': ['Python', 'Odoo', 'PostgreSQL', 'XML'],
            'status': 'Deployed and Active'
        },
        {
            'name': 'Request for Consumption Module',
            'clients': ['Sevilla Inc.'],
            'description': 'System for managing internal material consumption requests and tracking resource usage.',
            'features': [
                'Material consumption tracking',
                'Auto Generation of Stock Movement Transactions in the system',
                'Automated stock updates',
            ],
            'technologies': ['Python', 'Odoo', 'PostgreSQL', 'XML'],
            'status': 'Deployed and Active'
        },
        {
            'name': 'Trip Ticket Process Module',
            'clients': ['Ardent World Inc.'],
            'description': 'Comprehensive system for managing vehicle trips, logistics, and delivery scheduling.',
            'features': [
                'Driver assignment',
                'Delivery scheduling',
                'Customized Report for trip ticket'
            ],
            'technologies': ['Python', 'Odoo', 'PostgreSQL', 'XML'],
            'status': 'Deployed and Active'
        },
        {
            'name': 'Job Order Module',
            'clients': ['Ardent World'],
            'description': 'Complete job order management system for tracking and managing service requests and work orders.',
            'features': [
                'Job Order Requests for Manufacturing Subcontractors',
                'Automated Computation of prices base on configured vendors',
            ],
            'technologies': ['Python', 'Odoo', 'PostgreSQL', 'XML'],
            'status': 'Deployed and Active'
        },
        {
            'name': 'Biometrics Login Syncing',
            'clients': ['DLSZ'],
            'description': 'Integration system that synchronizes biometric data into odoo.',
            'features': [
                'Real-time biometric data synchronization from microsoft server db',
                'Secure authentication protocol',
                'User attendance tracking',
                'Configurable Syncing Parameters'
            ],
            'technologies': ['Python', 'Odoo', 'PostgreSQL', 'XML', 'Biometric API Integration'],
            'status': 'Deployed and Active'
        }
    ],
    
    
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

