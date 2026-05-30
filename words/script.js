let wordsList = [];
let currentIdx = 0;
let autoPlaying = false;
let autoTimer = null;
let speechSynth = window.speechSynthesis;

const fileSelect = document.getElementById('fileSelect');
const wordListDiv = document.getElementById('wordList');
const currentWordSpan = document.getElementById('currentWord');
const definitionDiv = document.getElementById('wordDefinition');
const progressFill = document.getElementById('progressFill');
const progressTextSpan = document.getElementById('progressText');
const voiceSelect = document.getElementById('voiceSelect');
const rateRange = document.getElementById('rateRange');
const rateValueSpan = document.getElementById('rateValue');
const intervalRange = document.getElementById('intervalRange');
const intervalValueSpan = document.getElementById('intervalValue');
const statusDiv = document.getElementById('status');
const refreshBtn = document.getElementById('refreshBtn');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const speakBtn = document.getElementById('speakBtn');
const autoPlayBtn = document.getElementById('autoPlayBtn');
const wordCard = document.getElementById('wordCard');

function showStatus(msg, type = 'loading') {
    statusDiv.textContent = msg;
    statusDiv.className = `status ${type}`;
    statusDiv.classList.remove('hidden');
    setTimeout(() => statusDiv.classList.add('hidden'), 2000);
}

function shuffleArray(arr) {
    const newArr = [...arr];
    for (let i = newArr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [newArr[i], newArr[j]] = [newArr[j], newArr[i]];
    }
    return newArr;
}

function renderWordList() {
    if (!wordsList.length) {
        wordListDiv.innerHTML = '<p style="text-align:center; color:#94a3b8; padding: 40px;">请选择词库</p>';
        return;
    }
    const fragment = document.createDocumentFragment();
    wordsList.forEach((item, idx) => {
        const div = document.createElement('div');
        div.className = 'word-item' + (idx === currentIdx ? ' active' : '');
        div.dataset.index = idx;
        div.textContent = `${idx + 1}. ${item.word}`;
        fragment.appendChild(div);
    });
    wordListDiv.innerHTML = '';
    wordListDiv.appendChild(fragment);
}

