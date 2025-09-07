// Application JavaScript

class NotificationManager {
    constructor() {
        this.permission = null;
        this.checkPermission();
    }
    
    async checkPermission() {
        if ('Notification' in window) {
            this.permission = await Notification.requestPermission();
        }
    }
    
    showNotification(title, options = {}) {
        if (this.permission === 'granted') {
            const notification = new Notification(title, {
                icon: '/static/icons/icon-192x192.png',
                badge: '/static/icons/icon-72x72.png',
                ...options
            });
            
            notification.onclick = () => {
                window.focus();
                notification.close();
            };
            
            // Auto close after 5 seconds
            setTimeout(() => notification.close(), 5000);
        }
    }
    
    notifyExpenseAdded(expense) {
        this.showNotification(
            'Nouvelle dépense ajoutée',
            {
                body: `${expense.person} a ajouté : ${expense.description} (${expense.amount}€)`,
                tag: 'expense-added'
            }
        );
    }
    
    notifyBudgetAlert(alert) {
        this.showNotification(
            'Alerte Budget',
            {
                body: alert.message,
                tag: 'budget-alert',
                urgency: alert.level === 'danger' ? 'high' : 'normal'
            }
        );
    }
    
    notifyValidationRequired(expense) {
        this.showNotification(
            'Validation requise',
            {
                body: `Dépense de ${expense.amount}€ en attente de validation`,
                tag: 'validation-required'
            }
        );
    }
}

class ExpenseApp {
    constructor() {
        this.categories = [];
        this.notificationManager = new NotificationManager();
        this.challenges = [];
        this.badges = [];
        this.init();
    }

    init() {
        this.loadCategories();
        this.setupEventListeners();
        this.setupThemeToggle();
        this.setTodayDate();
        this.setupToasts();
        this.loadChallenges();
        this.loadBadges();
        this.setupOfflineSupport();
    }
    
    setupOfflineSupport() {
        // Check if we're online
        window.addEventListener('online', () => {
            this.showToast('success', 'Connexion rétablie. Synchronisation en cours...');
            this.syncPendingData();
        });
        
        window.addEventListener('offline', () => {
            this.showToast('warning', 'Mode hors ligne activé');
        });
    }
    
    async syncPendingData() {
        // This would sync any pending data stored locally
        console.log('Syncing pending data...');
    }
    
    async loadChallenges() {
        try {
            const response = await fetch('/api/challenges');
            const data = await response.json();
            this.challenges = data.challenges;
            this.displayChallenges();
        } catch (error) {
            console.error('Error loading challenges:', error);
        }
    }
    
    displayChallenges() {
        const container = document.getElementById('challengesContainer');
        if (!container) return;
        
        container.innerHTML = '';
        
        this.challenges.forEach(challenge => {
            const challengeCard = this.createChallengeCard(challenge);
            container.appendChild(challengeCard);
        });
    }
    
    createChallengeCard(challenge) {
        const card = document.createElement('div');
        card.className = 'col-md-4';
        
        const progressColor = challenge.progress <= 50 ? 'success' : 
                             challenge.progress <= 80 ? 'warning' : 'danger';
        
        card.innerHTML = `
            <div class="card challenge-card h-100">
                <div class="card-body">
                    <h6 class="card-title">${challenge.name}</h6>
                    <p class="card-text small">${challenge.description}</p>
                    <div class="progress mb-2" style="height: 8px;">
                        <div class="progress-bar bg-${progressColor}" role="progressbar" 
                             style="width: ${Math.min(challenge.progress, 100)}%"></div>
                    </div>
                    <div class="d-flex justify-content-between">
                        <small>${challenge.current_spent.toFixed(2)}€</small>
                        <small>${challenge.target_amount.toFixed(2)}€</small>
                    </div>
                </div>
            </div>
        `;
        
        return card;
    }
    
    async loadBadges() {
        try {
            const response = await fetch('/api/badges');
            const data = await response.json();
            this.badges = data.badges;
            this.displayBadges();
        } catch (error) {
            console.error('Error loading badges:', error);
        }
    }
    
