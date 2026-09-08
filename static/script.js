async function polish() {
    const input = document.getElementById('input').value.trim();
    // 获取用户输入、当前场景和页面上的结果区域。
    const scene = document.getElementById('scene').value;
    const resultDiv = document.getElementById('result');
    const originalDiv = document.getElementById('original');
    const btn = document.getElementById('polishBtn');

    if (!input) {
        alert('请先输入要润色的英文文本！');
        return;
    }

    // 输入为空时不发送请求。
    btn.disabled = true;
    btn.textContent = '润色中...';
    resultDiv.className = 'result-content loading';
    resultDiv.textContent = 'AI 正在润色，请稍候...';

    try {
        // 调用 Flask 后端，将文本和润色场景转换为 JSON 发送。
        const response = await fetch('/polish', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: input,
                scene: scene
            })
        });

        const data = await response.json();

        // 后端返回错误时直接显示错误信息。
        if (data.error) {
            resultDiv.textContent = '错误：' + data.error;
        } else {
            // 显示原文
            originalDiv.className = 'original-content';
            originalDiv.textContent = input;
            // 显示润色结果
            resultDiv.className = 'result-content';
            resultDiv.textContent = data.result;
            // 清空输入框
            document.getElementById('input').value = '';
        }
    } catch (err) {
        // 网络错误通常表示后端没有启动或接口地址不可用。
        resultDiv.className = 'result-content';
        resultDiv.textContent = '请求失败：' + err.message + '\n\n请确认后端服务已启动（python app.py）';
    }

    // 无论请求成功还是失败，都恢复按钮状态。
    btn.disabled = false;
    btn.textContent = '润色';
}