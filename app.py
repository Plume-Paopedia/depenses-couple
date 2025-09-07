from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone, date
import calendar
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    color = db.Column(db.String(7), default='#007bff')  # Hex color
    icon = db.Column(db.String(50), default='fas fa-tags')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    is_exceptional = db.Column(db.Boolean, default=False)
    person = db.Column(db.String(100), default='Non spécifié')  # Who spent the money
    needs_reimbursement = db.Column(db.Boolean, default=False)  # If expense needs reimbursement
    notes = db.Column(db.String(500))  # Additional notes/options
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    category = db.relationship('Category', backref=db.backref('expenses', lazy=True))

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    billing_cycle = db.Column(db.String(20), default='monthly')  # monthly, yearly
    next_billing = db.Column(db.Date, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    person = db.Column(db.String(100), default='Non spécifié')  # Who pays for the subscription
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    category = db.relationship('Category', backref=db.backref('subscriptions', lazy=True))

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    monthly_limit = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    category = db.relationship('Category', backref=db.backref('budget', uselist=False))

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    is_recurring = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class ExpenseValidation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    requested_by = db.Column(db.String(100), nullable=False)
    reviewed_by = db.Column(db.String(100))
    comments = db.Column(db.String(500))
    threshold_amount = db.Column(db.Float, default=200.0)  # Amount that triggers validation
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    reviewed_at = db.Column(db.DateTime)
    
    expense = db.relationship('Expense', backref=db.backref('validation', uselist=False))

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    target_amount = db.Column(db.Float, nullable=False)
    target_type = db.Column(db.String(20), default='reduce')  # reduce, stay_under
    month = db.Column(db.Integer, nullable=False)  # 1-12
    year = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    category = db.relationship('Category', backref=db.backref('challenges', lazy=True))

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    icon = db.Column(db.String(50), default='fas fa-trophy')
    criteria_type = db.Column(db.String(50), nullable=False)  # expense_count, budget_respect, etc.
    criteria_value = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    earned_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    badge = db.relationship('Badge', backref=db.backref('user_badges', lazy=True))

class CalendarEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500))
    date = db.Column(db.Date, nullable=False)
    estimated_budget = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    is_vacation_mode = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    category = db.relationship('Category', backref=db.backref('events', lazy=True))

class NotificationSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=True)
    expense_threshold = db.Column(db.Float, default=100.0)
    budget_alert_percentage = db.Column(db.Float, default=80.0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

# Routes
@app.route('/')
def dashboard():
    # Get current month data
    today = datetime.now().date()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    # Calculate totals
    monthly_income = db.session.query(db.func.sum(Income.amount)).filter(
        Income.date >= start_of_month,
        Income.date <= end_of_month
    ).scalar() or 0
    
    monthly_expenses = db.session.query(db.func.sum(Expense.amount)).filter(
        Expense.date >= start_of_month,
        Expense.date <= end_of_month
    ).scalar() or 0
    
    monthly_subscriptions = db.session.query(db.func.sum(Subscription.amount)).filter(
        Subscription.is_active == True,
        Subscription.billing_cycle == 'monthly'
    ).scalar() or 0
    
    yearly_subscriptions = db.session.query(db.func.sum(Subscription.amount)).filter(
        Subscription.is_active == True,
        Subscription.billing_cycle == 'yearly'
    ).scalar() or 0
    
    monthly_subscriptions += (yearly_subscriptions or 0) / 12
    
    remaining_budget = monthly_income - monthly_expenses - monthly_subscriptions
    
    # Get recent expenses
    recent_expenses = Expense.query.order_by(Expense.created_at.desc()).limit(5).all()
    
    # Get upcoming subscriptions
    upcoming_subs = Subscription.query.filter(
        Subscription.is_active == True,
        Subscription.next_billing <= today + timedelta(days=7)
    ).order_by(Subscription.next_billing).all()
    
    return render_template('dashboard.html', 
                         monthly_income=monthly_income,
                         monthly_expenses=monthly_expenses,
                         monthly_subscriptions=monthly_subscriptions,
                         remaining_budget=remaining_budget,
                         recent_expenses=recent_expenses,
                         upcoming_subs=upcoming_subs,
                         date=date)

@app.route('/expenses')
def expenses():
    page = request.args.get('page', 1, type=int)
    category_filter = request.args.get('category', '')
    
    query = Expense.query
    if category_filter:
        query = query.filter(Expense.category_id == category_filter)
    
    expenses = query.order_by(Expense.date.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    categories = Category.query.all()
    return render_template('expenses.html', expenses=expenses, categories=categories)

@app.route('/subscriptions')
def subscriptions():
    active_subs = Subscription.query.filter_by(is_active=True).order_by(Subscription.next_billing).all()
    categories = Category.query.all()
    return render_template('subscriptions.html', subscriptions=active_subs, categories=categories, date=date)

@app.route('/budgets')
def budgets():
    budgets = Budget.query.join(Category).all()
    categories = Category.query.all()
    
    # Calculate current month spending per category
    today = datetime.now().date()
    start_of_month = today.replace(day=1)
    
    budget_data = []
    for budget in budgets:
        spent = db.session.query(db.func.sum(Expense.amount)).filter(
            Expense.category_id == budget.category_id,
            Expense.date >= start_of_month
        ).scalar() or 0
        
        budget_data.append({
            'budget': budget,
            'spent': spent,
            'percentage': (spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0
        })
    
    return render_template('budgets.html', budget_data=budget_data, categories=categories, today=today)

# API Routes
@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category_id = request.args.get('category_id', type=int)
    person = request.args.get('person')
    
    query = Expense.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    if person:
        query = query.filter_by(person=person)
    
    expenses = query.order_by(Expense.date.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'expenses': [{
            'id': expense.id,
            'amount': expense.amount,
            'description': expense.description,
            'date': expense.date.isoformat(),
            'category': expense.category.name,
            'person': expense.person,
            'notes': expense.notes,
            'is_exceptional': expense.is_exceptional,
            'needs_reimbursement': expense.needs_reimbursement
        } for expense in expenses.items],
        'total': expenses.total,
        'pages': expenses.pages,
        'current_page': page
    })

@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    
    # Check if expense requires validation
    amount = float(data['amount'])
    requires_validation = amount > 200.0  # Default threshold
    
    expense = Expense(
        amount=amount,
        description=data['description'],
        category_id=int(data['category_id']),
        is_exceptional=data.get('is_exceptional', False),
        date=datetime.strptime(data.get('date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date(),
        person=data.get('person', 'Non spécifié'),
        needs_reimbursement=data.get('needs_reimbursement', False),
        notes=data.get('notes', '')
    )
    
    db.session.add(expense)
    db.session.commit()
    
    # Create validation record if needed
    if requires_validation:
        validation = ExpenseValidation(
            expense_id=expense.id,
            requested_by=expense.person,
            status='pending'
        )
        db.session.add(validation)
        db.session.commit()
    
    # Check for budget alerts
    budget_alert = check_budget_alert(expense.category_id, amount)
    
    response_data = {
        'success': True, 
        'message': 'Expense added successfully',
        'expense_id': expense.id,
        'requires_validation': requires_validation
    }
    
    if budget_alert:
        response_data['budget_alert'] = budget_alert
    
    return jsonify(response_data)

@app.route('/api/expenses/<int:expense_id>/validate', methods=['POST'])
def validate_expense(expense_id):
    data = request.get_json()
    validation = ExpenseValidation.query.filter_by(expense_id=expense_id).first()
    
    if not validation:
        return jsonify({'success': False, 'message': 'Validation not found'}), 404
    
    validation.status = data.get('status', 'approved')
    validation.reviewed_by = data.get('reviewed_by', 'System')
    validation.comments = data.get('comments', '')
    validation.reviewed_at = datetime.now(timezone.utc)
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Expense validation updated'})

@app.route('/api/challenges', methods=['GET'])
def get_challenges():
    challenges = Challenge.query.filter_by(is_active=True).all()
    
    challenge_data = []
    for challenge in challenges:
        # Calculate progress
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        if challenge.month == current_month and challenge.year == current_year:
            start_of_month = datetime.now().replace(day=1).date()
            end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            spent = db.session.query(db.func.sum(Expense.amount)).filter(
                Expense.category_id == challenge.category_id,
                Expense.date >= start_of_month,
                Expense.date <= end_of_month
            ).scalar() or 0
            
            progress = (spent / challenge.target_amount * 100) if challenge.target_amount > 0 else 0
            
            challenge_data.append({
                'id': challenge.id,
                'name': challenge.name,
                'description': challenge.description,
                'target_amount': challenge.target_amount,
                'current_spent': spent,
                'progress': progress,
                'category': challenge.category.name if challenge.category else None
            })
    
    return jsonify({'challenges': challenge_data})

@app.route('/api/challenges', methods=['POST'])
def create_challenge():
    data = request.get_json()
    
    challenge = Challenge(
        name=data['name'],
        description=data['description'],
        category_id=data.get('category_id'),
        target_amount=float(data['target_amount']),
        target_type=data.get('target_type', 'reduce'),
        month=data.get('month', datetime.now().month),
        year=data.get('year', datetime.now().year)
    )
    
    db.session.add(challenge)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Challenge created successfully'})

@app.route('/api/badges', methods=['GET'])
def get_badges():
    user_name = request.args.get('user_name')
    
    if user_name:
        user_badges = UserBadge.query.filter_by(user_name=user_name).all()
        badges_data = [{
            'id': ub.badge.id,
            'name': ub.badge.name,
            'description': ub.badge.description,
            'icon': ub.badge.icon,
            'earned_at': ub.earned_at.isoformat()
        } for ub in user_badges]
    else:
        badges = Badge.query.all()
        badges_data = [{
            'id': badge.id,
            'name': badge.name,
            'description': badge.description,
            'icon': badge.icon,
            'criteria_type': badge.criteria_type,
            'criteria_value': badge.criteria_value
        } for badge in badges]
    
    return jsonify({'badges': badges_data})

@app.route('/api/calendar/events', methods=['GET'])
def get_calendar_events():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = CalendarEvent.query
    
    if start_date:
        query = query.filter(CalendarEvent.date >= datetime.strptime(start_date, '%Y-%m-%d').date())
    if end_date:
        query = query.filter(CalendarEvent.date <= datetime.strptime(end_date, '%Y-%m-%d').date())
    
    events = query.order_by(CalendarEvent.date).all()
    
    return jsonify({
        'events': [{
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.date.isoformat(),
            'estimated_budget': event.estimated_budget,
            'category': event.category.name if event.category else None,
            'is_vacation_mode': event.is_vacation_mode
        } for event in events]
    })

@app.route('/api/calendar/events', methods=['POST'])
def create_calendar_event():
    data = request.get_json()
    
    event = CalendarEvent(
        title=data['title'],
        description=data.get('description', ''),
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        estimated_budget=data.get('estimated_budget'),
        category_id=data.get('category_id'),
        is_vacation_mode=data.get('is_vacation_mode', False)
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Event created successfully'})

@app.route('/api/backup', methods=['POST'])
def create_backup():
    """Create a JSON backup of all data"""
    try:
        backup_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'version': '1.0',
            'categories': [{'id': c.id, 'name': c.name, 'color': c.color, 'icon': c.icon} for c in Category.query.all()],
            'expenses': [{
                'id': e.id, 'amount': e.amount, 'description': e.description,
                'date': e.date.isoformat(), 'category_id': e.category_id,
                'person': e.person, 'notes': e.notes, 'is_exceptional': e.is_exceptional,
                'needs_reimbursement': e.needs_reimbursement
            } for e in Expense.query.all()],
            'subscriptions': [{
                'id': s.id, 'name': s.name, 'amount': s.amount,
                'billing_cycle': s.billing_cycle, 'next_billing': s.next_billing.isoformat(),
                'category_id': s.category_id, 'person': s.person, 'is_active': s.is_active
            } for s in Subscription.query.all()],
            'budgets': [{
                'id': b.id, 'category_id': b.category_id, 'monthly_limit': b.monthly_limit
            } for b in Budget.query.all()],
            'income': [{
                'id': i.id, 'amount': i.amount, 'description': i.description,
                'date': i.date.isoformat(), 'is_recurring': i.is_recurring
            } for i in Income.query.all()]
        }
        
        return jsonify({
            'success': True,
            'backup_data': backup_data,
            'message': 'Backup created successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/qr-share/<int:expense_id>', methods=['GET'])
def generate_qr_share(expense_id):
    """Generate QR code data for sharing an expense"""
    expense = Expense.query.get_or_404(expense_id)
    
    share_data = {
        'type': 'expense',
        'amount': expense.amount,
        'description': expense.description,
        'category_id': expense.category_id,
        'person': expense.person,
        'notes': expense.notes,
        'date': expense.date.isoformat()
    }
    
    return jsonify({
        'success': True,
        'share_data': share_data,
        'qr_text': json.dumps(share_data)
    })

def check_budget_alert(category_id, amount):
    """Check if expense triggers budget alert"""
    budget = Budget.query.filter_by(category_id=category_id).first()
    if not budget:
        return None
    
    # Get current month spending
    today = datetime.now().date()
    start_of_month = today.replace(day=1)
    
    spent = db.session.query(db.func.sum(Expense.amount)).filter(
        Expense.category_id == category_id,
        Expense.date >= start_of_month
    ).scalar() or 0
    
    percentage_used = (spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0
    
    if percentage_used >= 90:
        return {
            'level': 'danger',
            'message': f'Budget dépassé ! {percentage_used:.1f}% utilisé',
            'spent': spent,
            'limit': budget.monthly_limit
        }
    elif percentage_used >= 80:
        return {
            'level': 'warning',
            'message': f'Attention : {percentage_used:.1f}% du budget utilisé',
            'spent': spent,
            'limit': budget.monthly_limit
        }
    
    return None

@app.route('/api/subscriptions', methods=['POST'])
def add_subscription():
    data = request.get_json()
    
    next_billing = datetime.strptime(data['next_billing'], '%Y-%m-%d').date()
    
    subscription = Subscription(
        name=data['name'],
        amount=float(data['amount']),
        billing_cycle=data['billing_cycle'],
        category_id=int(data['category_id']),
        next_billing=next_billing,
        person=data.get('person', 'Non spécifié')
    )
    
    db.session.add(subscription)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Subscription added successfully'})

@app.route('/api/budgets', methods=['POST'])
def add_budget():
    data = request.get_json()
    
    # Check if budget already exists for this category
    existing_budget = Budget.query.filter_by(category_id=int(data['category_id'])).first()
    if existing_budget:
        existing_budget.monthly_limit = float(data['monthly_limit'])
    else:
        budget = Budget(
            category_id=int(data['category_id']),
            monthly_limit=float(data['monthly_limit'])
        )
        db.session.add(budget)
    
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Budget updated successfully'})

@app.route('/api/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Expense deleted successfully'})

@app.route('/api/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    data = request.get_json()
    
    expense.amount = float(data['amount'])
    expense.description = data['description']
    expense.category_id = int(data['category_id'])
    expense.is_exceptional = data.get('is_exceptional', False)
    expense.date = datetime.strptime(data.get('date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date()
    expense.person = data.get('person', 'Non spécifié')
    expense.needs_reimbursement = data.get('needs_reimbursement', False)
    expense.notes = data.get('notes', '')
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Expense updated successfully'})

@app.route('/api/subscriptions/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    subscription = Subscription.query.get_or_404(subscription_id)
    db.session.delete(subscription)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Subscription deleted successfully'})

@app.route('/api/subscriptions/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    subscription = Subscription.query.get_or_404(subscription_id)
    data = request.get_json()
    
    subscription.name = data['name']
    subscription.amount = float(data['amount'])
    subscription.billing_cycle = data['billing_cycle']
    subscription.category_id = int(data['category_id'])
    subscription.next_billing = datetime.strptime(data['next_billing'], '%Y-%m-%d').date()
    subscription.person = data.get('person', 'Non spécifié')
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Subscription updated successfully'})

@app.route('/api/income', methods=['POST'])
def add_income():
    data = request.get_json()
    
    income = Income(
        amount=float(data['amount']),
        description=data['description'],
        date=datetime.strptime(data.get('date', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d').date(),
        is_recurring=data.get('is_recurring', False)
    )
    
    db.session.add(income)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Income added successfully'})

@app.route('/api/charts/expenses')
def chart_expenses():
    # Get last 6 months of data
    today = datetime.now().date()
    months_data = []
    
    for i in range(6):
        month_date = today.replace(day=1) - timedelta(days=i*30)
        start_of_month = month_date.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_expenses = db.session.query(db.func.sum(Expense.amount)).filter(
            Expense.date >= start_of_month,
            Expense.date <= end_of_month
        ).scalar() or 0
        
        months_data.append({
            'month': start_of_month.strftime('%B %Y'),
            'amount': month_expenses
        })
    
    months_data.reverse()
    return jsonify(months_data)

@app.route('/api/charts/categories')
def chart_categories():
    # Get current month spending by category
    today = datetime.now().date()
    start_of_month = today.replace(day=1)
    
    category_data = db.session.query(
        Category.name,
        Category.color,
        db.func.sum(Expense.amount).label('total')
    ).join(Expense).filter(
        Expense.date >= start_of_month
    ).group_by(Category.id).all()
    
    return jsonify([{
        'category': row.name,
        'amount': row.total,
        'color': row.color
    } for row in category_data])

def init_database():
    """Initialize the database with default data"""
    # Drop all tables and recreate them to ensure schema is up to date
    db.drop_all()
    db.create_all()
    
    # Add default categories if they don't exist
    if not Category.query.first():
        default_categories = [
            Category(name='Alimentation', color='#28a745', icon='fas fa-utensils'),
            Category(name='Transport', color='#007bff', icon='fas fa-car'),
            Category(name='Logement', color='#6f42c1', icon='fas fa-home'),
            Category(name='Divertissement', color='#e83e8c', icon='fas fa-gamepad'),
            Category(name='Santé', color='#dc3545', icon='fas fa-heartbeat'),
            Category(name='Vêtements', color='#fd7e14', icon='fas fa-tshirt'),
            Category(name='Éducation', color='#20c997', icon='fas fa-graduation-cap'),
            Category(name='Abonnements', color='#6610f2', icon='fas fa-sync-alt'),
            Category(name='Autres', color='#6c757d', icon='fas fa-ellipsis-h'),
        ]
        
        for category in default_categories:
            db.session.add(category)
        
        # Add default badges
        default_badges = [
            Badge(name='Premier Pas', description='Première dépense enregistrée', icon='fas fa-baby', criteria_type='expense_count', criteria_value=1),
            Badge(name='Habitué', description='10 dépenses enregistrées', icon='fas fa-star', criteria_type='expense_count', criteria_value=10),
            Badge(name='Expert', description='50 dépenses enregistrées', icon='fas fa-crown', criteria_type='expense_count', criteria_value=50),
            Badge(name='Maître Budget', description='Budget respecté 3 mois consécutifs', icon='fas fa-trophy', criteria_type='budget_respect', criteria_value=3),
            Badge(name='Économe', description='Réduction de 20% des dépenses sur un mois', icon='fas fa-piggy-bank', criteria_type='expense_reduction', criteria_value=20),
            Badge(name='Communicateur', description='50 commentaires ajoutés', icon='fas fa-comments', criteria_type='comment_count', criteria_value=50)
        ]
        
        for badge in default_badges:
            db.session.add(badge)
        
        db.session.commit()

@app.route('/manifest.json')
def serve_manifest():
    return app.send_static_file('manifest.json')

@app.route('/sw.js')
def serve_sw():
    return app.send_static_file('sw.js')

if __name__ == '__main__':
    with app.app_context():
        init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)