    displayBadges() {
        const container = document.getElementById('badgesContainer');
        if (!container) return;
        
        container.innerHTML = '';
        
        this.badges.forEach(badge => {
            const badgeElement = this.createBadgeElement(badge);
            container.appendChild(badgeElement);
        });
    }
    
    createBadgeElement(badge) {
        const element = document.createElement('div');
        element.className = 'col-auto';
        
        element.innerHTML = `
            <div class="badge-item text-center p-2" title="${badge.description}">
                <i class="${badge.icon} fa-2x text-warning mb-1"></i>
                <div class="small">${badge.name}</div>
            </div>
        `;
        
        return element;
    }

    async loadCategories() {
        try {
            // For now, we'll use hardcoded categories matching the backend
            this.categories = [
                { id: 1, name: 'Alimentation', color: '#28a745', icon: 'fas fa-utensils' },
                { id: 2, name: 'Transport', color: '#007bff', icon: 'fas fa-car' },
                { id: 3, name: 'Logement', color: '#6f42c1', icon: 'fas fa-home' },
                { id: 4, name: 'Divertissement', color: '#e83e8c', icon: 'fas fa-gamepad' },
                { id: 5, name: 'Santé', color: '#dc3545', icon: 'fas fa-heartbeat' },
                { id: 6, name: 'Vêtements', color: '#fd7e14', icon: 'fas fa-tshirt' },
                { id: 7, name: 'Éducation', color: '#20c997', icon: 'fas fa-graduation-cap' },
                { id: 8, name: 'Abonnements', color: '#6610f2', icon: 'fas fa-sync-alt' },
                { id: 9, name: 'Autres', color: '#6c757d', icon: 'fas fa-ellipsis-h' }
            ];
            this.populateCategorySelects();
        } catch (error) {
            console.error('Error loading categories:', error);
        }
    }

    populateCategorySelects() {
        const selects = ['expenseCategory', 'subscriptionCategory'];
        
        selects.forEach(selectId => {
            const select = document.getElementById(selectId);
            if (select) {
                // Clear existing options except the first one
                while (select.children.length > 1) {
                    select.removeChild(select.lastChild);
                }
                
                this.categories.forEach(category => {
                    const option = document.createElement('option');
                    option.value = category.id;
                    option.textContent = category.name;
                    option.setAttribute('data-color', category.color);
                    option.setAttribute('data-icon', category.icon);
                    select.appendChild(option);
                });
            }
        });
    }

    setupEventListeners() {
        // Quick Add Modal Form Submission
        document.getElementById('quickAddSubmit').addEventListener('click', () => {
            this.handleQuickAdd();
        });

        // Tab change event to update submit button text
        document.querySelectorAll('#quickAddModal .nav-link').forEach(tab => {
            tab.addEventListener('click', (e) => {
                const targetTab = e.target.getAttribute('data-bs-target');
                const submitBtn = document.getElementById('quickAddSubmit');
                
                switch (targetTab) {
                    case '#expense-pane':
                        submitBtn.textContent = 'Ajouter Dépense';
                        break;
                    case '#income-pane':
                        submitBtn.textContent = 'Ajouter Revenu';
                        break;
                    case '#subscription-pane':
                        submitBtn.textContent = 'Ajouter Abonnement';
                        break;
                }
            });
        });

        // Reset forms when modal is hidden
        document.getElementById('quickAddModal').addEventListener('hidden.bs.modal', () => {
            this.resetForms();
        });

        // Form validation on input
        this.setupFormValidation();
    }

    setupFormValidation() {
        const forms = ['expenseForm', 'incomeForm', 'subscriptionForm'];
        
        forms.forEach(formId => {
            const form = document.getElementById(formId);
            if (form) {
                form.addEventListener('input', (e) => {
                    this.validateForm(form);
                });
            }
        });
    }

