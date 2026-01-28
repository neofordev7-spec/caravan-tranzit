/**
 * CARAVAN TRANZIT Mini App - JavaScript
 * Version: 2.0
 * Telegram Web App Integration
 */

// ==================== TELEGRAM WEB APP ====================
const tg = window.Telegram?.WebApp;

// ==================== APP STATE ====================
const AppState = {
    currentScreen: 'splashScreen',
    previousScreens: [],
    language: localStorage.getItem('caravan_lang') || null,
    serviceType: null, // 'EPI' or 'MB'
    selectedPost: null,
    selectedAgent: null,
    vehicleNumber: null,
    selectedDestination: null,
    uploadedFiles: [],
    userCoins: 17500,
    userId: null
};

// ==================== DATA (BOTDAGI KABI) ====================
// CHEGARA BOJXONA POSTLARI (59 ta) - keyboards.py dan
const BORDER_POSTS = [
    "Yallama",
    "Olot",
    "Doʻstlik (Andijon)",
    "S. Najimov",
    "Dovut-ota",
    "Sirdaryo",
    "Ayritom",
    "Jartepa",
    "Oʻzbekiston",
    "Oybek",
    "Sariosiyo",
    "Uchqoʻrgʻon",
    "Shovot",
    "Islom Karimov nomidagi Toshkent xalqaro aeroporti",
    "Andarxon",
    "Xoʻjayli",
    "Kosonsoy",
    "Navoiy aeroporti",
    "Nukus aeroporti",
    "Qoraqalpogʻiston",
    "Doʻstlik (Qoraqalpog'iston)",
    "Andijon aeroporti",
    "Mingtepa",
    "Qorasuv",
    "Xonobod",
    "Pushmon",
    "Madaniyat",
    "Keskanyor",
    "Savay",
    "Buxoro aeroporti",
    "Xoʻjadavlat",
    "Uchtoʻrgʻon",
    "Qoʻshkent",
    "Qarshi-Kerki",
    "Qarshi aeroporti",
    "Namangan aeroporti",
    "Pop",
    "Samarqand aeroporti",
    "Termiz aeroporti",
    "Gulbahor",
    "Boldir",
    "Xovosobod",
    "Oq oltin",
    "Malik",
    "Navoiy",
    "Bekobod avto",
    "Gʻishtkoʻprik",
    "Farhod",
    "Bekobod",
    "Fargʻona aeroporti",
    "Fargʻona",
    "Rishton",
    "Rovot",
    "Soʻx",
    "Doʻstlik (Xorazm)",
    "Urganch aeroporti",
    "Keles",
    "Chuqursoy texnik idora"
];

// TIF (TASHQI IQTISODIY FAOLIYAT) POSTLARI (33 ta) - keyboards.py dan
const TIF_POSTS = [
    "Avia yuklar",
    "Sirgʻali",
    "Chuqursoy",
    "Toshkent-tovar",
    "Termiz",
    "Buxoro",
    "Angren",
    "Vodiy",
    "Ark buloq",
    "Qorakoʻl",
    "Termiz xalqaro savdo markazi",
    "Nasaf",
    "Urganch",
    "Ulugʻbek",
    "Guliston",
    "Asaka",
    "Namangan",
    "Samarqand",
    "Jizzax",
    "Qoʻqon",
    "Nukus",
    "Andijon",
    "Qamashi-Gʻuzor",
    "Navoiy",
    "Zarafshon",
    "Denov",
    "Daryo porti",
    "Chirchiq",
    "Olmaliq",
    "Yangiyoʻl",
    "Nazarbek",
    "Keles",
    "Elektron tijorat"
];

