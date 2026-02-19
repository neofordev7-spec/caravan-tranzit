/**
 * CARAVAN TRANZIT Mini App - JavaScript
 * Version: 3.0
 * Telegram Web App Integration with i18n
 */

// ==================== TELEGRAM WEB APP ====================
const tg = window.Telegram?.WebApp;

// ==================== APP STATE ====================
const AppState = {
    currentScreen: 'splashScreen',
    previousScreens: [],
    language: localStorage.getItem('caravan_lang') || 'uz',
    serviceType: null, // 'EPI' or 'MB'
    selectedPost: null,
    selectedAgent: null,
    vehicleNumber: null,
    vehicleType: 'truck',
    selectedDestination: null,
    uploadedFiles: [],
    userCoins: 35000,
    userId: null,
    userName: null,
    userPhone: null,
    isInitialized: false
};

// ==================== DATA ====================
const BORDER_POSTS = [
    "Oybek", "Yallama", "Olot", "Dustlik (Andijon)", "S. Najimov",
    "Dovut-ota", "Sirdaryo", "Ayritom", "Jartepa", "Ozbekiston",
    "Sariosiyo", "Uchqorgon", "Shovot", "Toshkent aeroporti",
    "Andarxon", "Xojayli", "Kosonsoy", "Navoiy aeroporti",
    "Nukus aeroporti", "Qoraqalpogiston", "Dustlik (Qoraqalpog'iston)",
    "Andijon aeroporti", "Mingtepa", "Qorasuv", "Xonobod",
    "Pushmon", "Madaniyat", "Keskanyor", "Savay", "Buxoro aeroporti",
    "Xojadavlat", "Uchtorgon", "Qoshkent", "Qarshi-Kerki",
    "Qarshi aeroporti", "Namangan aeroporti", "Pop", "Samarqand aeroporti",
    "Termiz aeroporti", "Gulbahor", "Boldir", "Xovosobod",
    "Oq oltin", "Malik", "Navoiy", "Bekobod avto", "Gishtko'prik",
    "Farhod", "Bekobod", "Fargona aeroporti", "Fargona", "Rishton",
    "Rovot", "Sox", "Dustlik (Xorazm)", "Urganch aeroporti",
    "Keles", "Chuqursoy texnik idora"
];

const TIF_POSTS = [
    "Toshkent TIF", "Sirgali", "Chuqursoy", "Toshkent-tovar",
    "Termiz TIF", "Buxoro TIF", "Angren", "Vodiy", "Ark buloq",
    "Qorakol", "Termiz xalqaro savdo markazi", "Nasaf", "Urganch",
    "Ulugbek", "Guliston", "Asaka", "Namangan", "Samarqand",
    "Jizzax", "Qoqon", "Nukus", "Andijon", "Qamashi-Guzor",
    "Navoiy TIF", "Zarafshon", "Denov", "Daryo porti", "Chirchiq",
    "Olmaliq", "Yangiyol", "Nazarbek", "Keles", "Elektron tijorat"
];

// Popular border posts (no images)
const POPULAR_POSTS = [
    { name: 'Yallama', region: 'Toshkent viloyati' },
    { name: 'Olot', region: 'Buxoro viloyati' },
    { name: "Do'stlik", region: 'Andijon viloyati' }
];

// Agent selection removed - not needed for now

// ==================== INITIALIZATION ====================
document.addEventListener('DOMContentLoaded', () => {
    initTelegramApp();
    initApp();
});

function initTelegramApp() {
    if (tg) {
        tg.ready();
        tg.expand();
        tg.enableClosingConfirmation();

        // Get user data from Telegram
        if (tg.initDataUnsafe?.user) {
            AppState.userId = tg.initDataUnsafe.user.id;
            AppState.userName = tg.initDataUnsafe.user.first_name + ' ' + (tg.initDataUnsafe.user.last_name || '');

            // Try to get language from Telegram
            const tgLang = tg.initDataUnsafe.user.language_code;
            if (tgLang && !localStorage.getItem('caravan_lang')) {
                const langMap = { 'uz': 'uz', 'ru': 'ru', 'en': 'en', 'zh': 'zh', 'tr': 'tr', 'kk': 'kk', 'ky': 'ky', 'tg': 'tj', 'tk': 'tk' };
                if (langMap[tgLang]) {
                    AppState.language = langMap[tgLang];
                    localStorage.setItem('caravan_lang', langMap[tgLang]);
                }
            }
        }

        // Set theme colors
        document.body.style.backgroundColor = tg.themeParams.bg_color || '#F5F7FA';

        // Back button handler
        tg.BackButton.onClick(() => goBack());

        // Main button handler
        tg.MainButton.onClick(() => handleMainButton());

        console.log('Telegram Web App initialized');
    }
}