    validateForm(form) {
        const inputs = form.querySelectorAll('input[required], select[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });
        
        return isValid;
    }

    async handleQuickAdd() {
        const activeTab = document.querySelector('#quickAddModal .tab-pane.show.active');
        const activeTabId = activeTab.id;
        
        let formData = {};
        let endpoint = '';
        let method = 'POST';
        let form = null;
        
        switch (activeTabId) {
            case 'expense-pane':
                form = document.getElementById('expenseForm');
                if (!this.validateForm(form)) return;
                
                formData = {
                    amount: document.getElementById('expenseAmount').value,
                    description: document.getElementById('expenseDescription').value,
                    category_id: document.getElementById('expenseCategory').value,
                    date: document.getElementById('expenseDate').value,
                    is_exceptional: document.getElementById('expenseExceptional').checked,
                    person: document.getElementById('expensePerson').value,
                    needs_reimbursement: document.getElementById('expenseReimbursement').checked,
                    notes: document.getElementById('expenseNotes').value
                };
                
                // Check if we're editing an existing expense
                if (window.editingExpenseId) {
                    endpoint = `/api/expenses/${window.editingExpenseId}`;
                    method = 'PUT';
                } else {
                    endpoint = '/api/expenses';
                }
                break;
                
            case 'income-pane':
                form = document.getElementById('incomeForm');
                if (!this.validateForm(form)) return;
                
                formData = {
                    amount: document.getElementById('incomeAmount').value,
                    description: document.getElementById('incomeDescription').value,
                    date: document.getElementById('incomeDate').value,
                    is_recurring: document.getElementById('incomeRecurring').checked
                };
                endpoint = '/api/income';
                break;
                
            case 'subscription-pane':
                form = document.getElementById('subscriptionForm');
                if (!this.validateForm(form)) return;
                
                formData = {
                    name: document.getElementById('subscriptionName').value,
                    amount: document.getElementById('subscriptionAmount').value,
                    billing_cycle: document.getElementById('subscriptionCycle').value,
                    category_id: document.getElementById('subscriptionCategory').value,
                    next_billing: document.getElementById('subscriptionNextBilling').value,
                    person: document.getElementById('subscriptionPerson').value || 'Non spécifié'
                };
                
                // Check if we're editing an existing subscription
                if (window.editingSubscriptionId) {
                    endpoint = `/api/subscriptions/${window.editingSubscriptionId}`;
                    method = 'PUT';
                } else {
                    endpoint = '/api/subscriptions';
                }
                break;
                
            default:
                return;
        }
        
        try {
            const response = await fetch(endpoint, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.showToast('success', result.message);
                
                // Handle expense-specific features
                if (activeTabId === 'expense-pane') {
                    // Show notification for new expense
                    this.notificationManager.notifyExpenseAdded({
                        person: formData.person,
                        description: formData.description,
                        amount: formData.amount
                    });
                    
                    // Show budget alert if present
                    if (result.budget_alert) {
                        this.notificationManager.notifyBudgetAlert(result.budget_alert);
                        this.showToast(result.budget_alert.level === 'danger' ? 'error' : 'warning', 
                                     result.budget_alert.message);
                    }
                    
                    // Show validation notification if needed
                    if (result.requires_validation) {
                        this.notificationManager.notifyValidationRequired({
                            amount: formData.amount
                        });
                        this.showToast('info', 'Cette dépense nécessite une validation');
                    }
                    
                    // Check for badge achievements
                    this.checkBadgeAchievements();
                }
                
                this.closeModal();
                // Refresh the page to show updated data
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                this.showToast('error', result.message || 'Une erreur s\'est produite');
            }
        } catch (error) {
            console.error('Error:', error);
            this.showToast('error', 'Erreur de connexion');
        }
    }

    setupThemeToggle() {
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        const html = document.documentElement;
        
        // Load saved theme
        const savedTheme = localStorage.getItem('theme') || 'light';
        html.setAttribute('data-bs-theme', savedTheme);
        this.updateThemeIcon(savedTheme, themeIcon);
        
        themeToggle.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            
            html.setAttribute('data-bs-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            this.updateThemeIcon(newTheme, themeIcon);
            
            // Add smooth transition
            document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
            setTimeout(() => {
                document.body.style.transition = '';
            }, 300);
        });
    }

