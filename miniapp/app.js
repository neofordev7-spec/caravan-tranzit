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

// Popular border posts with images
const POPULAR_POSTS = [
    {
        name: 'Yallama',
        region: 'Toshkent viloyati',
        agents: 12,
        image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCp-W_rYtGPEKTrMRFwSk8wy_LwJcJnUPbUaNOBTN-evLT2Y81LFIl-tI4HVLGSm3VWsOQQnNg6SIL2c9FNxCMTOg9TqMSVw75VawA8GXVFV_R4A7xSbf8LJsBMQNKzwEqXMzKd5s8M2ECU9IbN0EzzOy_YN-jWRuOCjRwrxqJQ6yOQTj14YEZSfJnP-cQtS6h_XW-iRCN7C1u4OhP_g6JZG_q8eMj_i0hl84F8mXG3sJ1Ct5qIBEGDlOZnqb90sRKBQfAQDFFmTuI'
    },
    {
        name: 'Olot',
        region: 'Buxoro viloyati',
        agents: 8,
        image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCwdYoL14nKWM5EBcjHLPy-o4_4xKV0yEyLQ-6_TQ0D49AqFOy1MK0q0bexXpRpAdUOCBq_S3aKOKLhC5-O9l8SKg0kC0JY4mA0Kv1TWj5LF8NWY5RM7mZQzQJ3TqDEDLlLQOI9qjJk4xZ-SNZK9uJZOiRyJQ1oU8LdG0WBWxf_W3cPQ7pAa1rlF1ygS6c2aN5RYH3wBjL8KpX3NdC2aJ6UJ5gf1OI6dM3o0wPDrIb8dNT7Fq1gZMl_NKqQ6sXDK8Lj3w5BNvVOvM'
    },
    {
        name: "Do'stlik",
        region: 'Andijon viloyati',
        agents: 15,
        image: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDpkSuZdZd0HXkEhxMqX8gEMZUJJRvkZqL7R_SBxN3QqQ2qlF-H8oO-p3rZYVsXg3rQfGwLB5x-P7rEZqMBKN2DfPYu0OkUq3Z7jMZ9qQF3KqMWxZPLR4f8ZjQc7PYPWv5kXQdJ9r0YNmLvJnLQw3sPXrZ8fN6HqG1KlZdnQqYx3pQgZYJx0pXQvLm8K7zRN8sPfLqWkM0gJQp6KxYPZrM9N_Z7qQkWh5p0Lw1RNO3WLJp6XG8KvQpZJ5gWM3dPHvKf8LQR7NZYjQ'
    }
];

