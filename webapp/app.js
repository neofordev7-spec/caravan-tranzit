// ==========================================
// CARAVAN TRANZIT Web App - Main JavaScript
// ==========================================

// Telegram Web App API
const tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

// Application State
const appState = {
    currentScreen: 'dashboard',
    userData: {
        name: 'Jasur Rakhimov',
        balance: 35000
    },
    formData: {
        post_id: null,
        post_name: '',
        agent_id: null,
        agent_name: '',
        vehicle_number: '',
        vehicle_type: 'truck',
        documents: {
            passport: null,
            techPassport: null,
            invoice: null
        },
        payment_method: 'click'
    }
};

// Border Posts Data
const BORDER_POSTS = [
    { id: 1, name: "Yallama", distance: "12km away", popular: true },
    { id: 2, name: "Olot", distance: "240km away", popular: true },
    { id: 3, name: "Alat", distance: "310km away", popular: true },
    { id: 4, name: "Doʻstlik", distance: "180km away", popular: false },
    { id: 5, name: "Oybek", distance: "95km away", popular: false }
];

// Test Agents (will be fetched from API in production)
const AGENTS_BY_POST = {
    1: [
        { id: 1, name: "Aziz Rakhimov", rating: 4.9, reviews: 124, status: 'online' },
        { id: 2, name: "Dilshod Aliyev", rating: 4.5, reviews: 45, status: 'online' }
    ],
    2: [
        { id: 3, name: "Sardor Karimov", rating: 4.8, reviews: 89, status: 'online' }
    ],
    3: [
        { id: 4, name: "Jahongir Rahimov", rating: 4.7, reviews: 67, status: 'offline' }
    ]
};

// ==========================================
// INITIALIZATION
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    loadUserData();
});

function initializeApp() {
    console.log('CARAVAN TRANZIT Web App initialized');
    tg.setHeaderColor('#F5F7FA');
    tg.setBackgroundColor('#F5F7FA');
}

function loadUserData() {
    // Get user data from Telegram
    const user = tg.initDataUnsafe?.user;
    if (user) {
        const fullName = `${user.first_name} ${user.last_name || ''}`.trim();
        appState.userData.name = fullName;
        document.getElementById('user-name').textContent = fullName;
    }

    // Load balance (could come from URL param or API)
    const urlParams = new URLSearchParams(window.location.search);
    const balance = urlParams.get('balance');
    if (balance) {
        appState.userData.balance = parseInt(balance);
        document.getElementById('wallet-balance').textContent = formatNumber(balance);
    }
}

// ==========================================
// EVENT LISTENERS SETUP
// ==========================================
function setupEventListeners() {
    // Dashboard
    document.getElementById('btn-new-declaration').addEventListener('click', () => {
        navigateToScreen('step1');
    });

    // Step 1: Location & Agent
    document.getElementById('btn-back-step1').addEventListener('click', () => {
        navigateToScreen('dashboard');
    });
    document.getElementById('btn-next-step1').addEventListener('click', () => {
        if (validateStep1()) {
            navigateToScreen('step2');
        }
    });
    loadBorderPosts();

    // Step 2: Vehicle Information
    document.getElementById('btn-back-step2').addEventListener('click', () => {
        navigateToScreen('step1');
    });
    document.getElementById('btn-next-step2').addEventListener('click', () => {
        if (validateStep2()) {
            navigateToScreen('step3');
        }
    });
    setupVehicleInputs();

    // Step 3: Document Upload
    document.getElementById('btn-back-step3').addEventListener('click', () => {
        navigateToScreen('step2');
    });
    document.getElementById('btn-next-step3').addEventListener('click', () => {
        if (validateStep3()) {
            navigateToScreen('payment');
        }
    });
    setupDocumentUpload();

    // Payment Screen
    document.getElementById('btn-back-payment').addEventListener('click', () => {
        navigateToScreen('step3');
    });
    document.getElementById('btn-submit-payment').addEventListener('click', handleFinalSubmit);
    setupPaymentMethods();

    // Navigation Bar
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            const nav = e.currentTarget.dataset.nav;
            if (nav === 'home') {
                navigateToScreen('dashboard');
            } else {
                tg.showAlert(`${nav.charAt(0).toUpperCase() + nav.slice(1)} feature coming soon!`);
            }
        });
    });

    // Telegram Back Button
    tg.BackButton.onClick(() => {
        handleBackNavigation();
    });
}

// ==========================================
// NAVIGATION
// ==========================================
function navigateToScreen(screenName) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });

    // Show target screen
    const targetScreen = document.getElementById(`screen-${screenName}`);
    if (targetScreen) {
        targetScreen.classList.add('active');
        appState.currentScreen = screenName;

        // Show/hide navigation bar (only visible on dashboard)
        const navBar = document.getElementById('nav-bar');
        navBar.style.display = (screenName === 'dashboard') ? 'flex' : 'none';

        // Update Telegram back button
        if (screenName === 'dashboard') {
            tg.BackButton.hide();
        } else {
            tg.BackButton.show();
        }

        // Scroll to top
        window.scrollTo(0, 0);
    }
}