// O'ZBEKISTON VILOYATLARI (14 ta) - keyboards.py dan
const VILOYATLAR = [
    "Qoraqalpogʻiston Respublikasi",
    "Andijon viloyati",
    "Buxoro viloyati",
    "Fargʻona viloyati",
    "Jizzax viloyati",
    "Xorazm viloyati",
    "Namangan viloyati",
    "Navoiy viloyati",
    "Qashqadaryo viloyati",
    "Samarqand viloyati",
    "Sirdaryo viloyati",
    "Surxondaryo viloyati",
    "Toshkent viloyati",
    "Toshkent shahri"
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

        // Get user data
        if (tg.initDataUnsafe?.user) {
            AppState.userId = tg.initDataUnsafe.user.id;
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
    // Set default language
    if (!AppState.language) {
        AppState.language = 'uz_lat';
        localStorage.setItem('caravan_lang', 'uz_lat');
    }

    // Show main app immediately - no splash, no delays
    showMainApp();

    // Setup event listeners
    setupEventListeners();
}

function setupEventListeners() {
    // Header back button
    document.getElementById('headerBackBtn')?.addEventListener('click', () => goBack());

    // Profile button
    document.getElementById('profileBtn')?.addEventListener('click', () => {
        navigateTo('settingsScreen');
    });
}

// ==================== LANGUAGE ====================
function selectLanguage(lang) {
    AppState.language = lang;
    localStorage.setItem('caravan_lang', lang);

    // Haptic feedback
    if (tg) tg.HapticFeedback?.impactOccurred('light');

    showMainApp();
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
    document.querySelectorAll('.nav-item').forEach(item => {
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

// ==================== EPI/MB FLOW (BOTDAGI KABI) ====================
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
    const container = document.getElementById('borderPostsList');
    container.innerHTML = '';

    // ANIQ EMAS tugmasi - birinchi
    const aniqEmasItem = document.createElement('div');
    aniqEmasItem.className = 'post-item aniq-emas';
    aniqEmasItem.innerHTML = `
        <span class="post-icon">❓</span>
        <span class="post-name">ANIQ EMAS</span>
        <span class="post-arrow">→</span>
    `;
    aniqEmasItem.onclick = () => showViloyatSelection('border');
    container.appendChild(aniqEmasItem);

    // Barcha postlar
    BORDER_POSTS.forEach(post => {
        const item = document.createElement('div');
        item.className = 'post-item';
        item.innerHTML = `
            <span class="post-icon">🏛</span>
            <span class="post-name">${post}</span>
            <span class="post-arrow">→</span>
        `;
        item.onclick = () => selectBorderPost(post);
        container.appendChild(item);
    });
}

function showViloyatSelection(type) {
    // type: 'border' yoki 'dest'
    AppState.viloyatSelectionType = type;
    loadViloyatlar();
    navigateTo('viloyatScreen');
}

function loadViloyatlar() {
    const container = document.getElementById('viloyatList');
    if (!container) return;
    container.innerHTML = '';

    VILOYATLAR.forEach(viloyat => {
        const item = document.createElement('div');
        item.className = 'post-item';
        item.innerHTML = `
            <span class="post-icon">🗺</span>
            <span class="post-name">${viloyat}</span>
            <span class="post-arrow">→</span>
        `;
        item.onclick = () => selectViloyat(viloyat);
        container.appendChild(item);
    });
}

function selectViloyat(viloyat) {
    if (tg) tg.HapticFeedback?.impactOccurred('medium');

    if (AppState.viloyatSelectionType === 'border') {
        AppState.selectedPost = `ANIQ EMAS (${viloyat})`;
        // TIF tanlashga o'tish
        loadDestinations();
        navigateTo('destScreen');
    } else {
        AppState.selectedDestination = `ANIQ EMAS (${viloyat})`;
        // Mashina raqamiga o'tish
        navigateTo('vehicleScreen');
    }
}

function selectBorderPost(post) {
    AppState.selectedPost = post;

    if (tg) tg.HapticFeedback?.impactOccurred('medium');

    // TIF (manzil) tanlashga o'tish - botdagi kabi
    loadDestinations();
    navigateTo('destScreen');
}

function formatVehicleNumber(input) {
    let value = input.value.toUpperCase().replace(/[^0-9A-Z]/g, '');
    input.value = value;

    // Validate format
    const isValid = /^[0-9]{2}[A-Z][0-9]{3}[A-Z]{2}$/.test(value);

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

    if (!/^[0-9]{2}[A-Z][0-9]{3}[A-Z]{2}$/.test(value)) {
        if (tg) {
            tg.showAlert("Iltimos, mashina raqamini to'g'ri kiriting!\n\nMisol: 01A777AA");
        } else {
            alert("Iltimos, mashina raqamini to'g'ri kiriting!\n\nMisol: 01A777AA");
        }
        return;
    }

    AppState.vehicleNumber = value;

    // Save to recent
    localStorage.setItem('caravan_recent_vehicle', value);

    if (tg) tg.HapticFeedback?.impactOccurred('medium');

    // Hujjat yuklashga o'tish - botdagi kabi
    navigateTo('documentsScreen');
}

// ==================== DOCUMENT UPLOAD ====================
function handleFileSelect(event) {
    const files = Array.from(event.target.files);

    files.forEach(file => {
        if (file.type.startsWith('image/') || file.type === 'application/pdf') {
            const reader = new FileReader();
            reader.onload = (e) => {
                AppState.uploadedFiles.push({
                    name: file.name,
                    data: e.target.result,
                    type: file.type
                });
                updateUploadedPreview();
            };
            reader.readAsDataURL(file);
        }
    });

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
            item.innerHTML = `
                <div style="display:flex;align-items:center;justify-content:center;height:100%;background:#E3F2FD;">
                    <span style="font-size:24px;">📄</span>
                </div>
                <button class="remove-btn" onclick="removeFile(${index})">×</button>
            `;
        }

        preview.appendChild(item);
    });

    counter.textContent = `${AppState.uploadedFiles.length} ta rasm`;

    // Enable submit button - always enabled (0 ta bo'lsa ham davom etish mumkin)
    submitBtn.disabled = false;
}

