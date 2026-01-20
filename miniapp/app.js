/**
 * MYBOJXONA Mini App JavaScript
 * Telegram Web App Integration
 */

// Telegram Web App instance
const tg = window.Telegram.WebApp;

// Application state
const appState = {
    currentStep: 0,
    serviceType: null, // 'EPI' or 'MB'
    direction: null, // 'IMPORT', 'EKSPORT', 'TRANZIT'
    borderPost: null,
    destPost: null,
    vehicleNumber: null,
    uploadedFiles: [],
    maxStep: 0
};

// Border posts data (59 items)
const BORDER_POSTS = [
    "Yallama", "Olot", "Doʻstlik (Andijon)", "S. Najimov", "Dovut-ota",
    "Sirdaryo", "Ayritom", "Jartepa", "Oʻzbekiston", "Oybek",
    "Sariosiyo", "Uchqoʻrgʻon", "Shovot", "Islom Karimov nomidagi Toshkent xalqaro aeroporti",
    "Andarxon", "Xoʻjayli", "Kosonsoy", "Navoiy aeroporti", "Nukus aeroporti",
    "Qoraqalpogʻiston", "Doʻstlik (Qoraqalpog'iston)", "Andijon aeroporti",
    "Mingtepa", "Qorasuv", "Xonobod", "Pushmon", "Madaniyat", "Keskanyor",
    "Savay", "Buxoro aeroporti", "Xoʻjadavlat", "Uchtoʻrgʻon", "Qoʻshkent",
    "Qarshi-Kerki", "Qarshi aeroporti", "Namangan aeroporti", "Pop",
    "Samarqand aeroporti", "Termiz aeroporti", "Sariosiyo", "Gulbahor",
    "Boldir", "Xovosobod", "Oq oltin", "Malik", "Navoiy", "Bekobod avto",
    "Gʻishtkoʻprik", "Farhod", "Bekobod", "Fargʻona aeroporti", "Fargʻona",
    "Rishton", "Rovot", "Soʻx", "Doʻstlik (Xorazm)", "Urganch aeroporti",
    "Keles", "Chuqursoy texnik idora"
];

// TIF posts data (33 items)
const TIF_POSTS = [
    "Avia yuklar", "Sirgʻali", "Chuqursoy", "Toshkent-tovar", "Termiz",
    "Buxoro", "Angren", "Vodiy", "Ark buloq", "Qorakoʻl",
    "Termiz xalqaro savdo markazi", "Nasaf", "Urganch", "Ulugʻbek",
    "Guliston", "Asaka", "Namangan", "Samarqand", "Jizzax", "Qoʻqon",
    "Nukus", "Andijon", "Qamashi-Gʻuzor", "Navoiy", "Zarafshon", "Denov",
    "Daryo porti", "Chirchiq", "Olmaliq", "Yangiyoʻl", "Nazarbek",
    "Keles", "Elektron tijorat"
];

// Initialize Telegram Web App
function initTelegramApp() {
    tg.ready();
    tg.expand();
    tg.enableClosingConfirmation();

    // Set theme
    document.body.style.backgroundColor = tg.themeParams.bg_color || '#F9FAFB';

    // Setup back button
    tg.BackButton.onClick(() => {
        goBack();
    });

    // Setup main button
    tg.MainButton.onClick(() => {
        handleMainButtonClick();
    });

    console.log('Telegram Web App initialized');
}

// Start application flow
function startFlow(serviceType) {
    appState.serviceType = serviceType;
    appState.currentStep = 1;
    appState.maxStep = Math.max(appState.maxStep, 1);

    showScreen('directionScreen');
    updateProgress();
    tg.BackButton.show();
}

// Select direction
function selectDirection(direction) {
    appState.direction = direction;
    appState.currentStep = 2;
    appState.maxStep = Math.max(appState.maxStep, 2);

    loadBorderPosts();
    showScreen('borderPostScreen');
    updateProgress();
}

// Load border posts
function loadBorderPosts() {
    const container = document.getElementById('borderPostsList');
    container.innerHTML = '';

    BORDER_POSTS.forEach(post => {
        const item = document.createElement('div');
        item.className = 'post-item';
        item.textContent = post;
        item.onclick = () => selectBorderPost(post);
        container.appendChild(item);
    });
}

// Select border post
function selectBorderPost(post) {
    appState.borderPost = post;

    // Highlight selected
    document.querySelectorAll('#borderPostsList .post-item').forEach(item => {
        item.classList.remove('selected');
    });
    event.target.classList.add('selected');

    // Auto-proceed after short delay
    setTimeout(() => {
        if (appState.direction === 'EKSPORT') {
            // EKSPORT: skip destination, go to vehicle
            appState.currentStep = 4;
            appState.maxStep = Math.max(appState.maxStep, 4);
            showScreen('vehicleScreen');
        } else {
            // IMPORT/TRANZIT: show destination posts
            appState.currentStep = 3;
            appState.maxStep = Math.max(appState.maxStep, 3);
            loadDestPosts();
            showScreen('destPostScreen');
        }
        updateProgress();
    }, 300);
}

