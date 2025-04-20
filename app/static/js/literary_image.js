// 為首頁生成文青風格的聖經圖像
$(document).ready(function() {
    // 創建Canvas元素
    var canvas = document.createElement('canvas');
    canvas.width = 500;
    canvas.height = 350;
    var ctx = canvas.getContext('2d');

    // 設定背景 - 淡米色
    ctx.fillStyle = '#f5f0e6';
    ctx.fillRect(0, 0, 500, 350);

    // 繪製裝飾性小圓點 - 散落的風格
    for (let i = 0; i < 20; i++) {
        const x = Math.random() * canvas.width;
        const y = Math.random() * canvas.height;
        const radius = Math.random() * 4 + 1;
        const colors = ['rgba(88, 162, 100, 0.2)', 'rgba(224, 122, 95, 0.2)', 'rgba(95, 168, 224, 0.2)'];
        const color = colors[Math.floor(Math.random() * colors.length)];

        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
    }

    // 繪製裝飾性圓形 - 左上角
    ctx.fillStyle = 'rgba(88, 162, 100, 0.15)';
    ctx.beginPath();
    ctx.arc(50, 50, 80, 0, Math.PI * 2);
    ctx.fill();

    // 繪製裝飾性圓形 - 右下角
    ctx.fillStyle = 'rgba(224, 122, 95, 0.1)';
    ctx.beginPath();
    ctx.arc(450, 300, 100, 0, Math.PI * 2);
    ctx.fill();

    // 繪製書本
    // 書本封面
    ctx.save();
    ctx.translate(250, 175);
    ctx.rotate(Math.PI * 0.05);

    // 書本陰影
    ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
    ctx.beginPath();
    ctx.roundRect(-95, -123, 190, 246, 5);
    ctx.fill();

    // 漸變書本封面
    const gradient = ctx.createLinearGradient(-90, -120, 90, 120);
    gradient.addColorStop(0, '#58a264');
    gradient.addColorStop(1, '#4c8d56');
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.roundRect(-90, -120, 180, 240, 5);
    ctx.fill();
    ctx.restore();

    // 書頁邊緣
    ctx.fillStyle = '#fff';
    ctx.save();
    ctx.translate(250, 175);
    ctx.rotate(Math.PI * 0.05);
    ctx.fillRect(90, -120, 12, 240);
    // 頁面質感
    for (let i = 0; i < 12; i++) {
        ctx.fillStyle = `rgba(0, 0, 0, ${0.03 + i * 0.005})`;
        ctx.fillRect(90 + i, -120, 1, 240);
    }
    ctx.restore();

    // 繪製書本花紋裝飾
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
    ctx.lineWidth = 1.5;
    ctx.save();
    ctx.translate(250, 175);
    ctx.rotate(Math.PI * 0.05);

    // 邊框
    ctx.strokeRect(-80, -110, 160, 220);

    // 內框裝飾
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
    ctx.lineWidth = 1;
    ctx.strokeRect(-70, -100, 140, 200);

    // 裝飾性線條
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
    ctx.beginPath();
    ctx.moveTo(-50, -80);
    ctx.lineTo(50, -80);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(-50, 80);
    ctx.lineTo(50, 80);
    ctx.stroke();

    // 裝飾性圖案
    drawBookDecoration(ctx, 0, -50, 20);
    drawBookDecoration(ctx, 0, 50, 20);

    ctx.restore();

    // 繪製標題
    ctx.save();
    ctx.translate(250, 175);
    ctx.rotate(Math.PI * 0.05);

    // 主標題
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 28px "Noto Serif TC", serif';
    ctx.textAlign = 'center';
    ctx.fillText('聖經', 0, 0);

    // 繪製光暈效果
    ctx.shadowColor = 'rgba(255, 255, 255, 0.5)';
    ctx.shadowBlur = 15;
    ctx.fillText('聖經', 0, 0);
    ctx.shadowBlur = 0;

    // 副標題
    ctx.font = '16px "Noto Sans TC", sans-serif';
    ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
    ctx.fillText('生命的指引', 0, 30);

    // 小型裝飾
    ctx.font = '16px Arial';
    ctx.fillText('✦  ✦  ✦', 0, 60);
    ctx.restore();

    // 繪製閃亮點效果
    drawSparkle(ctx, 180, 70, 6, '#ffe3a0');
    drawSparkle(ctx, 320, 120, 5, '#ffe3a0');
    drawSparkle(ctx, 200, 250, 4, '#ffe3a0');

    // 繪製裝飾性符號 - 樹葉圖案
    ctx.save();
    ctx.translate(180, 70);
    ctx.rotate(Math.PI * 0.2);
    drawLeaf(ctx, 0, 0, 30, 15, '#ffe3a0');
    ctx.restore();

    ctx.save();
    ctx.translate(350, 280);
    ctx.rotate(Math.PI * -0.3);
    drawLeaf(ctx, 0, 0, 25, 12, '#a0e2ff');
    ctx.restore();

    // 轉為圖片 URL
    var dataUrl = canvas.toDataURL();

    // 將生成的圖像放置在容器中
    var bibleImageElement = $('<img>').addClass('bible-image').attr('src', dataUrl).attr('alt', '聖經文青風格圖像');
    $('.bible-image-container').append(bibleImageElement);

    // 添加裝飾性葉子元素
    $('.bible-image-container').append('<div class="decorative-leaf leaf-1"></div>');
    $('.bible-image-container').append('<div class="decorative-leaf leaf-2"></div>');

    // 添加動畫閃亮效果
    addShinyEffect();
});

