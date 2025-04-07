// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 图片上传预览
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
        input.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    // 查找最近的预览容器
                    const previewContainer = input.parentElement.querySelector('.image-preview');
                    
                    if (previewContainer) {
                        // 如果已有预览容器，更新它
                        const img = previewContainer.querySelector('img');
                        img.src = e.target.result;
                    } else {
                        // 否则创建新的预览容器
                        const preview = document.createElement('div');
                        preview.className = 'image-preview mt-2';
                        
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.className = 'img-fluid rounded';
                        img.style.maxHeight = '200px';
                        
                        preview.appendChild(img);
                        input.parentElement.appendChild(preview);
                    }
                };
                
                reader.readAsDataURL(file);
            }
        });
    });
    
    // 表单提交时显示加载动画
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            // 检查是否已有加载动画
            let loadingElement = form.querySelector('.loading');
            
            if (!loadingElement) {
                // 创建加载动画
                loadingElement = document.createElement('div');
                loadingElement.className = 'loading mt-3';
                
                const spinner = document.createElement('div');
                spinner.className = 'loading-spinner';
                
                const text = document.createElement('p');
                text.className = 'mt-2';
                text.textContent = '处理中，请稍候...';
                
                loadingElement.appendChild(spinner);
                loadingElement.appendChild(text);
                
                // 添加到表单底部
                form.appendChild(loadingElement);
            }
            
            // 显示加载动画
            loadingElement.style.display = 'block';
            
            // 禁用提交按钮
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> 处理中...';
            }
        });
    });
    
    // 图像对比滑块（如果存在）
    const imageCompareSliders = document.querySelectorAll('.image-compare-slider');
    
    imageCompareSliders.forEach(slider => {
        slider.addEventListener('input', function() {
            const beforeImage = this.parentElement.querySelector('.before-image');
            const afterImage = this.parentElement.querySelector('.after-image');
            
            if (beforeImage && afterImage) {
                afterImage.style.clipPath = `inset(0 0 0 ${this.value}%)`;
            }
        });
    });
});
