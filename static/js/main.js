/**
 * LLM Agent Analytics Dashboard
 * Main JavaScript file
 */

document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle for mobile
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
    
    // Dropdown menus in sidebar
    const dropdowns = document.querySelectorAll('.sidebar-dropdown > a');
    
    dropdowns.forEach(dropdown => {
        // Auto-expand if an item in the dropdown is active
        const submenu = dropdown.nextElementSibling;
        const hasActiveChild = submenu && submenu.querySelector('a.active');
        
        if (hasActiveChild) {
            dropdown.parentElement.classList.add('active');
            submenu.style.maxHeight = submenu.scrollHeight + 'px';
        }
        
        dropdown.addEventListener('click', function(e) {
            e.preventDefault();
            
            const parent = this.parentElement;
            parent.classList.toggle('active');
            
            const submenu = this.nextElementSibling;
            if (submenu) {
                if (parent.classList.contains('active')) {
                    submenu.style.maxHeight = submenu.scrollHeight + 'px';
                } else {
                    submenu.style.maxHeight = 0;
                }
            }
        });
    });
    
    // Time range filter
    const timeRangeSelect = document.getElementById('time-range');
    if (timeRangeSelect) {
        timeRangeSelect.addEventListener('change', function() {
            const days = this.value;
            // You would typically reload data based on the selected range
            console.log(`Time range changed to ${days} days`);
            
            // Example: refresh page with new days parameter
            // window.location.href = window.location.pathname + `?days=${days}`;
        });
    }
    
    // Chart resizing on window resize
    window.addEventListener('resize', function() {
        const charts = document.querySelectorAll('canvas');
        charts.forEach(chart => {
            if (chart.chart) {
                chart.chart.resize();
            }
        });
    });
    
    // Chart download buttons
    const downloadButtons = document.querySelectorAll('.chart-action-btn[title="Download"]');
    downloadButtons.forEach(button => {
        button.addEventListener('click', function() {
            const chartContainer = this.closest('.chart-container');
            const canvas = chartContainer.querySelector('canvas');
            const chartName = chartContainer.querySelector('h3').textContent.trim();
            
            if (canvas) {
                const a = document.createElement('a');
                a.href = canvas.toDataURL('image/png');
                a.download = `${chartName.toLowerCase().replace(/\s+/g, '_')}.png`;
                a.click();
            }
        });
    });
    
    // Chart expand buttons (modal view)
    const expandButtons = document.querySelectorAll('.chart-action-btn[title="Expand"]');
    expandButtons.forEach(button => {
        button.addEventListener('click', function() {
            const chartContainer = this.closest('.chart-container');
            const canvas = chartContainer.querySelector('canvas');
            const chartTitle = chartContainer.querySelector('h3').textContent;
            
            if (canvas) {
                createModal(chartTitle, canvas);
            }
        });
    });
    
    // Modal creation
    function createModal(title, canvas) {
        // First remove any existing modals
        const existingModal = document.querySelector('.chart-modal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Create modal container
        const modal = document.createElement('div');
        modal.className = 'chart-modal';
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.width = '100%';
        modal.style.height = '100%';
        modal.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        modal.style.zIndex = '1000';
        modal.style.display = 'flex';
        modal.style.alignItems = 'center';
        modal.style.justifyContent = 'center';
        modal.style.flexDirection = 'column';
        modal.style.padding = '2rem';
        
        // Create modal header
        const modalHeader = document.createElement('div');
        modalHeader.style.display = 'flex';
        modalHeader.style.justifyContent = 'space-between';
        modalHeader.style.width = '100%';
        modalHeader.style.maxWidth = '900px';
        modalHeader.style.marginBottom = '1rem';
        
        // Create title
        const modalTitle = document.createElement('h2');
        modalTitle.textContent = title;
        modalTitle.style.color = 'white';
        modalTitle.style.margin = '0';
        
        // Create close button
        const closeButton = document.createElement('button');
        closeButton.innerHTML = '&times;';
        closeButton.style.background = 'none';
        closeButton.style.border = 'none';
        closeButton.style.color = 'white';
        closeButton.style.fontSize = '2rem';
        closeButton.style.cursor = 'pointer';
        closeButton.style.padding = '0';
        closeButton.style.lineHeight = '1';
        
        // Create content container
        const modalContent = document.createElement('div');
        modalContent.style.backgroundColor = 'var(--bg-secondary)';
        modalContent.style.borderRadius = 'var(--radius-md)';
        modalContent.style.padding = '1.5rem';
        modalContent.style.width = '100%';
        modalContent.style.maxWidth = '900px';
        modalContent.style.height = '70vh';
        
        // Clone the canvas
        const clonedCanvas = document.createElement('canvas');
        clonedCanvas.style.width = '100%';
        clonedCanvas.style.height = '100%';
        
        // Append elements
        modalHeader.appendChild(modalTitle);
        modalHeader.appendChild(closeButton);
        modalContent.appendChild(clonedCanvas);
        modal.appendChild(modalHeader);
        modal.appendChild(modalContent);
        document.body.appendChild(modal);
        
        // Make the modal closable
        closeButton.addEventListener('click', function() {
            modal.remove();
        });
        
        // Close when clicking outside
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.remove();
            }
        });
        
        // Escape key closes modal
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && document.querySelector('.chart-modal')) {
                modal.remove();
            }
        });
        
        // Clone the chart to the new canvas
        const chartInstance = Chart.getChart(canvas);
        if (chartInstance) {
            new Chart(clonedCanvas, {
                type: chartInstance.config.type,
                data: JSON.parse(JSON.stringify(chartInstance.data)),
                options: JSON.parse(JSON.stringify(chartInstance.options))
            });
        }
    }
    
    // Fetch notifications (example, would need to be implemented)
    function fetchNotifications() {
        // This would typically be an API call
        const notificationsEl = document.getElementById('notifications-list');
        if (notificationsEl) {
            fetch('/api/notifications')
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        notificationsEl.innerHTML = '';
                        data.forEach(notification => {
                            const li = document.createElement('li');
                            li.className = notification.read ? 'read' : '';
                            li.innerHTML = `
                                <div class="notification-icon ${notification.type}">
                                    <i class="fas fa-${notification.type === 'error' ? 'exclamation-circle' : 
                                                    notification.type === 'warning' ? 'exclamation-triangle' : 
                                                    'info-circle'}"></i>
                                </div>
                                <div class="notification-content">
                                    <p>${notification.message}</p>
                                    <span class="notification-time">${notification.time}</span>
                                </div>
                                <button class="mark-read-btn" data-id="${notification.id}">
                                    <i class="fas fa-check"></i>
                                </button>
                            `;
                            notificationsEl.appendChild(li);
                        });
                        
                        // Add event listeners to mark-read buttons
                        document.querySelectorAll('.mark-read-btn').forEach(btn => {
                            btn.addEventListener('click', function() {
                                const notificationId = this.dataset.id;
                                markNotificationAsRead(notificationId);
                            });
                        });
                    }
                })
                .catch(error => {
                    console.error('Error fetching notifications:', error);
                });
        }
    }
    
    // Mark notification as read (example)
    function markNotificationAsRead(id) {
        fetch(`/api/notifications/${id}/read`, {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const notificationEl = document.querySelector(`.mark-read-btn[data-id="${id}"]`).closest('li');
                    notificationEl.classList.add('read');
                }
            })
            .catch(error => {
                console.error('Error marking notification as read:', error);
            });
    }
    
    // Init notifications if they exist
    const notificationsToggle = document.getElementById('notifications-toggle');
    if (notificationsToggle) {
        // Toggle notifications dropdown
        notificationsToggle.addEventListener('click', function() {
            const dropdown = document.querySelector('.notifications-menu');
            dropdown.classList.toggle('active');
            fetchNotifications();
        });
        
        // Close notifications when clicking outside
        document.addEventListener('click', function(e) {
            const dropdown = document.querySelector('.notifications-menu');
            if (dropdown && dropdown.classList.contains('active') && 
                !e.target.closest('.notifications-dropdown')) {
                dropdown.classList.remove('active');
            }
        });
        
        // Mark all as read button
        const markAllReadBtn = document.querySelector('.mark-all-read');
        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', function(e) {
                e.preventDefault();
                fetch('/api/notifications/mark-all-read', {
                    method: 'POST'
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.querySelectorAll('#notifications-list li').forEach(li => {
                                li.classList.add('read');
                            });
                            document.querySelector('.notification-badge').textContent = '0';
                        }
                    })
                    .catch(error => {
                        console.error('Error marking all notifications as read:', error);
                    });
            });
        }
    }
});