function removeFile(index) {
    AppState.uploadedFiles.splice(index, 1);
    updateUploadedPreview();

    if (tg) tg.HapticFeedback?.impactOccurred('light');
}

function submitDocuments() {
    if (tg) tg.HapticFeedback?.impactOccurred('medium');

    // Summary ga o'tish - botdagi kabi
    updateSummary();
    navigateTo('summaryScreen');
}

function loadDestinations() {
    const container = document.getElementById('destList');
    container.innerHTML = '';

    // ANIQ EMAS tugmasi - birinchi
    const aniqEmasItem = document.createElement('div');
    aniqEmasItem.className = 'post-item aniq-emas';
    aniqEmasItem.innerHTML = `
        <span class="post-icon">❓</span>
        <span class="post-name">ANIQ EMAS</span>
        <span class="post-arrow">→</span>
    `;
    aniqEmasItem.onclick = () => showViloyatSelection('dest');
    container.appendChild(aniqEmasItem);

    // Barcha TIF postlari
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

    // Mashina raqamiga o'tish - botdagi kabi
    navigateTo('vehicleScreen');
}

function updateSummary() {
    document.getElementById('sumVehicle').textContent = AppState.vehicleNumber || '-';
    document.getElementById('sumPost').textContent = AppState.selectedPost || '-';
    document.getElementById('sumDest').textContent = AppState.selectedDestination || '-';
    document.getElementById('sumPhotos').textContent = `${AppState.uploadedFiles.length} ta`;
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

    // Prepare data - botdagi kabi
    const applicationData = {
        code: appCode,
        user_id: AppState.userId,
        service_type: AppState.serviceType,
        border_post: AppState.selectedPost,
        dest_post: AppState.selectedDestination,
        car_number: AppState.vehicleNumber,
        files_count: AppState.uploadedFiles.length,
        timestamp: now.toISOString()
    };

    // Update waiting screen
    document.getElementById('waitingCode').textContent = appCode;
    document.getElementById('waitingPhotos').textContent = `${AppState.uploadedFiles.length} ta`;
    document.getElementById('waitingTime').textContent = now.toLocaleTimeString('uz', { hour: '2-digit', minute: '2-digit' });

    // Show waiting screen
    navigateTo('waitingScreen');

    // Send to Telegram bot
    if (tg) {
        tg.sendData(JSON.stringify(applicationData));
        tg.MainButton.hideProgress();
    }

    // Reset flow state
    resetFlowState();
}

function generateAppCode() {
    const prefix = AppState.serviceType === 'EPI' ? 'EPI' : 'MB';
    const year = new Date().getFullYear();
    const random = Math.floor(1000 + Math.random() * 9000);
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
        tg.showAlert(`${method.toUpperCase()} to'lov tanlandi. Tez orada ishga tushadi!`);
    } else {
        alert(`${method.toUpperCase()} to'lov tanlandi.`);
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
            tg.showAlert('Iltimos, mashina raqamini kiriting!');
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
        tg.showAlert('Gabarit xizmati tez orada ishga tushadi!');
    }
}

function showInsuranceScreen() {
    if (tg) {
        tg.showAlert("Sug'urta xizmati tez orada ishga tushadi!");
    }
}

function showQueueScreen() {
    if (tg) {
        tg.showAlert('Navbat xizmati tez orada ishga tushadi!');
    }
}

function showContactsScreen() {
    navigateTo('contactsScreen');
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
        tg.showAlert('Havola nusxalandi!');
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
function changeLanguage() {
    // Show alert - language change via settings only
    if (tg) {
        tg.showAlert("Til: O'zbek (Latin). Tilni o'zgartirish imkoniyati tez orada qo'shiladi.");
    } else {
        alert("Til: O'zbek (Latin)");
    }
}

function clearCache() {
    localStorage.clear();

    if (tg) {
        tg.showAlert('Xotira tozalandi!');
        tg.HapticFeedback?.notificationOccurred('success');
    }
}

function editPhone() {
    if (tg) {
        tg.showAlert('Telefon raqamini o\'zgartirish uchun admin bilan bog\'laning.');
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
window.selectAgent = selectAgent;
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
window.clearCache = clearCache;
window.editPhone = editPhone;
window.contactAdmin = contactAdmin;
window.filterList = filterList;

console.log('CARAVAN TRANZIT Mini App v2.0 loaded');