const AGENTS = [
    {
        id: 'ali',
        name: 'Ali Valiyev',
        rating: 4.8,
        priceMin: 35000,
        priceMax: 60000,
        badge: 'top_rated',
        online: true,
        avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuA-4mXKU91loGciYNcynW5W0szXcGke8fIG5daq5NfGfkfMdAAAjJLEzhtuoNEnKUhKoBTK97bsvZhj1QQE8L7gmbQkaovU4Y0UqOX__aUuRi-lYNP8BmP-ieznwyHxDNABqYuc0H3bshPEwKnRdxZX8Ay_0N66kLJmWGp332wNgz5BckDHwyFGh_NzVKn74hg5RRiudRCy-aYCEcRKGQkkB2lHU9ac9t02MJiNVOgbGNmkCcLSuhxQaNDm-YhJ1_4dCPCdrMPoTdY'
    },
    {
        id: 'sanjar',
        name: 'Sanjar Islomov',
        rating: 4.9,
        priceMin: 40000,
        priceMax: 65000,
        badge: 'fast_response',
        online: true,
        avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuDA5jd_af6u8rvQ-3pYCQE4HYF9sO6t19uhZ3vqyKzsYvFDZg4_sGewLg9BecZMqQAmAM9EootOyjA9MLMyvmeNd_BAbezyLTAkT9tAvKVpva0u_PqJiCwZvvT96ybFyjrNdTXQg-VbnkJ5PPRCOtalYo4DNbmpUDKuv6vYiPGDupMlEDJ2pKNIA7XVI3JY417U53DEWMv8n5S7Zm2YGvye9944PrDqpltPV5VdGpBVbxJAXuWFUileTSuMxcxEd6kb4zrw27j5d7A'
    },
    {
        id: 'nigora',
        name: 'Nigora Saidova',
        rating: 4.7,
        priceMin: 38000,
        priceMax: 62000,
        badge: 'highly_recommended',
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

// Load popular posts carousel
function loadPopularPosts() {
    const container = document.getElementById('popularPostsContainer');
    if (!container) return;

    container.innerHTML = '';

    POPULAR_POSTS.forEach(post => {
        const card = document.createElement('div');
        card.className = 'popular-post-card';
        card.innerHTML = `
            <div class="popular-post-image" style="background-image: url('${post.image}')">
                <div class="popular-post-overlay">
                    <h4 class="popular-post-name">${post.name}</h4>
                    <p class="popular-post-region">${post.region}</p>
                    <span class="popular-post-agents">${post.agents} ${t('agents_count')}</span>
                </div>
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
        const badgeText = agent.badge === 'top_rated' ? t('top_rated') :
                         agent.badge === 'fast_response' ? t('fast_response') : agent.badge;

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
                    <span>${agent.rating} • ${badgeText}</span>
                </div>
            </div>
            <button class="agent-select-btn" onclick="event.stopPropagation(); selectAgent('${agent.id}')">
                ${t('select')}
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
        tg.showAlert(t('coming_soon'));
    } else {
        alert(t('coming_soon'));
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

    counter.textContent = `${AppState.uploadedFiles.length} ${t('photos_count')}`;

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
    // Update service type
    const serviceEl = document.getElementById('sumService');
    if (serviceEl) {
        serviceEl.textContent = AppState.serviceType === 'EPI' ? 'EPI (Electronic Pre-Arrival)' : 'MB DEKLARATSIYA';
    }

    // Update other fields
    document.getElementById('sumVehicle').textContent = AppState.vehicleNumber || '-';
    document.getElementById('sumPost').textContent = AppState.selectedPost || '-';
    document.getElementById('sumDest').textContent = AppState.selectedDestination || '-';
    document.getElementById('sumAgent').textContent = getAgentName(AppState.selectedAgent);

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
        case 'agent':
            // Go to agent selection
            loadAgents();
            navigateTo('agentScreen');
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
    if (agentId === 'cash') return t('cash_payment');
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

    // Get agent info
    const agent = AGENTS.find(a => a.id === AppState.selectedAgent);
    const agentName = agent ? agent.name : (AppState.selectedAgent === 'cash' ? t('cash_payment') : '-');

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

    // Update waiting screen
    document.getElementById('waitingCode').textContent = appCode;
    document.getElementById('waitingPhotos').textContent = `${AppState.uploadedFiles.length} ta`;
    document.getElementById('waitingTime').textContent = now.toLocaleTimeString('uz', { hour: '2-digit', minute: '2-digit' });

    // Show waiting screen
    navigateTo('waitingScreen');

    // Send to Telegram bot
    if (tg) {
        try {
            tg.sendData(JSON.stringify(applicationData));
            tg.MainButton.hideProgress();
        } catch (e) {
            console.error('Error sending data:', e);
            tg.MainButton.hideProgress();
        }
    }

    // Save application locally for reference
    saveApplicationLocally(applicationData);

    // Reset flow state
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
window.selectLanguage = selectLanguage;
window.showLanguageModal = showLanguageModal;
window.clearCache = clearCache;
window.editPhone = editPhone;
window.contactAdmin = contactAdmin;
window.filterList = filterList;
window.loadAgents = loadAgents;
window.loadOfflineAgents = loadOfflineAgents;
window.toggleOfflineAgents = toggleOfflineAgents;
window.findNearestPost = findNearestPost;
window.formatPrice = formatPrice;
window.editSummaryField = editSummaryField;
window.loadPopularPosts = loadPopularPosts;
window.loadGroupedPosts = loadGroupedPosts;
window.filterBorderPosts = filterBorderPosts;
window.showMapScreen = showMapScreen;
window.switchAppsTab = switchAppsTab;
window.t = t;

console.log('CARAVAN TRANZIT Mini App v3.0 loaded with i18n support');