function initApp() {
    // Set default language if not set
    if (!AppState.language) {
        AppState.language = 'uz';
        localStorage.setItem('caravan_lang', 'uz');
    }

    // Set language in i18n
    if (typeof setLanguage === 'function') {
        setLanguage(AppState.language);
    }

    // Show main app immediately - no splash, no delays
    showMainApp();

    // Setup event listeners
    setupEventListeners();

    // Update UI texts
    updateAllUITexts();

    // Load saved data
    loadSavedData();

    AppState.isInitialized = true;
}

function setupEventListeners() {
    // Header back button
    document.getElementById('headerBackBtn')?.addEventListener('click', () => goBack());

    // Profile button
    document.getElementById('profileBtn')?.addEventListener('click', () => {
        navigateTo('settingsScreen');
    });

    // Listen for language changes
    document.addEventListener('languageChanged', () => {
        updateAllUITexts();
    });
}

function loadSavedData() {
    // Load recent vehicle
    const recentVehicle = localStorage.getItem('caravan_recent_vehicle');
    if (recentVehicle) {
        const recentEl = document.getElementById('recentVehicles');
        if (recentEl) {
            recentEl.innerHTML = `
                <div class="recent-item" onclick="useRecentVehicle('${recentVehicle}')">
                    <span class="recent-icon">🔄</span>
                    <span class="recent-text">${t('previous_vehicle')}: <strong>${recentVehicle}</strong></span>
                    <span class="recent-hint">(${t('last_used')})</span>
                </div>
            `;
        }
    }

    // Load user balance (would come from API in production)
    const savedBalance = localStorage.getItem('caravan_balance');
    if (savedBalance) {
        AppState.userCoins = parseInt(savedBalance);
    }
    updateCoinsDisplay();
}

// ==================== UI TEXT UPDATES ====================
function updateAllUITexts() {
    // Update home screen
    updateElement('walletLabel', t('my_coins'));
    updateElement('walletCurrency', t('uzs_equivalent'));
    updateElement('servicesTitle', t('services'));
    updateElement('recentAppsTitle', t('recent_apps'));

    // Update navigation
    document.querySelectorAll('.nav-label-new').forEach((el, index) => {
        const labels = ['nav_home', 'nav_map', '', 'nav_history', 'nav_profile'];
        if (labels[index]) {
            el.textContent = t(labels[index]);
        }
    });

    // Update service cards
    const serviceNames = document.querySelectorAll('.service-name-new');
    const serviceKeys = ['epi_service', 'mb_service', 'kgd_service', 'my_apps', 'bonus', 'prices'];
    serviceNames.forEach((el, index) => {
        if (serviceKeys[index]) {
            el.textContent = t(serviceKeys[index]);
        }
    });

    // Update current language display
    const langInfo = typeof getLanguageInfo === 'function' ? getLanguageInfo(AppState.language) : null;
    if (langInfo) {
        updateElement('currentLang', langInfo.native);
    }

    // Update settings screen
    updateElement('phoneLabel', t('phone'));
    updateElement('languageLabel', t('language'));
}

function updateElement(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
}