function updateDisplay() {
    if (!wordsList.length) return;
    const wordObj = wordsList[currentIdx];
    currentWordSpan.textContent = wordObj.word;
    definitionDiv.textContent = wordObj.definition;

    const percent = ((currentIdx + 1) / wordsList.length) * 100;
    progressFill.style.width = `${percent}%`;
    progressTextSpan.textContent = `${currentIdx + 1} / ${wordsList.length}`;

    const items = wordListDiv.querySelectorAll('.word-item');
    items.forEach((item, idx) => {
        item.classList.toggle('active', idx === currentIdx);
    });

    const activeItem = wordListDiv.querySelector('.word-item.active');
    if (activeItem) {
        activeItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

function cancelSpeech() {
    if (speechSynth) {
        speechSynth.cancel();
    }
}

function speakCurrentWord() {
    if (!wordsList.length) {
        showStatus('请先选择词库', 'error');
        return;
    }
    cancelSpeech();
    const wordText = wordsList[currentIdx].word;

    let voices = speechSynth.getVoices();
    if (!voices.length) {
        setTimeout(() => {
            voices = speechSynth.getVoices();
            doSpeak(wordText, voices);
        }, 100);
        return;
    }
    doSpeak(wordText, voices);
}

function doSpeak(text, voices) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = parseFloat(rateRange.value);
    utterance.pitch = 1;
    utterance.lang = 'en-US';

    let selectedVoice = null;
    const selectedIdx = voiceSelect.value;
    if (selectedIdx && voices[parseInt(selectedIdx)]) {
        selectedVoice = voices[parseInt(selectedIdx)];
    } else {
        const preferredNames = ['Google US English', 'Google UK English', 'Samantha', 'Microsoft Zira', 'Alex', 'Microsoft David'];
        for (let name of preferredNames) {
            const found = voices.find(v => v.name.includes(name) && v.lang.startsWith('en'));
            if (found) {
                selectedVoice = found;
                break;
            }
        }
        if (!selectedVoice) {
            const englishVoice = voices.find(v => v.lang.startsWith('en'));
            if (englishVoice) selectedVoice = englishVoice;
        }
    }
    if (selectedVoice) utterance.voice = selectedVoice;

    try {
        speechSynth.speak(utterance);
    } catch (err) {
        console.error('speak error', err);
    }
}

function nextWord() {
    if (!wordsList.length) return;
    cancelSpeech();
    currentIdx = (currentIdx + 1) % wordsList.length;
    updateDisplay();
    speakCurrentWord();
}

function prevWord() {
    if (!wordsList.length) return;
    cancelSpeech();
    currentIdx = (currentIdx - 1 + wordsList.length) % wordsList.length;
    updateDisplay();
    speakCurrentWord();
}

function startAutoPlay() {
    if (autoTimer) clearInterval(autoTimer);
    autoPlaying = true;
    autoPlayBtn.textContent = '⏸️ 停止';
    autoPlayBtn.classList.add('danger');
    speakCurrentWord();
    autoTimer = setInterval(() => {
        if (autoPlaying && wordsList.length) {
            cancelSpeech();
            currentIdx = (currentIdx + 1) % wordsList.length;
            updateDisplay();
            speakCurrentWord();
        }
    }, parseFloat(intervalRange.value) * 1000);
}

function stopAutoPlay() {
    if (autoTimer) {
        clearInterval(autoTimer);
        autoTimer = null;
    }
    autoPlaying = false;
    autoPlayBtn.textContent = '▶ 自动播放';
    autoPlayBtn.classList.remove('danger');
    cancelSpeech();
}

function toggleAutoPlay() {
    if (!wordsList.length) {
        showStatus('请先选择词库', 'error');
        return;
    }
    if (autoPlaying) {
        stopAutoPlay();
    } else {
        startAutoPlay();
    }
}

function loadWordBank(filename) {
    if (!filename) return;
    showStatus(`📖 加载 ${filename} 中...`, 'loading');

    wordsList = [];

    fetch(filename)
        .then(response => {
            if (!response.ok && window.location.protocol !== 'file:') {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(text => {
            const lines = text.split('\n');
            const wordObjects = [];

            for (const line of lines) {
                const trimmedLine = line.trim();
                if (trimmedLine) {
                    const parts = trimmedLine.split('\t');
                    if (parts.length >= 2) {
                        const word = parts[0].trim();
                        const definition = parts.slice(1).join('\t').trim();
                        if (word) {
                            wordObjects.push({ word, definition });
                        }
                    }
                }
            }

            if (wordObjects.length === 0) {
                throw new Error('词库文件为空或格式错误');
            }

            wordsList = shuffleArray(wordObjects);
            currentIdx = 0;

            updateDisplay();
            renderWordList();

            cancelSpeech();

            showStatus(`✅ 成功加载 ${wordsList.length} 个单词`, 'success');
        })
        .catch(err => {
            console.error('加载词库失败:', err);
            showStatus(`❌ 加载失败: ${err.message}`, 'error');
            wordListDiv.innerHTML = '<p style="text-align:center; color:#94a3b8; padding: 40px;">请使用HTTP服务器访问</p>';
        });
}

function populateVoiceList() {
    const voices = speechSynth.getVoices();
    const enVoices = voices.filter(v => v.lang.startsWith('en'));

    voiceSelect.innerHTML = '';
    if (!enVoices.length) {
        const opt = document.createElement('option');
        opt.value = '';
        opt.textContent = '默认英语语音';
        voiceSelect.appendChild(opt);
    } else {
        enVoices.forEach((voice, idx) => {
            const option = document.createElement('option');
            option.value = voices.indexOf(voice);
            option.textContent = `${voice.name} (${voice.lang})`;
            voiceSelect.appendChild(option);
        });
    }
}

fileSelect.addEventListener('change', () => {
    if (autoPlaying) stopAutoPlay();
    loadWordBank(fileSelect.value);
});

refreshBtn.addEventListener('click', () => {
    if (!fileSelect.value) {
        showStatus('请先选择词库', 'error');
        return;
    }
    if (autoPlaying) stopAutoPlay();
    loadWordBank(fileSelect.value);
});

prevBtn.addEventListener('click', () => {
    if (autoPlaying) stopAutoPlay();
    prevWord();
});

nextBtn.addEventListener('click', () => {
    if (autoPlaying) stopAutoPlay();
    nextWord();
});

speakBtn.addEventListener('click', () => {
    if (autoPlaying) stopAutoPlay();
    speakCurrentWord();
});

autoPlayBtn.addEventListener('click', toggleAutoPlay);

wordCard.addEventListener('click', () => {
    if (autoPlaying) stopAutoPlay();
    speakCurrentWord();
});

rateRange.addEventListener('input', () => {
    rateValueSpan.textContent = parseFloat(rateRange.value).toFixed(1);
});

intervalRange.addEventListener('input', () => {
    intervalValueSpan.textContent = parseFloat(intervalRange.value).toFixed(1) + '秒';
    if (autoPlaying) {
        stopAutoPlay();
        startAutoPlay();
    }
});

wordListDiv.addEventListener('click', (e) => {
    const wordItem = e.target.closest('.word-item');
    if (wordItem && wordItem.dataset.index !== undefined) {
        if (autoPlaying) stopAutoPlay();
        currentIdx = parseInt(wordItem.dataset.index);
        updateDisplay();
        speakCurrentWord();
    }
});

document.addEventListener('keydown', (e) => {
    const tag = e.target.tagName;
    if (tag === 'SELECT' || tag === 'INPUT') return;

    if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (autoPlaying) stopAutoPlay();
        prevWord();
    } else if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (autoPlaying) stopAutoPlay();
        nextWord();
    } else if (e.key === ' ' || e.key === 'Space') {
        e.preventDefault();
        toggleAutoPlay();
    }
});

if (speechSynth.onvoiceschanged !== undefined) {
    speechSynth.onvoiceschanged = populateVoiceList;
}
populateVoiceList();
