import json
import os
import secrets
from datetime import datetime
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'it-agent-dev-secret-key-12345'

# In-memory data store
DATA = {
    "users": [
        {"id": "U001", "name": "John Smith", "email": "john@company.com", "role": "Manager", "status": "active", "license_id": "L001"},
        {"id": "U002", "name": "Sarah Johnson", "email": "sarah@company.com", "role": "Developer", "status": "active", "license_id": "L002"},
        {"id": "U003", "name": "Mike Chen", "email": "mike@company.com", "role": "Analyst", "status": "active", "license_id": "L003"},
        {"id": "U004", "name": "David Brown", "email": "david@company.com", "role": "Developer", "status": "active", "license_id": "L004"},
        {"id": "U005", "name": "Emma Wilson", "email": "emma@company.com", "role": "Manager", "status": "inactive", "license_id": None},
    ],
    "licenses": [
        {"id": "L001", "type": "Professional", "assigned_to": "U001", "status": "active"},
        {"id": "L002", "type": "Professional", "assigned_to": "U002", "status": "active"},
        {"id": "L003", "type": "Standard", "assigned_to": "U003", "status": "active"},
        {"id": "L004", "type": "Professional", "assigned_to": "U004", "status": "active"},
        {"id": "L005", "type": "Standard", "assigned_to": None, "status": "available"},
        {"id": "L006", "type": "Enterprise", "assigned_to": None, "status": "available"},
        {"id": "L007", "type": "Standard", "assigned_to": None, "status": "available"},
        {"id": "L008", "type": "Professional", "assigned_to": None, "status": "available"},
    ],
    "audit_log": [
        {"timestamp": "2026-04-15 09:00:00", "action": "User Created", "performed_by": "admin", "details": "Created user John Smith"},
        {"timestamp": "2026-04-15 09:15:00", "action": "License Assigned", "performed_by": "admin", "details": "Assigned license L001 to John Smith"},
    ]
}


def log_action(action, details):
    """Log an audit action."""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "performed_by": "admin",
        "details": details
    }
    DATA['audit_log'].append(entry)


def find_user_by_email(email):
    """Find user by email (case-insensitive)."""
    for user in DATA['users']:
        if user['email'].lower() == email.lower():
            return user
    return None


def find_user_by_id(user_id):
    """Find user by ID."""
    for user in DATA['users']:
        if user['id'] == user_id:
            return user
    return None


def find_license_by_id(license_id):
    """Find license by ID."""
    for lic in DATA['licenses']:
        if lic['id'] == license_id:
            return lic
    return None


def generate_temp_password():
    """Generate a temporary password."""
    return secrets.token_hex(4).upper()


# Routes

@app.route('/')
def dashboard():
    """Dashboard with statistics."""
    user_count = len(DATA['users'])
    active_users = len([u for u in DATA['users'] if u['status'] == 'active'])
    license_count = len(DATA['licenses'])
    available_licenses = len([l for l in DATA['licenses'] if l['status'] == 'available'])
    recent_logs = DATA['audit_log'][-5:] if DATA['audit_log'] else []

    return render_template(
        'dashboard.html',
        user_count=user_count,
        active_users=active_users,
        license_count=license_count,
        available_licenses=available_licenses,
        recent_logs=recent_logs
    )


@app.route('/users')
def users_list():
    """User management page."""
    return render_template('users.html', users=DATA['users'])


@app.route('/users/create', methods=['POST'])
def create_user():
    """Create a new user."""
    name = request.form.get('user_name', '').strip()
    email = request.form.get('user_email', '').strip()
    role = request.form.get('user_role', 'Developer').strip()

    if not name or not email:
        flash('Name and email are required', 'danger')
        return redirect(url_for('users_list'))

    if find_user_by_email(email):
        flash(f'User with email {email} already exists', 'danger')
        return redirect(url_for('users_list'))

    new_user = {
        "id": f"U{str(len(DATA['users']) + 1).zfill(3)}",
        "name": name,
        "email": email,
        "role": role,
        "status": "active",
        "license_id": None
    }
    DATA['users'].append(new_user)
    log_action("User Created", f"Created user {name} ({email}) with role {role}")
    flash(f'User {name} created successfully', 'success')
    return redirect(url_for('users_list'))


@app.route('/users/reset-password', methods=['POST'])
def reset_password():
    """Reset password for a user."""
    email = request.form.get('reset_email', '').strip()

    user = find_user_by_email(email)
    if not user:
        flash(f'User with email {email} not found', 'danger')
        return redirect(url_for('users_list'))

    temp_password = generate_temp_password()
    log_action("Password Reset", f"Reset password for {user['name']} ({email})")
    flash(f'Password reset for {user["name"]}. Temporary password: <strong>{temp_password}</strong>', 'success')
    return redirect(url_for('users_list'))


@app.route('/users/toggle-status', methods=['POST'])
def toggle_status():
    """Toggle user active/inactive status."""
    user_id = request.form.get('user_id', '').strip()

    user = find_user_by_id(user_id)
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('users_list'))

    old_status = user['status']
    user['status'] = 'inactive' if user['status'] == 'active' else 'active'
    log_action("Status Changed", f"Changed {user['name']} status from {old_status} to {user['status']}")
    flash(f'User {user["name"]} status changed to {user["status"]}', 'success')
    return redirect(url_for('users_list'))


@app.route('/licenses')
def licenses_list():
    """License management page."""
    users_by_id = {u['id']: u for u in DATA['users']}
    return render_template('licenses.html', licenses=DATA['licenses'], users_by_id=users_by_id)


@app.route('/licenses/assign', methods=['POST'])
def assign_license():
    """Assign a license to a user."""
    license_id = request.form.get('license_id', '').strip()
    email = request.form.get('assign_email', '').strip()

    user = find_user_by_email(email)
    if not user:
        flash(f'User with email {email} not found', 'danger')
        return redirect(url_for('licenses_list'))

    license = find_license_by_id(license_id)
    if not license:
        flash(f'License {license_id} not found', 'danger')
        return redirect(url_for('licenses_list'))

    if license['status'] == 'available':
        # Remove license from any previous user
        for u in DATA['users']:
            if u['license_id'] == license_id:
                u['license_id'] = None

        # Assign to new user
        user['license_id'] = license_id
        license['assigned_to'] = user['id']
        license['status'] = 'active'

        log_action("License Assigned", f"Assigned license {license_id} ({license['type']}) to {user['name']}")
        flash(f'License {license_id} assigned to {user["name"]}', 'success')
    else:
        flash(f'License {license_id} is not available', 'danger')

    return redirect(url_for('licenses_list'))


@app.route('/audit')
def audit_log():
    """View audit log."""
    return render_template('audit.html', logs=DATA['audit_log'])


@app.route('/api/status')
def api_status():
    """JSON API for health checks."""
    return jsonify({
        "users": len(DATA['users']),
        "licenses": len(DATA['licenses']),
        "audit": DATA['audit_log'][-5:]
    })


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "IT Admin Panel"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