function updateCoinsDisplay() {
    const coinsEl = document.getElementById('coinsValue');
    if (coinsEl) {
        coinsEl.textContent = formatNumber(AppState.userCoins);
    }

    const bonusCoinsEl = document.getElementById('bonusCoins');
    if (bonusCoinsEl) {
        bonusCoinsEl.textContent = formatNumber(AppState.userCoins);
    }
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// ==================== LANGUAGE ====================
function selectLanguage(lang) {
    AppState.language = lang;
    localStorage.setItem('caravan_lang', lang);

    if (typeof setLanguage === 'function') {
        setLanguage(lang);
    }

    // Haptic feedback
    if (tg) tg.HapticFeedback?.impactOccurred('light');

    updateAllUITexts();
    showLanguageModal(false);
}

function showLanguageModal(show = true) {
    let modal = document.getElementById('languageModal');

    if (show) {
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'languageModal';
            modal.className = 'modal-overlay';
            modal.innerHTML = `
                <div class="modal-content">
                    <div class="modal-header">
                        <h3>${t('language')}</h3>
                        <button class="modal-close" onclick="showLanguageModal(false)">×</button>
                    </div>
                    <div class="language-list">
                        ${getAvailableLanguages().map(lang => `
                            <button class="language-option ${lang.code === AppState.language ? 'active' : ''}"
                                    onclick="selectLanguage('${lang.code}')">
                                <span class="lang-flag">${lang.flag}</span>
                                <span class="lang-name">${lang.native}</span>
                                ${lang.code === AppState.language ? '<span class="lang-check">✓</span>' : ''}
                            </button>
                        `).join('')}
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }
        modal.style.display = 'flex';
        if (tg) tg.HapticFeedback?.impactOccurred('light');
    } else if (modal) {
        modal.style.display = 'none';
    }
}

function changeLanguage() {
    showLanguageModal(true);
}

// ==================== NAVIGATION ====================
function showScreen(screenId) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });

    // Show target screen
    const targetScreen = document.getElementById(screenId);
    if (targetScreen) {
        targetScreen.classList.add('active');
        AppState.currentScreen = screenId;

        // Scroll to top
        window.scrollTo(0, 0);
    }

    // Update back button visibility
    updateBackButton();
}

function showMainApp() {
    // Show home screen immediately
    navigateTo('homeScreen');
}

function navigateTo(screenId) {
    // Save previous screen for back navigation
    if (AppState.currentScreen && AppState.currentScreen !== screenId) {
        AppState.previousScreens.push(AppState.currentScreen);
    }

    // Hide all screens in main
    document.querySelectorAll('#appMain .screen').forEach(screen => {
        screen.classList.remove('active');
    });

    // Show target screen
    const targetScreen = document.getElementById(screenId);
    if (targetScreen) {
        targetScreen.classList.add('active');
        AppState.currentScreen = screenId;
    }

    // Update bottom nav active state
    updateBottomNav(screenId);
    updateBackButton();

    // Scroll to top
    window.scrollTo(0, 0);

    // Haptic feedback
    if (tg) tg.HapticFeedback?.impactOccurred('light');
}

function updateBottomNav(screenId) {
    document.querySelectorAll('.nav-item-new').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.screen === screenId) {
            item.classList.add('active');
        }
    });
}

function updateBackButton() {
    const backBtn = document.getElementById('headerBackBtn');
    const mainScreens = ['homeScreen', 'applicationsScreen', 'chatScreen', 'bonusScreen', 'settingsScreen'];

    if (backBtn) {
        if (mainScreens.includes(AppState.currentScreen)) {
            backBtn.style.display = 'none';
            if (tg) tg.BackButton.hide();
        } else {
            backBtn.style.display = 'flex';
            if (tg) tg.BackButton.show();
        }
    }
}

function goBack() {
    if (AppState.previousScreens.length > 0) {
        const previousScreen = AppState.previousScreens.pop();
        navigateTo(previousScreen);
    } else {
        navigateTo('homeScreen');
    }

    if (tg) tg.HapticFeedback?.impactOccurred('light');
}

function goHome() {
    AppState.previousScreens = [];
    navigateTo('homeScreen');
    resetFlowState();
}

function resetFlowState() {
    AppState.serviceType = null;
    AppState.selectedPost = null;
    AppState.selectedAgent = null;
    AppState.vehicleNumber = null;
    AppState.selectedDestination = null;
    AppState.uploadedFiles = [];
}

// ==================== EPI/MB FLOW ====================
function startEPIFlow() {
    AppState.serviceType = 'EPI';
    loadBorderPosts();
    navigateTo('borderPostScreen');
}

function startMBFlow() {
    AppState.serviceType = 'MB';
    loadBorderPosts();
    navigateTo('borderPostScreen');
}

function loadBorderPosts() {
    // Load popular posts
    loadPopularPosts();

    // Load alphabetically grouped posts
    loadGroupedPosts();
}

// Load popular posts (simple list, no images)
function loadPopularPosts() {
    const container = document.getElementById('popularPostsContainer');
    if (!container) return;

    container.innerHTML = '';

    POPULAR_POSTS.forEach(post => {
        const card = document.createElement('div');
        card.className = 'popular-post-card';
        card.innerHTML = `
            <div class="popular-post-simple">
                <h4 class="popular-post-name">${post.name}</h4>
                <p class="popular-post-region">${post.region}</p>
            </div>
        `;
        card.onclick = () => selectBorderPost(post.name);
        container.appendChild(card);
    });
}

// Load posts grouped alphabetically
function loadGroupedPosts() {
    const container = document.getElementById('borderPostsList');
    if (!container) return;

    container.innerHTML = '';

    // Sort posts alphabetically
    const sortedPosts = [...BORDER_POSTS].sort((a, b) => a.localeCompare(b, 'uz'));

    // Group by first letter
    const groups = {};
    sortedPosts.forEach(post => {
        const firstLetter = post.charAt(0).toUpperCase();
        if (!groups[firstLetter]) {
            groups[firstLetter] = [];
        }
        groups[firstLetter].push(post);
    });

    // Render grouped posts
    Object.keys(groups).sort().forEach(letter => {
        // Letter header
        const letterHeader = document.createElement('div');
        letterHeader.className = 'post-letter-header';
        letterHeader.textContent = letter;
        container.appendChild(letterHeader);

        // Posts in this group
        groups[letter].forEach(post => {
            const item = document.createElement('div');
            item.className = 'post-item-grouped';
            item.innerHTML = `
                <div class="post-item-info">
                    <span class="post-item-name">${post}</span>
                </div>
                <span class="post-item-arrow">›</span>
            `;
            item.onclick = () => selectBorderPost(post);
            container.appendChild(item);
        });
    });
}

// Search/filter border posts
function filterBorderPosts(query) {
    const lowerQuery = query.toLowerCase().trim();

    // Filter popular posts
    const popularContainer = document.getElementById('popularPostsContainer');
    if (popularContainer) {
        const popularCards = popularContainer.querySelectorAll('.popular-post-card');
        popularCards.forEach(card => {
            const name = card.querySelector('.popular-post-name')?.textContent.toLowerCase() || '';
            card.style.display = name.includes(lowerQuery) || !lowerQuery ? 'block' : 'none';
        });

        // Hide popular section title if all cards are hidden
        const popularSection = document.querySelector('.popular-posts-section');
        if (popularSection) {
            const visibleCards = popularContainer.querySelectorAll('.popular-post-card[style*="display: block"], .popular-post-card:not([style*="display"])');
            popularSection.style.display = lowerQuery && visibleCards.length === 0 ? 'none' : 'block';
        }
    }

    // Filter grouped posts
    const listContainer = document.getElementById('borderPostsList');
    if (listContainer) {
        const items = listContainer.querySelectorAll('.post-item-grouped');
        const letterHeaders = listContainer.querySelectorAll('.post-letter-header');

        // Track which letters have visible items
        const visibleLetters = new Set();

        items.forEach(item => {
            const name = item.querySelector('.post-item-name')?.textContent.toLowerCase() || '';
            const isVisible = name.includes(lowerQuery) || !lowerQuery;
            item.style.display = isVisible ? 'flex' : 'none';

            if (isVisible) {
                // Find the letter for this item
                const letter = name.charAt(0).toUpperCase();
                visibleLetters.add(letter);
            }
        });

        // Show/hide letter headers
        letterHeaders.forEach(header => {
            const letter = header.textContent;
            header.style.display = visibleLetters.has(letter) || !lowerQuery ? 'block' : 'none';
        });
    }
}

function selectBorderPost(post) {
    AppState.selectedPost = post;

    if (tg) tg.HapticFeedback?.impactOccurred('medium');

    // Skip agent selection - go directly to vehicle number input
    navigateTo('vehicleScreen');
}

// Format price with thousands separator
function formatPrice(price) {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function formatVehicleNumber(input) {
    let value = input.value.toUpperCase().replace(/[^0-9A-Za-z\- ]/g, '');
    input.value = value;

    // Accept any vehicle number with at least 3 characters (international formats)
    const isValid = value.replace(/[\s\-]/g, '').length >= 3;

    if (isValid) {
        input.classList.add('valid');
        input.classList.remove('invalid');
    } else if (value.length > 0) {
        input.classList.add('invalid');
        input.classList.remove('valid');
    } else {
        input.classList.remove('valid', 'invalid');
    }
}

function useRecentVehicle(number) {
    document.getElementById('vehicleNumber').value = number;
    formatVehicleNumber(document.getElementById('vehicleNumber'));
}

function submitVehicle() {
    const input = document.getElementById('vehicleNumber');
    const value = input.value.trim();

    // Accept any vehicle number with at least 3 chars (international formats)
    if (value.replace(/[\s\-]/g, '').length < 3) {
        if (tg) {
            tg.showAlert(t('error_vehicle_format'));
        } else {
            alert(t('error_vehicle_format'));
        }
        return;
    }

    AppState.vehicleNumber = value;

    // Save to recent
    localStorage.setItem('caravan_recent_vehicle', value);

    if (tg) tg.HapticFeedback?.impactOccurred('medium');

    // Go to document upload
    navigateTo('documentsScreen');
}

// ==================== DOCUMENT UPLOAD ====================
function handleFileSelect(event) {
    const files = Array.from(event.target.files);

    if (!files || files.length === 0) return;

    files.forEach(file => {
        // Accept images, PDFs, Word, Excel (check by extension too for mobile compatibility)
        const ext = file.name.toLowerCase().split('.').pop();
        const isImage = file.type.startsWith('image/') || ['jpg', 'jpeg', 'png', 'heic', 'heif', 'webp', 'gif'].includes(ext);
        const isPdf = file.type === 'application/pdf' || ext === 'pdf';
        const isDoc = ['doc', 'docx', 'xls', 'xlsx'].includes(ext) ||
                      file.type.includes('word') || file.type.includes('excel') ||
                      file.type.includes('spreadsheet') || file.type.includes('msword') ||
                      file.type.includes('officedocument');

        if (isImage || isPdf || isDoc) {
            const reader = new FileReader();
            reader.onload = (e) => {
                let fileType = file.type;
                if (!fileType) {
                    if (isImage) fileType = 'image/jpeg';
                    else if (isPdf) fileType = 'application/pdf';
                    else if (isDoc) fileType = 'application/octet-stream';
                }
                AppState.uploadedFiles.push({
                    name: file.name,
                    data: e.target.result,
                    type: fileType,
                    size: file.size
                });
                updateUploadedPreview();
            };
            reader.onerror = () => {
                console.error('File read error:', file.name);
            };
            reader.readAsDataURL(file);
        }
    });

    // Reset input so same file can be selected again
    event.target.value = '';

    if (tg) tg.HapticFeedback?.impactOccurred('light');
}

function updateUploadedPreview() {
    const preview = document.getElementById('uploadedPreview');
    const counter = document.getElementById('uploadCounter');
    const submitBtn = document.getElementById('uploadDoneBtn');

    preview.innerHTML = '';

    AppState.uploadedFiles.forEach((file, index) => {
        const item = document.createElement('div');
        item.className = 'preview-item';

        if (file.type.startsWith('image/')) {
            item.innerHTML = `
                <img src="${file.data}" alt="${file.name}">
                <button class="remove-btn" onclick="removeFile(${index})">×</button>
            `;
        } else {
            // PDF, Word, Excel va boshqa hujjatlar uchun icon
            const ext = file.name.toLowerCase().split('.').pop();
            let icon = '📄';
            if (ext === 'pdf') icon = '📕';
            else if (['doc', 'docx'].includes(ext)) icon = '📘';
            else if (['xls', 'xlsx'].includes(ext)) icon = '📗';
            item.innerHTML = `
                <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;background:#E3F2FD;padding:4px;">
                    <span style="font-size:24px;">${icon}</span>
                    <span style="font-size:9px;overflow:hidden;text-overflow:ellipsis;max-width:100%;white-space:nowrap;">${file.name}</span>
                </div>
                <button class="remove-btn" onclick="removeFile(${index})">×</button>
            `;
        }

        preview.appendChild(item);
    });

    counter.textContent = `${AppState.uploadedFiles.length} ${t('photos_count')}`;

    // Enable/disable submit button (at least 1 file required)
    submitBtn.disabled = AppState.uploadedFiles.length < 1;
}

function removeFile(index) {
    AppState.uploadedFiles.splice(index, 1);
    updateUploadedPreview();

    if (tg) tg.HapticFeedback?.impactOccurred('light');
}

function submitDocuments() {
    if (tg) tg.HapticFeedback?.impactOccurred('medium');

    // Load destinations and go to destination selection
    loadDestinations();
    navigateTo('destScreen');
}

function loadDestinations() {
    const container = document.getElementById('destList');
    container.innerHTML = '';

    TIF_POSTS.forEach(dest => {
        const item = document.createElement('div');
        item.className = 'post-item';
        item.innerHTML = `
            <span class="post-icon">📍</span>
            <span class="post-name">${dest}</span>
            <span class="post-arrow">→</span>
        `;
        item.onclick = () => selectDestination(dest);
        container.appendChild(item);
    });
}

function selectDestination(dest) {
    AppState.selectedDestination = dest;

    if (tg) tg.HapticFeedback?.impactOccurred('medium');

    // Update summary and show
    updateSummary();
    navigateTo('summaryScreen');
}

function updateSummary() {
    // Update service type
    const serviceEl = document.getElementById('sumService');
    if (serviceEl) {
        serviceEl.textContent = AppState.serviceType === 'EPI' ? 'EPI (Electronic Pre-Arrival)' : 'MB DEKLARATSIYA';
    }

    // Update other fields
    document.getElementById('sumVehicle').textContent = AppState.vehicleNumber || '-';
    document.getElementById('sumPost').textContent = AppState.selectedPost || '-';
    document.getElementById('sumDest').textContent = AppState.selectedDestination || '-';

    // Update documents count with new format
    const photosEl = document.getElementById('sumPhotos');
    if (photosEl) {
        const count = AppState.uploadedFiles.length;
        photosEl.innerHTML = `<span class="docs-icon">📎</span> ${count} ${t('files_attached')}`;
    }
}

// Edit summary field - navigate to appropriate screen
function editSummaryField(field) {
    if (tg) tg.HapticFeedback?.impactOccurred('light');

    switch (field) {
        case 'service':
            // Go back to home to select service
            navigateTo('homeScreen');
            break;
        case 'post':
            // Go to border post selection
            loadBorderPosts();
            navigateTo('borderPostScreen');
            break;
        case 'vehicle':
            // Go to vehicle input
            navigateTo('vehicleScreen');
            break;
        case 'documents':
            // Go to documents upload
            navigateTo('documentsScreen');
            break;
        case 'destination':
            // Go to destination selection
            loadDestinations();
            navigateTo('destScreen');
            break;
        default:
            break;
    }
}

function getAgentName(agentId) {
    return '-';
}

// ==================== SUBMIT APPLICATION ====================
async function submitApplication() {
    if (tg) {
        tg.MainButton.showProgress();
        tg.HapticFeedback?.impactOccurred('heavy');
    }

    // Generate application code
    const appCode = generateAppCode();
    const now = new Date();

    // Agent info (not selected in mini app flow)
    const agentName = '-';

    // Prepare data to send to bot
    const applicationData = {
        type: 'application',
        code: appCode,
        user_id: AppState.userId,
        user_name: AppState.userName,
        service_type: AppState.serviceType,
        border_post: AppState.selectedPost,
        destination: AppState.selectedDestination,
        vehicle_number: AppState.vehicleNumber,
        vehicle_type: AppState.vehicleType,
        agent_id: AppState.selectedAgent,
        agent_name: agentName,
        files_count: AppState.uploadedFiles.length,
        language: AppState.language,
        timestamp: now.toISOString()
    };

    // Save application locally BEFORE sendData (sendData closes the Mini App)
    saveApplicationLocally(applicationData);

    // Send to Telegram bot (this closes the Mini App immediately)
    if (tg) {
        try {
            tg.sendData(JSON.stringify(applicationData));
            // Note: Mini App closes here, code below won't execute
        } catch (e) {
            console.error('Error sending data:', e);
            tg.MainButton.hideProgress();
            tg.showAlert('Xatolik yuz berdi. Qaytadan urinib ko\'ring.');
            return;
        }
    }

    // Code below only runs if tg is not available (browser testing)
    // Update waiting screen
    document.getElementById('waitingCode').textContent = appCode;
    document.getElementById('waitingPhotos').textContent = `${AppState.uploadedFiles.length} ta`;
    document.getElementById('waitingTime').textContent = now.toLocaleTimeString('uz', { hour: '2-digit', minute: '2-digit' });
    navigateTo('waitingScreen');
    resetFlowState();
}

function saveApplicationLocally(appData) {
    const apps = JSON.parse(localStorage.getItem('caravan_apps') || '[]');
    apps.unshift(appData);
    // Keep only last 50 applications
    if (apps.length > 50) apps.pop();
    localStorage.setItem('caravan_apps', JSON.stringify(apps));
}

function generateAppCode() {
    const prefix = AppState.serviceType === 'EPI' ? 'EPI' : 'MB';
    const year = new Date().getFullYear();
    const random = Math.floor(100000 + Math.random() * 900000);
    return `${prefix}-${year}-${random}`;
}

// ==================== SCREENS ====================
function showApplicationsScreen() {
    navigateTo('applicationsScreen');
}

function showAppDetail(appId) {
    document.getElementById('appDetailTitle').textContent = appId;
    navigateTo('appDetailScreen');
}

function showPaymentScreen() {
    navigateTo('paymentScreen');
}

function selectPayment(method) {
    if (tg) {
        tg.HapticFeedback?.impactOccurred('medium');

        // Send payment selection to bot
        tg.sendData(JSON.stringify({
            type: 'payment_selected',
            method: method,
            timestamp: new Date().toISOString()
        }));

        tg.showAlert(`${method.toUpperCase()} ${t('coming_soon')}`);
    } else {
        alert(`${method.toUpperCase()} ${t('coming_soon')}`);
    }
}

function showKGDScreen() {
    navigateTo('kgdScreen');
}

function checkKGD() {
    const input = document.getElementById('kgdInput');
    const value = input.value.trim().toUpperCase().replace(/\s/g, '');

    if (!value) {
        if (tg) {
            tg.showAlert(t('enter_vehicle'));
        }
        return;
    }

    // Update result
    document.getElementById('kgdVehicle').textContent = value;
    document.getElementById('kgdResult').style.display = 'block';

    if (tg) tg.HapticFeedback?.impactOccurred('medium');
}

function showPricesScreen() {
    navigateTo('pricesScreen');
}

function showGabarScreen() {
    if (tg) {
        tg.showAlert(t('coming_soon'));
    }
}

function showInsuranceScreen() {
    if (tg) {
        tg.showAlert(t('coming_soon'));
    }
}

function showQueueScreen() {
    if (tg) {
        tg.showAlert(t('coming_soon'));
    }
}

function showContactsScreen() {
    navigateTo('contactsScreen');
}

function showMapScreen() {
    if (tg) {
        tg.showAlert(t('coming_soon'));
    } else {
        alert(t('coming_soon'));
    }
}

// Switch applications tab (Active / History)
function switchAppsTab(tab) {
    const activeTab = document.getElementById('activeTab');
    const historyTab = document.getElementById('historyTab');
    const activeCards = document.querySelectorAll('.app-card-new:not(.completed)');
    const completedCards = document.querySelectorAll('.app-card-new.completed');
    const historyDivider = document.getElementById('historyDivider');

    if (tab === 'active') {
        activeTab.classList.add('active');
        historyTab.classList.remove('active');

        // Show active cards, hide completed
        activeCards.forEach(card => card.style.display = 'block');
        completedCards.forEach(card => card.style.display = 'none');
        if (historyDivider) historyDivider.style.display = 'none';
    } else {
        historyTab.classList.add('active');
        activeTab.classList.remove('active');

        // Hide active cards, show completed
        activeCards.forEach(card => card.style.display = 'none');
        completedCards.forEach(card => card.style.display = 'block');
        if (historyDivider) historyDivider.style.display = 'none';
    }

    if (tg) tg.HapticFeedback?.impactOccurred('light');
}

// ==================== CHAT ====================
function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (!message) return;

    const container = document.getElementById('chatMessages');
    const now = new Date();
    const time = now.toLocaleTimeString('uz', { hour: '2-digit', minute: '2-digit' });

    // Add user message
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message user';
    msgDiv.innerHTML = `
        <div class="message-bubble">
            <p>${escapeHtml(message)}</p>
        </div>
        <span class="message-time">${time} 👤</span>
    `;

    // Insert before typing indicator
    const typingIndicator = document.getElementById('typingIndicator');
    container.insertBefore(msgDiv, typingIndicator);

    // Clear input
    input.value = '';

    // Scroll to bottom
    container.scrollTop = container.scrollHeight;

    // Show typing indicator
    typingIndicator.style.display = 'flex';

    // Send to bot
    if (tg) {
        tg.sendData(JSON.stringify({
            type: 'chat_message',
            message: message,
            timestamp: now.toISOString()
        }));
    }

    // Hide typing after delay (simulate response)
    setTimeout(() => {
        typingIndicator.style.display = 'none';
    }, 2000);

    if (tg) tg.HapticFeedback?.impactOccurred('light');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ==================== BONUS ====================
function copyReferralLink() {
    const link = document.getElementById('referralLink').textContent;

    if (navigator.clipboard) {
        navigator.clipboard.writeText(link);
    }

    if (tg) {
        tg.showAlert(t('link_copied'));
        tg.HapticFeedback?.notificationOccurred('success');
    }
}

function shareReferralLink() {
    const link = document.getElementById('referralLink').textContent;
    const text = "CARAVAN TRANZIT - Yuk tashish oson! Ro'yxatdan o'ting va bonus oling: " + link;

    if (tg) {
        tg.openTelegramLink(`https://t.me/share/url?url=${encodeURIComponent(link)}&text=${encodeURIComponent(text)}`);
    } else if (navigator.share) {
        navigator.share({ title: 'CARAVAN TRANZIT', text: text, url: link });
    }
}

// ==================== SETTINGS ====================
function clearCache() {
    localStorage.clear();

    if (tg) {
        tg.showAlert(t('cache_cleared'));
        tg.HapticFeedback?.notificationOccurred('success');
    }
}

function editPhone() {
    if (tg) {
        tg.showAlert(t('contact_admin_phone'));
    }
}

function contactAdmin() {
    if (tg) {
        tg.openTelegramLink('https://t.me/CARAVAN_TRANZIT');
    }
}

// ==================== UTILITIES ====================
function filterList(containerId, query) {
    const container = document.getElementById(containerId);
    const items = container.querySelectorAll('.post-item');
    const lowerQuery = query.toLowerCase();

    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(lowerQuery) ? 'flex' : 'none';
    });
}