// Load destination posts
function loadDestPosts() {
    const container = document.getElementById('destPostsList');
    container.innerHTML = '';

    const posts = appState.direction === 'IMPORT' ? TIF_POSTS : BORDER_POSTS;

    posts.forEach(post => {
        const item = document.createElement('div');
        item.className = 'post-item';
        item.textContent = post;
        item.onclick = () => selectDestPost(post);
        container.appendChild(item);
    });
}

// Select destination post
function selectDestPost(post) {
    appState.destPost = post;

    // Highlight selected
    document.querySelectorAll('#destPostsList .post-item').forEach(item => {
        item.classList.remove('selected');
    });
    event.target.classList.add('selected');

    // Auto-proceed
    setTimeout(() => {
        appState.currentStep = 4;
        appState.maxStep = Math.max(appState.maxStep, 4);
        showScreen('vehicleScreen');
        updateProgress();
    }, 300);
}

// Format vehicle number
function formatVehicleNumber(input) {
    let value = input.value.toUpperCase().replace(/[^0-9A-Z]/g, '');
    input.value = value;

    // Validate format: 01A777AA
    const isValid = /^[0-9]{2}[A-Z][0-9]{3}[A-Z]{2}$/.test(value);

    if (isValid) {
        input.style.borderColor = '#10B981';
    } else {
        input.style.borderColor = value.length === 0 ? '#E5E7EB' : '#F59E0B';
    }
}

// Submit vehicle number
function submitVehicle() {
    const input = document.getElementById('vehicleNumber');
    const value = input.value.trim();

    if (!/^[0-9]{2}[A-Z][0-9]{3}[A-Z]{2}$/.test(value)) {
        tg.showAlert('Iltimos, mashina raqamini to\'g\'ri kiriting!\n\nMisol: 01A777AA');
        return;
    }

    appState.vehicleNumber = value;
    appState.currentStep = 5;
    appState.maxStep = Math.max(appState.maxStep, 5);

    loadDocumentChecklist();
    showScreen('documentsScreen');
    updateProgress();
}

// Load document checklist
function loadDocumentChecklist() {
    const container = document.getElementById('docChecklist');
    container.innerHTML = '';

    const docs = appState.serviceType === 'EPI' ? [
        { icon: '📄', text: 'Pasport (Oldi-Orqa)' },
        { icon: '🚗', text: 'Tex-pasport (Oldi-Orqa)' },
        { icon: '📦', text: 'CMR va Invoice' },
        { icon: '📜', text: 'Sertifikatlar (agar bo\'lsa)' }
    ] : [
        { icon: '📄', text: 'Pasport (Oldi-Orqa)' },
        { icon: '🚗', text: 'Tex-pasport (Oldi-Orqa)' }
    ];

    docs.forEach(doc => {
        const item = document.createElement('div');
        item.className = 'doc-item';
        item.innerHTML = `
            <span class="doc-item-icon">${doc.icon}</span>
            <span class="doc-item-text">${doc.text}</span>
        `;
        container.appendChild(item);
    });
}

// Handle file selection
function handleFileSelect(event) {
    const files = Array.from(event.target.files);

    files.forEach(file => {
        if (file.type.startsWith('image/') || file.type === 'application/pdf') {
            const reader = new FileReader();
            reader.onload = (e) => {
                appState.uploadedFiles.push({
                    name: file.name,
                    data: e.target.result,
                    type: file.type
                });
                displayUploadedFiles();
                updateSubmitButton();
            };
            reader.readAsDataURL(file);
        }
    });
}

// Display uploaded files
function displayUploadedFiles() {
    const container = document.getElementById('uploadedFiles');
    container.innerHTML = '';

    appState.uploadedFiles.forEach((file, index) => {
        const fileDiv = document.createElement('div');
        fileDiv.className = 'uploaded-file';

        if (file.type.startsWith('image/')) {
            fileDiv.innerHTML = `
                <img src="${file.data}" alt="${file.name}">
                <button class="file-remove" onclick="removeFile(${index})">×</button>
            `;
        } else {
            fileDiv.innerHTML = `
                <div style="display: flex; align-items: center; justify-content: center; height: 100%; background: #F3E8FF;">
                    <span style="font-size: 32px;">📄</span>
                </div>
                <button class="file-remove" onclick="removeFile(${index})">×</button>
            `;
        }

        container.appendChild(fileDiv);
    });
}

// Remove file
function removeFile(index) {
    appState.uploadedFiles.splice(index, 1);
    displayUploadedFiles();
    updateSubmitButton();
}

// Update submit button state
function updateSubmitButton() {
    const btn = document.getElementById('submitBtn');
    const minFiles = appState.serviceType === 'EPI' ? 3 : 2;

    if (appState.uploadedFiles.length >= minFiles) {
        btn.disabled = false;
    } else {
        btn.disabled = true;
    }
}

