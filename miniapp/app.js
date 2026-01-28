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

const AGENTS = [
    {
        id: 'ali',
        name: 'Ali Valiyev',
        rating: 4.8,
        priceMin: 35000,
        priceMax: 60000,
        badge: 'Top Rated',
        online: true,
        avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuA-4mXKU91loGciYNcynW5W0szXcGke8fIG5daq5NfGfkfMdAAAjJLEzhtuoNEnKUhKoBTK97bsvZhj1QQE8L7gmbQkaovU4Y0UqOX__aUuRi-lYNP8BmP-ieznwyHxDNABqYuc0H3bshPEwKnRdxZX8Ay_0N66kLJmWGp332wNgz5BckDHwyFGh_NzVKn74hg5RRiudRCy-aYCEcRKGQkkB2lHU9ac9t02MJiNVOgbGNmkCcLSuhxQaNDm-YhJ1_4dCPCdrMPoTdY'
    },
    {
        id: 'sanjar',
        name: 'Sanjar Islomov',
        rating: 4.9,
        priceMin: 40000,
        priceMax: 65000,
        badge: 'Fast Response',
        online: true,
        avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDA5jd_af6u8rvQ-3pYCQE4HYF9sO6t19uhZ3vqyKzsYvFDZg4_sGewLg9BecZMqQAmAM9EootOyjA9MLMyvmeNd_BAbezyLTAkT9tAvKVpva0u_PqJiCwZvvT96ybFyjrNdTXQg-VbnkJ5PPRCOtalYo4DNbmpUDKuv6vYiPGDupMlEDJ2pKNIA7XVI3JY417U53DEWMv8n5S7Zm2YGvye9944PrDqpltPV5VdGpBVbxJAXuWFUileTSuMxcxEd6kb4zrw27j5d7A'
    },
    {
        id: 'nigora',
        name: 'Nigora Saidova',
        rating: 4.7,
        priceMin: 38000,
        priceMax: 62000,
        badge: 'Highly Recommended',
        online: true,
        avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCODBuLtQS0l9ImFObjL52sU7JrI5Kb9poisA6ywRjkhcHm_vNHHCg5HDp3rHpEE4z8pfNHbIQ-SDcNyE9zJuNj_BW7sFNqYZsbg8mtif2Bk01rm4GK7Xa2KxKtbctmNGnuVVt5uwA_FR2hKA9tfwbjsoEXVGYHWLt5P03DSpswM9wuNXDDlUv9WE7R9W8QraIGwlCUcOnuQeQikYscPvsCmrXzXQeBDm940mjqfpx8o_Esy5vZE8EHlTm8Ss3Ah0UMTQQ6UhiBa7M'
    }
];

