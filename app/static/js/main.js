// Main JavaScript for Conquer Bible v2

$(document).ready(function() {
    // Enable tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Enable popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Add active class to current page in navbar
    $('.navbar-nav .nav-link').each(function() {
        if ($(this).attr('href') === window.location.pathname) {
            $(this).addClass('active');
        }
    });

    // Highlight all progress bars that are at 100%
    $('.progress-bar').each(function() {
        var value = parseInt($(this).attr('aria-valuenow'));
        if (value === 100) {
            $(this).removeClass('bg-primary').addClass('bg-success');
        }
    });

    // Confirmation dialogs
    $('.confirm-action').on('click', function(e) {
        if (!confirm($(this).data('confirm') || 'Are you sure?')) {
            e.preventDefault();
            return false;
        }
    });
});