    updateThemeIcon(theme, icon) {
        if (theme === 'dark') {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
    }

    setTodayDate() {
        const today = new Date().toISOString().split('T')[0];
        const dateInputs = ['expenseDate', 'incomeDate'];
        
        dateInputs.forEach(inputId => {
            const input = document.getElementById(inputId);
            if (input) {
                input.value = today;
            }
        });
        
        // Set next billing date to tomorrow for subscriptions
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        const tomorrowStr = tomorrow.toISOString().split('T')[0];
        
        const nextBillingInput = document.getElementById('subscriptionNextBilling');
        if (nextBillingInput) {
            nextBillingInput.value = tomorrowStr;
        }
    }

    setupToasts() {
        this.successToast = new bootstrap.Toast(document.getElementById('successToast'));
        this.errorToast = new bootstrap.Toast(document.getElementById('errorToast'));
    }

    showToast(type, message) {
        if (type === 'success') {
            document.querySelector('#successToast .toast-body').textContent = message;
            this.successToast.show();
        } else {
            document.querySelector('#errorToast .toast-body').textContent = message;
            this.errorToast.show();
        }
    }

    closeModal() {
        const modal = bootstrap.Modal.getInstance(document.getElementById('quickAddModal'));
        modal.hide();
    }

    resetForms() {
        const forms = ['expenseForm', 'incomeForm', 'subscriptionForm'];
        
        forms.forEach(formId => {
            const form = document.getElementById(formId);
            if (form) {
                form.reset();
                // Remove validation classes
                form.querySelectorAll('.is-invalid').forEach(input => {
                    input.classList.remove('is-invalid');
                });
            }
        });
        
        // Clear editing state
        window.editingExpenseId = null;
        window.editingSubscriptionId = null;
        
        // Reset submit button text
        document.getElementById('quickAddSubmit').textContent = 'Ajouter';
        
        // Reset dates
        this.setTodayDate();
    }

    // Utility function to format currency
    formatCurrency(amount) {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'EUR'
        }).format(amount);
    }

    // Utility function to format date
    formatDate(dateString) {
        return new Intl.DateTimeFormat('fr-FR').format(new Date(dateString));
    }
    
    async checkBadgeAchievements() {
        try {
            const response = await fetch('/api/badges?user_name=' + encodeURIComponent('current_user'));
            const data = await response.json();
            
            // Check if user earned new badges (simplified check)
            if (data.badges && data.badges.length > this.badges.length) {
                const newBadges = data.badges.slice(this.badges.length);
                newBadges.forEach(badge => {
                    this.showBadgeEarned(badge);
                });
                this.badges = data.badges;
            }
        } catch (error) {
            console.error('Error checking badge achievements:', error);
        }
    }
    
    showBadgeEarned(badge) {
        const toast = document.createElement('div');
        toast.className = 'toast badge-toast';
        toast.innerHTML = `
            <div class="toast-header bg-warning text-dark">
                <i class="${badge.icon} me-2"></i>
                <strong class="me-auto">Badge Gagné !</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                <strong>${badge.name}</strong><br>
                ${badge.description}
            </div>
        `;
        
        document.querySelector('.toast-container').appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remove from DOM after it's hidden
        toast.addEventListener('hidden.bs.toast', () => {
            toast.remove();
        });
    }
    
    async createChallenge(challengeData) {
        try {
            const response = await fetch('/api/challenges', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(challengeData)
            });
            
            const result = await response.json();
            if (result.success) {
                this.showToast('success', 'Défi créé avec succès !');
                this.loadChallenges();
            } else {
                this.showToast('error', result.message);
            }
        } catch (error) {
            console.error('Error creating challenge:', error);
            this.showToast('error', 'Erreur lors de la création du défi');
        }
    }
    
    async generateQRCode(expenseId) {
        try {
            const response = await fetch(`/api/qr-share/${expenseId}`);
            const data = await response.json();
            
            if (data.success) {
                // Show QR code in modal (would need QR library in real implementation)
                this.showQRModal(data.qr_text);
            }
        } catch (error) {
            console.error('Error generating QR code:', error);
        }
    }
    
    showQRModal(qrText) {
        // This would show a modal with QR code
        // For now, just copy to clipboard
        navigator.clipboard.writeText(qrText).then(() => {
            this.showToast('success', 'Données copiées dans le presse-papier');
        });
    }
    
    async createBackup() {
        try {
            const response = await fetch('/api/backup', { method: 'POST' });
            const data = await response.json();
            
            if (data.success) {
                // Download backup as JSON file
                const blob = new Blob([JSON.stringify(data.backup_data, null, 2)], {
                    type: 'application/json'
                });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `depenses-couple-backup-${new Date().toISOString().split('T')[0]}.json`;
                a.click();
                URL.revokeObjectURL(url);
                
                this.showToast('success', 'Sauvegarde créée avec succès !');
            }
        } catch (error) {
            console.error('Error creating backup:', error);
            this.showToast('error', 'Erreur lors de la création de la sauvegarde');
        }
    }
}