function handleBackNavigation() {
    const navigationMap = {
        'step1': 'dashboard',
        'step2': 'step1',
        'step3': 'step2',
        'payment': 'step3',
        'dashboard': null
    };

    const previousScreen = navigationMap[appState.currentScreen];
    if (previousScreen) {
        navigateToScreen(previousScreen);
    } else {
        tg.close();
    }
}

// ==========================================
// STEP 1: LOCATION & AGENT SELECTION
// ==========================================
function loadBorderPosts() {
    const postsList = document.getElementById('posts-list');
    const popularPosts = BORDER_POSTS.filter(p => p.popular);

    popularPosts.forEach(post => {
        const card = createPostCard(post);
        postsList.appendChild(card);
    });
}

function createPostCard(post) {
    const card = document.createElement('div');
    card.className = 'selection-card';
    card.innerHTML = `
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
                    📍
                </div>
                <div>
                    <p class="font-semibold">${post.name}</p>
                    <p class="text-sm text-gray-500">✈️ ${post.distance}</p>
                </div>
            </div>
            <div class="radio-dot"></div>
        </div>
    `;

    card.addEventListener('click', () => selectPost(post, card));
    return card;
}

function selectPost(post, cardElement) {
    // Deselect all posts
    document.querySelectorAll('#posts-list .selection-card').forEach(card => {
        card.classList.remove('selected');
    });

    // Select this post
    cardElement.classList.add('selected');
    appState.formData.post_id = post.id;
    appState.formData.post_name = post.name;

    // Load agents for this post
    loadAgents(post.id);
}

function loadAgents(postId) {
    const agentsSection = document.getElementById('agents-section');
    const agentsList = document.getElementById('agents-list');

    agentsList.innerHTML = '';
    const agents = AGENTS_BY_POST[postId] || [];
    const onlineAgents = agents.filter(a => a.status === 'online');

    if (onlineAgents.length > 0) {
        agentsSection.style.display = 'block';

        onlineAgents.forEach(agent => {
            const card = createAgentCard(agent);
            agentsList.appendChild(card);
        });
    } else {
        agentsSection.style.display = 'none';
    }

    // Disable next button until agent is selected
    document.getElementById('btn-next-step1').disabled = true;
}

function createAgentCard(agent) {
    const card = document.createElement('div');
    card.className = 'selection-card';
    card.innerHTML = `
        <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-xl">
                    👤
                </div>
                <div>
                    <div class="flex items-center gap-2 mb-1">
                        <p class="font-semibold">${agent.name}</p>
                        <span class="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">ONLINE</span>
                    </div>
                    <p class="text-sm text-gray-600">⭐ ${agent.rating} (${agent.reviews} reviews)</p>
                </div>
            </div>
            <div class="radio-dot"></div>
        </div>
    `;

    card.addEventListener('click', () => selectAgent(agent, card));
    return card;
}

function selectAgent(agent, cardElement) {
    // Deselect all agents
    document.querySelectorAll('#agents-list .selection-card').forEach(card => {
        card.classList.remove('selected');
    });

    // Select this agent
    cardElement.classList.add('selected');
    appState.formData.agent_id = agent.id;
    appState.formData.agent_name = agent.name;

    // Enable next button
    document.getElementById('btn-next-step1').disabled = false;
}

function validateStep1() {
    return appState.formData.post_id && appState.formData.agent_id;
}

// ==========================================
// STEP 2: VEHICLE INFORMATION
// ==========================================
function setupVehicleInputs() {
    const vehicleInput = document.getElementById('vehicle-number');

    // Auto-format license plate
    vehicleInput.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\s+/g, '').toUpperCase();

        // Format: 01 A 777 AA
        let formatted = '';
        if (value.length >= 2) {
            formatted = value.slice(0, 2);
            if (value.length > 2) formatted += ' ' + value.slice(2, 3);
            if (value.length > 3) formatted += ' ' + value.slice(3, 6);
            if (value.length > 6) formatted += ' ' + value.slice(6, 8);
        } else {
            formatted = value;
        }

        e.target.value = formatted;
        appState.formData.vehicle_number = value.replace(/\s+/g, '');
        validateStep2();
    });

    // Vehicle type selection
    const typeTruck = document.getElementById('type-truck');
    const typeCar = document.getElementById('type-car');

    typeTruck.addEventListener('click', () => {
        typeTruck.classList.add('selected');
        typeCar.classList.remove('selected');
        appState.formData.vehicle_type = 'truck';
        validateStep2();
    });

    typeCar.addEventListener('click', () => {
        typeCar.classList.add('selected');
        typeTruck.classList.remove('selected');
        appState.formData.vehicle_type = 'car';
        validateStep2();
    });
}

function validateStep2() {
    const isValid = appState.formData.vehicle_number.length >= 7;
    document.getElementById('btn-next-step2').disabled = !isValid;
    return isValid;
}

