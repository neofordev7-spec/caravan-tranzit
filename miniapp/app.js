/**
 * CARAVAN TRANZIT Mini App - JavaScript
 * Version: 4.0 (Secure API Integration)
 * Telegram Web App Integration with i18n and Fetch API
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

const POPULAR_POSTS = [
    { name: 'Yallama', region: 'Toshkent viloyati' },
    { name: 'Olot', region: 'Buxoro viloyati' },
    { name: "Do'stlik", region: 'Andijon viloyati' }
];

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

        if (tg.initDataUnsafe?.user) {
            AppState.userId = tg.initDataUnsafe.user.id;
            AppState.userName = tg.initDataUnsafe.user.first_name + ' ' + (tg.initDataUnsafe.user.last_name || '');
            
            const tgLang = tg.initDataUnsafe.user.language_code;
            if (tgLang && !localStorage.getItem('caravan_lang')) {
                const langMap = { 'uz': 'uz', 'ru': 'ru', 'en': 'en' };
                if (langMap[tgLang]) {
                    AppState.language = langMap[tgLang];
                    localStorage.setItem('caravan_lang', langMap[tgLang]);
                }
            }
        }

        tg.BackButton.onClick(() => goBack());
        tg.MainButton.onClick(() => handleMainButton());
    }
}

function initApp() {
    if (typeof setLanguage === 'function') {
        setLanguage(AppState.language);
    }
    navigateTo('homeScreen');
    setupEventListeners();
    updateAllUITexts();
    loadSavedData();
    AppState.isInitialized = true;
}

function setupEventListeners() {
    document.getElementById('headerBackBtn')?.addEventListener('click', () => goBack());
    document.getElementById('profileBtn')?.addEventListener('click', () => navigateTo('settingsScreen'));
    document.addEventListener('languageChanged', () => updateAllUITexts());
}

function loadSavedData() {
    const recentVehicle = localStorage.getItem('caravan_recent_vehicle');
    if (recentVehicle) {
        const recentEl = document.getElementById('recentVehicles');
        if (recentEl) {
            recentEl.innerHTML = `
                <div class="recent-item" onclick="useRecentVehicle('${recentVehicle}')">
                    <span class="recent-icon">🔄</span>
                    <span class="recent-text">${t('previous_vehicle')}: <strong>${recentVehicle}</strong></span>
                </div>`;
        }
    }
    updateCoinsDisplay();
}

// ==================== NAVIGATION & UI ====================
function navigateTo(screenId) {
    if (AppState.currentScreen && AppState.currentScreen !== screenId) {
        AppState.previousScreens.push(AppState.currentScreen);
    }
    document.querySelectorAll('.screen').forEach(screen => screen.classList.remove('active'));
    const targetScreen = document.getElementById(screenId);
    if (targetScreen) {
        targetScreen.classList.add('active');
        AppState.currentScreen = screenId;
    }
    updateBottomNav(screenId);
    updateBackButton();
    window.scrollTo(0, 0);
    if (tg) tg.HapticFeedback?.impactOccurred('light');
}

function updateBottomNav(screenId) {
    document.querySelectorAll('.nav-item-new').forEach(item => {
        item.classList.toggle('active', item.getAttribute('data-screen') === screenId);
    });
}

function updateBackButton() {
    const mainScreens = ['homeScreen', 'applicationsScreen', 'chatScreen', 'settingsScreen'];
    if (tg) {
        if (mainScreens.includes(AppState.currentScreen)) tg.BackButton.hide();
        else tg.BackButton.show();
    }
}

function goBack() {
    if (AppState.previousScreens.length > 0) navigateTo(AppState.previousScreens.pop());
    else navigateTo('homeScreen');
}

function goHome() {
    AppState.previousScreens = [];
    navigateTo('homeScreen');
    resetFlowState();
}

function resetFlowState() {
    AppState.serviceType = null;
    AppState.selectedPost = null;
    AppState.vehicleNumber = null;
    AppState.selectedDestination = null;
    AppState.uploadedFiles = [];
}

// ==================== 🚀 SUBMIT APPLICATION (The Main Fix) ====================
async function submitApplication() {
    if (tg) {
        tg.MainButton.showProgress();
        tg.HapticFeedback?.impactOccurred('heavy');
    }

    // Backend ga yuboriladigan ma'lumotlar
    const appData = {
        user_id: AppState.userId,
        user_name: AppState.userName,
        service_type: AppState.serviceType,
        border_post: AppState.selectedPost,
        destination: AppState.selectedDestination,
        vehicle_number: AppState.vehicleNumber,
        language: AppState.language,
        // Eslatma: Rasmlarni yuborish uchun alohida logika kerak bo'lishi mumkin
        photos_count: AppState.uploadedFiles.length 
    };

    try {
        // 🟢 TUZATILDI: tg.sendData o'rniga Fetch API ishlatildi
        const response = await fetch('/api/applications', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(appData)
        });

        const result = await response.json();

        if (result.success) {
            // Muvaffaqiyatli bo'lsa, Waiting Screen'ni yangilaymiz
            document.getElementById('waitingCode').textContent = result.app_code;
            document.getElementById('waitingPhotos').textContent = `${AppState.uploadedFiles.length} ta`;
            document.getElementById('waitingTime').textContent = new Date().toLocaleTimeString('uz', { hour: '2-digit', minute: '2-digit' });
            
            saveApplicationLocally({ ...appData, code: result.app_code });
            navigateTo('waitingScreen');
            resetFlowState();
            
            if (tg) tg.MainButton.hide();
        } else {
            const errMsg = (typeof result.error === 'string') ? result.error : 'Server error';
            throw new Error(errMsg);
        }
    } catch (e) {
        const alertMsg = (typeof e.message === 'string' && e.message !== 'Server error')
            ? e.message
            : t('error_general');
        if (tg) tg.showAlert(alertMsg);
        else alert(alertMsg);
    } finally {
        if (tg) tg.MainButton.hideProgress();
    }
}

// ==================== FLOW LOGIC ====================
function startEPIFlow() { AppState.serviceType = 'EPI'; loadBorderPosts(); navigateTo('borderPostScreen'); }
function startMBFlow() { AppState.serviceType = 'MB'; loadBorderPosts(); navigateTo('borderPostScreen'); }

function loadBorderPosts() {
    loadPopularPosts();
    loadGroupedPosts();
}

function loadPopularPosts() {
    const container = document.getElementById('popularPostsContainer');
    if (!container) return;
    container.innerHTML = POPULAR_POSTS.map(post => `
        <div class="popular-post-card" onclick="selectBorderPost('${post.name}')">
            <div class="popular-post-simple">
                <h4 class="popular-post-name">${post.name}</h4>
                <p class="popular-post-region">${post.region}</p>
            </div>
        </div>`).join('');
}

function loadGroupedPosts() {
    const container = document.getElementById('borderPostsList');
    if (!container) return;
    const sorted = [...BORDER_POSTS].sort((a, b) => a.localeCompare(b, 'uz'));
    container.innerHTML = sorted.map(post => `
        <div class="post-item-grouped" onclick="selectBorderPost('${post}')">
            <span class="post-item-name">${post}</span>
            <span class="post-item-arrow">›</span>
        </div>`).join('');
}

function selectBorderPost(post) {
    AppState.selectedPost = post;
    navigateTo('vehicleScreen');
}

function formatVehicleNumber(input) {
    input.value = input.value.toUpperCase().replace(/[^0-9A-Za-z\- ]/g, '');
    const isValid = input.value.length >= 3;
    input.classList.toggle('valid', isValid);
}

function submitVehicle() {
    const val = document.getElementById('vehicleNumber').value.trim();
    if (val.length < 3) return tg?.showAlert(t('error_vehicle_format'));
    AppState.vehicleNumber = val;
    localStorage.setItem('caravan_recent_vehicle', val);
    navigateTo('documentsScreen');
}

// ==================== HELPERS ====================
function saveApplicationLocally(appData) {
    const apps = JSON.parse(localStorage.getItem('caravan_apps') || '[]');
    apps.unshift(appData);
    localStorage.setItem('caravan_apps', JSON.stringify(apps.slice(0, 50)));
}

function updateCoinsDisplay() {
    const el = document.getElementById('coinsValue');
    if (el) el.textContent = AppState.userCoins.toLocaleString();
}

function updateAllUITexts() {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        el.textContent = t(el.getAttribute('data-i18n'));
    });
}

function submitDocuments() {
    navigateTo('summaryScreen');
}

function handleMainButton() {
    if (AppState.currentScreen === 'summaryScreen') submitApplication();
    else if (AppState.currentScreen === 'documentsScreen') submitDocuments();
}

// ==================== PAYME DYNAMIC LINK ====================
async function openPaymeLink(appCode) {
    if (!appCode) {
        if (tg) tg.showAlert('Ariza kodi topilmadi.');
        return;
    }

    try {
        const params = new URLSearchParams();
        if (AppState.userId) params.set('user_id', AppState.userId);

        const response = await fetch(`/api/payments/payme-link/${encodeURIComponent(appCode)}?${params.toString()}`);
        const result = await response.json();

        if (result.success && result.url) {
            if (tg) {
                tg.openLink(result.url);
            } else {
                window.open(result.url, '_blank');
            }
        } else {
            const errorMsg = (typeof result.error === 'string') ? result.error : 'Payme havolasini olishda xatolik';
            if (tg) tg.showAlert(errorMsg);
            else alert(errorMsg);
        }
    } catch (e) {
        if (tg) tg.showAlert(t('error_general'));
        else alert(t('error_general'));
    }
}

// Global scope export
Object.assign(window, {
    startEPIFlow, startMBFlow, selectBorderPost, submitVehicle,
    submitApplication, navigateTo, goBack, goHome, openPaymeLink,
    formatVehicleNumber, useRecentVehicle: (n) => { document.getElementById('vehicleNumber').value = n; },
    showApplicationsScreen: () => navigateTo('applicationsScreen'),
    showKGDScreen: () => navigateTo('kgdScreen'),
    showPricesScreen: () => navigateTo('pricesScreen'),
    showContactsScreen: () => navigateTo('contactsScreen'),
    showMapScreen: () => { if (tg) tg.showAlert(t('coming_soon')); },
    submitDocuments
});
