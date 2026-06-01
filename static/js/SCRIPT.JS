// Hospital Management System JavaScript

$(document).ready(function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Search functionality
    $('#searchInput').on('keyup', function() {
        var value = $(this).val().toLowerCase();
        $('#dataTable tbody tr').filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    // Form validation
    $('form').on('submit', function(e) {
        var isValid = true;
        $(this).find('[required]').each(function() {
            if (!$(this).val()) {
                isValid = false;
                $(this).addClass('is-invalid');
                $(this).next('.invalid-feedback').text('This field is required');
            } else {
                $(this).removeClass('is-invalid');
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            alert('Please fill in all required fields');
        }
    });

    // Date picker initialization
    $('input[type="date"]').on('change', function() {
        var date = $(this).val();
        if (date) {
            // You can add date validation here
            console.log('Selected date:', date);
        }
    });

    // Modal close confirmation
    $('.modal').on('hide.bs.modal', function(e) {
        var form = $(this).find('form');
        if (form.length && form.hasClass('modified')) {
            if (!confirm('You have unsaved changes. Are you sure you want to close?')) {
                e.preventDefault();
            }
        }
    });

    // Track form modifications
    $('form input, form select, form textarea').on('change', function() {
        $(this).closest('form').addClass('modified');
    });

    // Delete confirmation
    $('.delete-btn').on('click', function(e) {
        if (!confirm('Are you sure you want to delete this record? This action cannot be undone.')) {
            e.preventDefault();
        }
    });
});

// Function to load data via AJAX
function loadData(endpoint, targetElement) {
    $.ajax({
        url: endpoint,
        method: 'GET',
        success: function(data) {
            $(targetElement).html(data);
        },
        error: function(xhr, status, error) {
            console.error('Error loading data:', error);
            $(targetElement).html('<div class="alert alert-danger">Error loading data. Please try again.</div>');
        }
    });
}

// Function to refresh table data
function refreshTable(tableId, endpoint) {
    $.ajax({
        url: endpoint,
        method: 'GET',
        success: function(data) {
            $(tableId + ' tbody').empty();
            $.each(data, function(index, item) {
                // Add rows dynamically
                var row = '<tr>';
                $.each(item, function(key, value) {
                    row += '<td>' + (value || '-') + '</td>';
                });
                row += '</tr>';
                $(tableId + ' tbody').append(row);
            });
        }
    });
}

// Function to show loading spinner
function showLoading(element) {
    $(element).html('<div class="text-center"><div class="spinner"></div></div>');
}

// Function to format date
function formatDate(dateString) {
    if (!dateString) return '-';
    var date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Function to get status badge
function getStatusBadge(status) {
    var badgeClass = '';
    switch(status.toLowerCase()) {
        case 'scheduled':
            badgeClass = 'bg-primary';
            break;
        case 'completed':
            badgeClass = 'bg-success';
            break;
        case 'cancelled':
            badgeClass = 'bg-danger';
            break;
        case 'available':
            badgeClass = 'bg-success';
            break;
        case 'occupied':
            badgeClass = 'bg-warning';
            break;
        case 'paid':
            badgeClass = 'bg-success';
            break;
        case 'pending':
            badgeClass = 'bg-warning';
            break;
        default:
            badgeClass = 'bg-secondary';
    }
    return '<span class="badge ' + badgeClass + '">' + status + '</span>';
}

// Export functions if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        formatDate,
        formatCurrency,
        getStatusBadge
    };
}