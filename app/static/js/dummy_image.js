// Generate a placeholder image for the landing page
$(document).ready(function() {
    // This creates a placeholder image since we can't actually create real image files
    var canvas = document.createElement('canvas');
    canvas.width = 500;
    canvas.height = 350;
    var ctx = canvas.getContext('2d');

    // Background
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, 500, 350);

    // Book cover
    ctx.fillStyle = '#563d7c';
    ctx.fillRect(150, 50, 200, 250);

    // Book pages (side)
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(350, 50, 20, 250);

    // Cross symbol
    ctx.strokeStyle = '#ffc107';
    ctx.lineWidth = 8;
    ctx.beginPath();
    ctx.moveTo(250, 90);
    ctx.lineTo(250, 180);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(210, 135);
    ctx.lineTo(290, 135);
    ctx.stroke();

    // Text
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 20px Arial';
    ctx.textAlign = 'center';
    ctx.fillText('聖經', 250, 220);
    ctx.font = '16px Arial';
    ctx.fillText('Bible', 250, 250);

    // Convert to image
    var dataUrl = canvas.toDataURL();

    // If the bible-reading image doesn't exist, use our generated one
    $('img[src$="bible-reading.png"]').on('error', function() {
        $(this).attr('src', dataUrl);
    });

    // Also manually trigger it for development
    setTimeout(function() {
        $('img[src$="bible-reading.png"]').attr('src', dataUrl);
    }, 100);
});