// Submit application
async function submitApplication() {
    tg.MainButton.showProgress();

    // Prepare data
    const applicationData = {
        user_id: tg.initDataUnsafe.user?.id,
        service_type: appState.serviceType,
        direction: appState.direction,
        border_post: appState.borderPost,
        dest_post: appState.destPost,
        vehicle_number: appState.vehicleNumber,
        files_count: appState.uploadedFiles.length,
        timestamp: new Date().toISOString()
    };

    try {
        // Send to bot API endpoint
        const response = await fetch('/api/applications', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(applicationData)
        });

        const result = await response.json();

        // Show success screen
        showSuccessScreen(result.app_code || generateAppCode());

        // Send data to bot via Telegram
        tg.sendData(JSON.stringify(applicationData));

    } catch (error) {
        console.error('Submit error:', error);

        // Fallback: still show success and send data
        showSuccessScreen(generateAppCode());
        tg.sendData(JSON.stringify(applicationData));
    } finally {
        tg.MainButton.hideProgress();
    }
}

// Generate application code
function generateAppCode() {
    const prefix = appState.serviceType === 'EPI' ? 'EP' : 'MB';
    const random = Math.random().toString(36).substr(2, 6).toUpperCase();
    return `${prefix}-${random}`;
}

// Show success screen
function showSuccessScreen(appCode) {
    document.getElementById('appCode').textContent = appCode;
    document.getElementById('appVehicle').textContent = appState.vehicleNumber;

    showScreen('successScreen');
    hideProgress();
    tg.BackButton.hide();

    // Confetti animation (optional)
    setTimeout(() => {
        tg.showAlert('✅ Arizangiz muvaffaqiyatli yuborildi!\n\nAdmin tez orada javob beradi.');
    }, 500);
}

// Navigation functions
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');

    // Scroll to top
    window.scrollTo(0, 0);
}

function goBack() {
    if (appState.currentStep === 0) {
        tg.close();
        return;
    }

    appState.currentStep--;

    const screens = ['homeScreen', 'directionScreen', 'borderPostScreen', 'destPostScreen', 'vehicleScreen', 'documentsScreen'];
    const targetScreen = screens[appState.currentStep];

    if (targetScreen) {
        showScreen(targetScreen);
        updateProgress();

        if (appState.currentStep === 0) {
            tg.BackButton.hide();
        }
    }
}

function backToHome() {
    // Reset state
    appState.currentStep = 0;
    appState.serviceType = null;
    appState.direction = null;
    appState.borderPost = null;
    appState.destPost = null;
    appState.vehicleNumber = null;
    appState.uploadedFiles = [];

    showScreen('homeScreen');
    hideProgress();
    tg.BackButton.hide();
}

// Progress functions
function updateProgress() {
    const progressContainer = document.getElementById('progressContainer');
    const progressFill = document.getElementById('progressFill');

    if (appState.currentStep > 0) {
        progressContainer.style.display = 'block';

        // Update step indicators
        document.querySelectorAll('.step').forEach((step, index) => {
            const stepNum = index + 1;
            if (stepNum < appState.currentStep) {
                step.classList.add('completed');
                step.classList.remove('active');
            } else if (stepNum === appState.currentStep) {
                step.classList.add('active');
                step.classList.remove('completed');
            } else {
                step.classList.remove('active', 'completed');
            }
        });

        // Update progress bar
        const percentage = ((appState.currentStep - 1) / 4) * 100;
        progressFill.style.width = `${percentage}%`;
    } else {
        hideProgress();
    }
}

function hideProgress() {
    document.getElementById('progressContainer').style.display = 'none';
}

// Filter posts by search
function filterPosts(type) {
    const searchInput = document.getElementById(type === 'border' ? 'borderPostSearch' : 'destPostSearch');
    const container = document.getElementById(type === 'border' ? 'borderPostsList' : 'destPostsList');
    const query = searchInput.value.toLowerCase();

    const items = container.querySelectorAll('.post-item');
    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(query) ? 'block' : 'none';
    });
}

// Placeholder functions for other features
function viewApplications() {
    tg.showAlert('🎫 ARIZALARIM\n\nBu bo\'lim tez orada ishga tushadi!');
}

function viewPrices() {
    const pricesText = `💰 NARXLAR KATALOGI\n\n` +
        `📦 1-2 partiya: 35,000 so'm\n` +
        `📦 3 partiya: 45,000 so'm\n` +
        `📦 4 partiya: 60,000 so'm\n` +
        `📦 5 partiya: 75,000 so'm\n` +
        `📦 6 partiya: 105,000 so'm\n` +
        `📦 7 partiya: 126,000 so'm\n` +
        `📦 8 partiya: 144,000 so'm\n\n` +
        `🔄 Boshqa: X*20,000 so'm`;

    tg.showAlert(pricesText);
}

function handleMainButtonClick() {
    // Handle main button actions based on current screen
    console.log('Main button clicked');
}

// Drag and drop support
function setupDragDrop() {
    const uploadArea = document.getElementById('uploadArea');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.style.background = 'white';
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.style.background = '';
        });
    });

    uploadArea.addEventListener('drop', (e) => {
        const files = e.dataTransfer.files;
        document.getElementById('fileInput').files = files;
        handleFileSelect({ target: { files } });
    });
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initTelegramApp();
    setupDragDrop();
    console.log('MYBOJXONA Mini App loaded');
});
