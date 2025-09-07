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
    
    return render_template('budgets.html', budget_data=budget_data, categories=categories)

# API Routes
@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    
    expense = Expense(
        amount=float(data['amount']),
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
    
    return jsonify({'success': True, 'message': 'Expense added successfully'})

@app.route('/api/subscriptions', methods=['POST'])
def add_subscription():
    data = request.get_json()
    
    next_billing = datetime.strptime(data['next_billing'], '%Y-%m-%d').date()
    
    subscription = Subscription(
        name=data['name'],
        amount=float(data['amount']),
        billing_cycle=data['billing_cycle'],
        category_id=int(data['category_id']),
        next_billing=next_billing
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
        
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)