// ==========================================
// STEP 3: DOCUMENT UPLOAD
// ==========================================
function setupDocumentUpload() {
    setupSingleDocumentUpload('passport', 'passport-input', 'passport-upload', 'passport-preview');
    setupSingleDocumentUpload('techPassport', 'tech-passport-input', 'tech-passport-upload', 'tech-passport-preview');
    setupSingleDocumentUpload('invoice', 'invoice-input', 'invoice-upload', 'invoice-preview');
}

function setupSingleDocumentUpload(docType, inputId, uploadZoneId, previewId) {
    const input = document.getElementById(inputId);
    const uploadZone = document.getElementById(uploadZoneId);
    const preview = document.getElementById(previewId);

    uploadZone.addEventListener('click', () => input.click());

    input.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (file) {
            if (!file.type.startsWith('image/')) {
                tg.showAlert('Please upload an image file');
                return;
            }

            if (file.size > 10 * 1024 * 1024) {
                tg.showAlert('File size must be less than 10MB');
                return;
            }

            // Convert to base64
            const base64 = await fileToBase64(file);
            appState.formData.documents[docType] = {
                name: file.name,
                type: file.type,
                size: file.size,
                data: base64
            };

            // Show preview
            uploadZone.style.display = 'none';
            preview.style.display = 'block';
            preview.innerHTML = `
                <div class="doc-preview flex items-center gap-3">
                    <img src="${base64}" alt="${docType}">
                    <div class="flex-1">
                        <p class="font-semibold flex items-center gap-2">
                            ${getDocumentTitle(docType)}
                            <span class="text-green-600">✓</span>
                        </p>
                        <p class="text-sm text-gray-500">${file.name}</p>
                    </div>
                    <button class="remove-btn" onclick="removeDocument('${docType}', '${uploadZoneId}', '${previewId}')">
                        ×
                    </button>
                </div>
            `;

            validateStep3();
        }
    });
}

function getDocumentTitle(docType) {
    const titles = {
        passport: 'Passport',
        techPassport: 'Tech Passport',
        invoice: 'Invoice'
    };
    return titles[docType] || docType;
}

window.removeDocument = function(docType, uploadZoneId, previewId) {
    appState.formData.documents[docType] = null;
    document.getElementById(uploadZoneId).style.display = 'block';
    document.getElementById(previewId).style.display = 'none';
    document.getElementById(previewId).innerHTML = '';
    validateStep3();
};

function validateStep3() {
    const { passport, techPassport, invoice } = appState.formData.documents;
    const isValid = passport && techPassport && invoice;
    document.getElementById('btn-next-step3').disabled = !isValid;
    return isValid;
}

// ==========================================
// PAYMENT SCREEN
// ==========================================
function setupPaymentMethods() {
    document.querySelectorAll('.payment-method').forEach(method => {
        method.addEventListener('click', (e) => {
            // Deselect all
            document.querySelectorAll('.payment-method').forEach(m => {
                m.classList.remove('selected');
            });

            // Select this one
            e.currentTarget.classList.add('selected');
            appState.formData.payment_method = e.currentTarget.dataset.method;
        });
    });
}

// ==========================================
// FINAL SUBMISSION
// ==========================================
async function handleFinalSubmit() {
    try {
        // Show loading
        const btn = document.getElementById('btn-submit-payment');
        btn.disabled = true;
        btn.innerHTML = '⏳ Processing...';

        // Prepare payload for Telegram
        const payload = {
            post: {
                id: appState.formData.post_id,
                name: appState.formData.post_name
            },
            agent: {
                id: appState.formData.agent_id,
                name: appState.formData.agent_name
            },
            vehicle: {
                number: appState.formData.vehicle_number,
                type: appState.formData.vehicle_type
            },
            payment_method: appState.formData.payment_method,
            documents_count: 3,
            timestamp: Date.now()
        };

        // Note: Large files (base64) cannot be sent via sendData
        // In production, files should be uploaded to server first,
        // then send file URLs/IDs to bot

        console.log('Submitting declaration:', payload);

        // Send to Telegram bot
        tg.sendData(JSON.stringify(payload));

        // Show success and close
        setTimeout(() => {
            tg.close();
        }, 500);

    } catch (error) {
        console.error('Submission error:', error);
        tg.showAlert('An error occurred. Please try again.');

        // Reset button
        const btn = document.getElementById('btn-submit-payment');
        btn.disabled = false;
        btn.innerHTML = 'Proceed to Payment';
    }
}

// ==========================================
// UTILITY FUNCTIONS
// ==========================================
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

// ==========================================
// SEARCH FUNCTIONALITY (Optional Enhancement)
// ==========================================
const searchInput = document.getElementById('search-post');
if (searchInput) {
    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        document.querySelectorAll('#posts-list .selection-card').forEach(card => {
            const text = card.textContent.toLowerCase();
            card.style.display = text.includes(query) ? 'block' : 'none';
        });
    });
}

// ==========================================
// DEBUG HELPERS
// ==========================================
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('🔧 Debug mode enabled');
    window.appState = appState;
    window.navigateToScreen = navigateToScreen;
}