// Offline agents data
const OFFLINE_AGENTS = [
    { id: 'karim', name: 'Karim Rahimov', rating: 4.5 },
    { id: 'aziza', name: 'Aziza Karimova', rating: 4.6 },
    { id: 'bobur', name: 'Bobur Xolmatov', rating: 4.4 },
    { id: 'dilnoza', name: 'Dilnoza Tosheva', rating: 4.3 },
    { id: 'jamshid', name: 'Jamshid Aliev', rating: 4.5 },
    { id: 'shoxrux', name: 'Shoxrux Ergashev', rating: 4.2 },
    { id: 'madina', name: 'Madina Yusupova', rating: 4.6 },
    { id: 'rustam', name: 'Rustam Nazarov', rating: 4.4 }
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
    const container = document.getElementById('borderPostsList');
    container.innerHTML = '';

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

function selectBorderPost(post) {
    AppState.selectedPost = post;

    if (tg) tg.HapticFeedback?.impactOccurred('medium');

    // Update agent screen header with post name
    const postNameEl = document.getElementById('agentPostName');
    if (postNameEl) {
        postNameEl.textContent = post + ' posti';
    }

    // Load agents for this post
    loadAgents();

    // Go to agent selection
    navigateTo('agentScreen');
}

// Load online agents dynamically
function loadAgents() {
    const container = document.getElementById('agentsList');
    if (!container) return;

    container.innerHTML = '';

    const onlineAgents = AGENTS.filter(a => a.online);
    document.getElementById('onlineAgentCount').textContent = onlineAgents.length;

    onlineAgents.forEach(agent => {
        const card = document.createElement('div');
        card.className = 'agent-card-new';
        card.innerHTML = `
            <div class="agent-avatar-wrapper">
                <div class="agent-avatar-img" style="background-image: url('${agent.avatar}')"></div>
                <div class="agent-online-indicator"></div>
            </div>
            <div class="agent-info-new">
                <h4 class="agent-name">${agent.name}</h4>
                <p class="agent-price">${formatPrice(agent.priceMin)} - ${formatPrice(agent.priceMax)} so'm</p>
                <div class="agent-rating-badge">
                    <span class="star">⭐</span>
                    <span>${agent.rating} • ${agent.badge}</span>
                </div>
            </div>
            <button class="agent-select-btn" onclick="event.stopPropagation(); selectAgent('${agent.id}')">
                Select
            </button>
        `;
        card.onclick = () => selectAgent(agent.id);
        container.appendChild(card);
    });

    // Load offline agents count
    document.getElementById('offlineAgentCount').textContent = OFFLINE_AGENTS.length;
    loadOfflineAgents();
}

// Load offline agents list
function loadOfflineAgents() {
    const container = document.getElementById('offlineAgentsList');
    if (!container) return;

    container.innerHTML = '';

    OFFLINE_AGENTS.forEach(agent => {
        const item = document.createElement('div');
        item.className = 'offline-agent-item';
        item.innerHTML = `
            <div class="offline-agent-avatar">👤</div>
            <div class="offline-agent-info">
                <span class="offline-agent-name">${agent.name}</span>
                <span class="offline-agent-rating">⭐ ${agent.rating}</span>
            </div>
            <span class="offline-status">Offline</span>
        `;
        container.appendChild(item);
    });
}

// Toggle offline agents section
function toggleOfflineAgents() {
    const list = document.getElementById('offlineAgentsList');
    const arrow = document.getElementById('offlineArrow');

    if (list.style.display === 'none') {
        list.style.display = 'block';
        arrow.textContent = '▲';
    } else {
        list.style.display = 'none';
        arrow.textContent = '▼';
    }

    if (tg) tg.HapticFeedback?.impactOccurred('light');
}

// Find nearest post function
function findNearestPost() {
    if (tg) {
        tg.HapticFeedback?.impactOccurred('medium');
        tg.showAlert('Eng yaqin post qidirilmoqda... Bu funksiya tez orada ishga tushadi!');
    } else {
        alert('Eng yaqin post qidirilmoqda...');
    }
}

// Format price with thousands separator
function formatPrice(price) {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function selectAgent(agentId) {
    AppState.selectedAgent = agentId;

    if (tg) tg.HapticFeedback?.impactOccurred('medium');

    // Go to vehicle number input
    navigateTo('vehicleScreen');
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

    // Go to document upload
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

    // Enable/disable submit button
    const minFiles = AppState.serviceType === 'EPI' ? 2 : 2;
    submitBtn.disabled = AppState.uploadedFiles.length < minFiles;
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
    document.getElementById('sumVehicle').textContent = AppState.vehicleNumber || '-';
    document.getElementById('sumPost').textContent = AppState.selectedPost || '-';
    document.getElementById('sumDest').textContent = AppState.selectedDestination || '-';
    document.getElementById('sumAgent').textContent = getAgentName(AppState.selectedAgent);
    document.getElementById('sumPhotos').textContent = `${AppState.uploadedFiles.length} ta`;
}

function getAgentName(agentId) {
    if (agentId === 'cash') return 'Naqd pulda (Cash Payment)';
    const agent = AGENTS.find(a => a.id === agentId);
    if (agent) {
        return `${agent.name} (${formatPrice(agent.priceMin)}-${formatPrice(agent.priceMax)} so'm)`;
    }
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

    // Prepare data
    const applicationData = {
        code: appCode,
        user_id: AppState.userId,
        service_type: AppState.serviceType,
        border_post: AppState.selectedPost,
        destination: AppState.selectedDestination,
        vehicle_number: AppState.vehicleNumber,
        agent: AppState.selectedAgent,
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
window.loadAgents = loadAgents;
window.loadOfflineAgents = loadOfflineAgents;
window.toggleOfflineAgents = toggleOfflineAgents;
window.findNearestPost = findNearestPost;
window.formatPrice = formatPrice;

console.log('CARAVAN TRANZIT Mini App v2.0 loaded');