function handleMainButton() {
    // Handle main button actions based on current screen
    switch (AppState.currentScreen) {
        case 'summaryScreen':
            submitApplication();
            break;
        case 'documentsScreen':
            submitDocuments();
            break;
        default:
            console.log('Main button clicked on:', AppState.currentScreen);
    }
}

// ==================== EXPORT FOR HTML ONCLICK ====================
window.startEPIFlow = startEPIFlow;
window.startMBFlow = startMBFlow;
window.formatVehicleNumber = formatVehicleNumber;
window.useRecentVehicle = useRecentVehicle;
window.submitVehicle = submitVehicle;
window.handleFileSelect = handleFileSelect;
window.removeFile = removeFile;
window.submitDocuments = submitDocuments;
window.submitApplication = submitApplication;
window.showApplicationsScreen = showApplicationsScreen;
window.showAppDetail = showAppDetail;
window.showPaymentScreen = showPaymentScreen;
window.selectPayment = selectPayment;
window.showKGDScreen = showKGDScreen;
window.checkKGD = checkKGD;
window.showPricesScreen = showPricesScreen;
window.showGabarScreen = showGabarScreen;
window.showInsuranceScreen = showInsuranceScreen;
window.showQueueScreen = showQueueScreen;
window.showContactsScreen = showContactsScreen;
window.navigateTo = navigateTo;
window.goBack = goBack;
window.goHome = goHome;
window.sendMessage = sendMessage;
window.copyReferralLink = copyReferralLink;
window.shareReferralLink = shareReferralLink;
window.changeLanguage = changeLanguage;
window.selectLanguage = selectLanguage;
window.showLanguageModal = showLanguageModal;
window.clearCache = clearCache;
window.editPhone = editPhone;
window.contactAdmin = contactAdmin;
window.filterList = filterList;
window.formatPrice = formatPrice;
window.editSummaryField = editSummaryField;
window.loadPopularPosts = loadPopularPosts;
window.loadGroupedPosts = loadGroupedPosts;
window.filterBorderPosts = filterBorderPosts;
window.showMapScreen = showMapScreen;
window.switchAppsTab = switchAppsTab;
window.t = t;

console.log('CARAVAN TRANZIT Mini App v3.0 loaded with i18n support');