// Chart utilities
class ChartManager {
    constructor() {
        this.charts = {};
    }

    async createExpensesChart(canvasId) {
        try {
            const response = await fetch('/api/charts/expenses');
            const data = await response.json();
            
            const ctx = document.getElementById(canvasId).getContext('2d');
            
            this.charts[canvasId] = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.map(item => item.month),
                    datasets: [{
                        label: 'Dépenses (€)',
                        data: data.map(item => item.amount),
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: '#667eea',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 6,
                        pointHoverRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            },
                            ticks: {
                                callback: function(value) {
                                    return value + '€';
                                }
                            }
                        },
                        x: {
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    }
                }
            });
        } catch (error) {
            console.error('Error creating expenses chart:', error);
        }
    }

    async createCategoriesChart(canvasId) {
        try {
            const response = await fetch('/api/charts/categories');
            const data = await response.json();
            
            if (data.length === 0) return;
            
            const ctx = document.getElementById(canvasId).getContext('2d');
            
            this.charts[canvasId] = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: data.map(item => item.category),
                    datasets: [{
                        data: data.map(item => item.amount),
                        backgroundColor: data.map(item => item.color),
                        borderWidth: 0,
                        hoverBorderWidth: 3,
                        hoverBorderColor: '#fff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                padding: 20,
                                usePointStyle: true,
                                font: {
                                    size: 12
                                }
                            }
                        }
                    },
                    cutout: '60%'
                }
            });
        } catch (error) {
            console.error('Error creating categories chart:', error);
        }
    }

    destroyChart(canvasId) {
        if (this.charts[canvasId]) {
            this.charts[canvasId].destroy();
            delete this.charts[canvasId];
        }
    }

    destroyAllCharts() {
        Object.keys(this.charts).forEach(canvasId => {
            this.destroyChart(canvasId);
        });
    }
}

// Animation utilities
class AnimationManager {
    static observeElements() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-up');
                }
            });
        }, {
            threshold: 0.1
        });

        document.querySelectorAll('.card, .stats-card').forEach(el => {
            observer.observe(el);
        });
    }

    static animateNumbers() {
        document.querySelectorAll('.stats-value').forEach(el => {
            const finalValue = parseFloat(el.textContent.replace(/[^\d.-]/g, ''));
            if (isNaN(finalValue)) return;
            
            let currentValue = 0;
            const increment = finalValue / 50;
            const timer = setInterval(() => {
                currentValue += increment;
                if (currentValue >= finalValue) {
                    currentValue = finalValue;
                    clearInterval(timer);
                }
                
                const formattedValue = new Intl.NumberFormat('fr-FR', {
                    style: 'currency',
                    currency: 'EUR'
                }).format(currentValue);
                
                el.textContent = formattedValue;
            }, 20);
        });
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize main app
    window.expenseApp = new ExpenseApp();
    window.chartManager = new ChartManager();
    
    // Initialize animations
    AnimationManager.observeElements();
    
    // Initialize charts on dashboard
    if (document.getElementById('expensesChart')) {
        window.chartManager.createExpensesChart('expensesChart');
    }
    
    if (document.getElementById('categoriesChart')) {
        window.chartManager.createCategoriesChart('categoriesChart');
    }
    
    // Animate numbers on page load
    setTimeout(() => {
        AnimationManager.animateNumbers();
    }, 500);
});

// Handle page visibility change to refresh charts
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // Refresh charts when page becomes visible
        setTimeout(() => {
            if (window.chartManager) {
                window.chartManager.destroyAllCharts();
                
                if (document.getElementById('expensesChart')) {
                    window.chartManager.createExpensesChart('expensesChart');
                }
                
                if (document.getElementById('categoriesChart')) {
                    window.chartManager.createCategoriesChart('categoriesChart');
                }
            }
        }, 100);
    }
});