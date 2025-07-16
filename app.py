from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.secret_key = 'credit-card-mastery-secret-key'

# Simple file-based storage
DATA_FILE = 'cards_data.json'

def load_cards():
    """Load cards from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_cards(cards):
    """Save cards to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(cards, f, indent=2)

def calculate_dates(cycle_start, cycle_end):
    """Calculate all critical dates based on cycle dates"""
    # Parse dates
    start_date = datetime.strptime(cycle_start, '%Y-%m-%d')
    end_date = datetime.strptime(cycle_end, '%Y-%m-%d')
    
    # CRITICAL: The cycle_end date IS the closing date - this is when your statement closes
    # and your balance gets reported to credit bureaus
    closing_date = end_date  # This is your STATEMENT CLOSING DATE
    reporting_date = closing_date  # Same as closing date - when balance reports to credit bureaus
    
    # Current cycle calculations based on industry standards
    pay_by_date = closing_date - timedelta(days=3)  # 3 days before closing/reporting (strategic timing)
    can_use_funds = closing_date + timedelta(days=3)  # 3 days after closing/reporting (strategic timing)
    due_date = closing_date + timedelta(days=25)  # 25 days after closing date (industry standard)
    
    # Calculate next cycle dates (same cycle length)
    cycle_length = (end_date - start_date).days + 1
    next_cycle_start = closing_date + timedelta(days=1)
    next_cycle_end = next_cycle_start + timedelta(days=cycle_length - 1)
    
    # Next cycle closing and reporting dates
    next_closing_date = next_cycle_end
    next_reporting_date = next_closing_date
    next_pay_by_date = next_closing_date - timedelta(days=3)
    next_can_use_funds = next_closing_date + timedelta(days=3)
    next_due_date = next_closing_date + timedelta(days=25)
    
    # Calculate monthly timeline
    previous_month = start_date.strftime('%B %Y')
    current_month = start_date.strftime('%B %Y') if start_date.month == end_date.month else f"{start_date.strftime('%B')} - {end_date.strftime('%B %Y')}"
    following_month = due_date.strftime('%B %Y')
    
    return {
        'cycle_start': start_date.strftime('%b %d, %Y'),
        'cycle_end': end_date.strftime('%b %d, %Y'),
        'closing_date': closing_date.strftime('%b %d, %Y'),  # NEW: Explicit closing date
        'reporting_date': reporting_date.strftime('%b %d, %Y'),
        'pay_by_date': pay_by_date.strftime('%b %d, %Y'),
        'can_use_funds': can_use_funds.strftime('%b %d, %Y'),
        'due_date': due_date.strftime('%b %d, %Y'),
        'next_cycle_start': next_cycle_start.strftime('%b %d, %Y'),
        'next_cycle_end': next_cycle_end.strftime('%b %d, %Y'),
        'next_closing_date': next_closing_date.strftime('%b %d, %Y'),  # NEW: Next closing date
        'next_reporting_date': next_reporting_date.strftime('%b %d, %Y'),
        'next_pay_by_date': next_pay_by_date.strftime('%b %d, %Y'),
        'next_can_use_funds': next_can_use_funds.strftime('%b %d, %Y'),
        'next_due_date': next_due_date.strftime('%b %d, %Y'),
        'previous_month': previous_month,
        'current_month': current_month,
        'following_month': following_month
    }

@app.route('/')
def index():
    """Main page showing all cards"""
    cards = load_cards()
    return render_template('index.html', cards=cards)

@app.route('/add_card', methods=['POST'])
def add_card():
    """Add a new credit card"""
    try:
        # Get form data
        card_name = request.form.get('card_name', '').strip()
        credit_limit = float(request.form.get('credit_limit', 0))
        current_balance = float(request.form.get('current_balance', 0))
        cycle_start = request.form.get('cycle_start', '')
        cycle_end = request.form.get('cycle_end', '')
        
        # Validation
        if not card_name:
            flash('Card name is required', 'error')
            return redirect(url_for('index'))
        
        if credit_limit <= 0:
            flash('Credit limit must be greater than 0', 'error')
            return redirect(url_for('index'))
        
        if current_balance < 0:
            flash('Current balance cannot be negative', 'error')
            return redirect(url_for('index'))
        
        if current_balance > credit_limit:
            flash('Current balance cannot exceed credit limit', 'error')
            return redirect(url_for('index'))
        
        if not cycle_start or not cycle_end:
            flash('Both cycle start and end dates are required', 'error')
            return redirect(url_for('index'))
        
        # Calculate utilization
        utilization = (current_balance / credit_limit) * 100
        
        # Calculate actual available balance (what they have now)
        actual_available_balance = credit_limit - current_balance
        
        # Calculate target balances for different utilization levels
        target_balance_10_percent = credit_limit * 0.10  # 10% of credit limit
        target_balance_30_percent = credit_limit * 0.30  # 30% of credit limit
        
        # Calculate what their available balance should be at each level
        target_available_10_percent = credit_limit - target_balance_10_percent  # 90% of credit limit
        target_available_30_percent = credit_limit - target_balance_30_percent  # 70% of credit limit
        
        # Calculate how much they need to pay down to reach target available balances
        need_to_pay_10_percent = max(0, current_balance - target_balance_10_percent)
        need_to_pay_30_percent = max(0, current_balance - target_balance_30_percent)
        
        # Calculate dates
        dates = calculate_dates(cycle_start, cycle_end)
        
        # Create card object
        card = {
            'id': len(load_cards()) + 1,
            'name': card_name,
            'credit_limit': credit_limit,
            'current_balance': current_balance,
            'utilization': utilization,
            'available_balance': {
                'actual_available': actual_available_balance,
                'target_available_10_percent': target_available_10_percent,
                'target_available_30_percent': target_available_30_percent,
                'need_to_pay_10_percent': need_to_pay_10_percent,
                'need_to_pay_30_percent': need_to_pay_30_percent
            },
            'dates': dates
        }
        
        # Save card
        cards = load_cards()
        cards.append(card)
        save_cards(cards)
        
        flash(f'Card "{card_name}" added successfully!', 'success')
        return redirect(url_for('index'))
        
    except ValueError as e:
        flash('Please enter valid numbers for credit limit and balance', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error adding card: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/delete_card/<int:card_id>')
def delete_card(card_id):
    """Delete a credit card"""
    try:
        cards = load_cards()
        cards = [card for card in cards if card['id'] != card_id]
        save_cards(cards)
        flash('Card deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting card: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000) 