// 繪製書本裝飾
function drawBookDecoration(ctx, x, y, size) {
    ctx.beginPath();
    const petals = 6;
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';

    for (let i = 0; i < petals; i++) {
        const angle = (i / petals) * Math.PI * 2;
        const x1 = x + Math.cos(angle) * size;
        const y1 = y + Math.sin(angle) * size;
        ctx.moveTo(x, y);
        ctx.lineTo(x1, y1);
    }

    ctx.stroke();

    // 中心點
    ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
    ctx.beginPath();
    ctx.arc(x, y, size/6, 0, Math.PI * 2);
    ctx.fill();
}

// 繪製簡單的葉子形狀
function drawLeaf(ctx, x, y, width, height, color) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.bezierCurveTo(
        x + width/2, y - height/2,
        x + width, y - height/2,
        x + width, y
    );
    ctx.bezierCurveTo(
        x + width, y + height/2,
        x + width/2, y + height/2,
        x, y
    );
    ctx.fill();
}

// 繪製閃亮效果
function drawSparkle(ctx, x, y, size, color) {
    ctx.save();
    ctx.translate(x, y);

    // 外部光暈
    const gradient = ctx.createRadialGradient(0, 0, 0, 0, 0, size * 2);
    gradient.addColorStop(0, color);
    gradient.addColorStop(1, 'rgba(255, 255, 255, 0)');

    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(0, 0, size * 2, 0, Math.PI * 2);
    ctx.fill();

    // 內部星形
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.beginPath();

    const spikes = 4;
    const innerRadius = size / 4;
    const outerRadius = size;

    for (let i = 0; i < spikes * 2; i++) {
        const radius = i % 2 === 0 ? outerRadius : innerRadius;
        const angle = (Math.PI * 2 * i) / (spikes * 2);
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }

    ctx.closePath();
    ctx.fill();

    ctx.restore();
}

// 添加閃亮效果動畫
function addShinyEffect() {
    const shinyStyles = `
        @keyframes shiny {
            0% { opacity: 0.2; transform: scale(0.8); }
            50% { opacity: 0.9; transform: scale(1.1); }
            100% { opacity: 0.2; transform: scale(0.8); }
        }
    `;

    const styleSheet = document.createElement('style');
    styleSheet.textContent = shinyStyles;
    document.head.appendChild(styleSheet);

    // 添加5個閃亮點元素
    for (let i = 0; i < 5; i++) {
        const shiny = document.createElement('div');
        shiny.className = 'shiny-dot';
        shiny.style.cssText = `
            position: absolute;
            width: 6px;
            height: 6px;
            background: white;
            border-radius: 50%;
            z-index: 2;
            box-shadow: 0 0 10px 2px rgba(255, 227, 160, 0.8);
            animation: shiny ${1.5 + Math.random() * 2}s infinite ease-in-out;
            animation-delay: ${Math.random() * 2}s;
            left: ${10 + Math.random() * 80}%;
            top: ${10 + Math.random() * 80}%;
        `;
        $('.bible-image-container').append(shiny);
    }
}