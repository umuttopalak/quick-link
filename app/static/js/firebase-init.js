// Firebase configuration and initialization
let firebaseConfig = null;

// Function to fetch Firebase config from server
async function fetchFirebaseConfig() {
    try {
        const response = await fetch('/api/firebase-config');
        if (!response.ok) {
            throw new Error(`Failed to fetch Firebase config: ${response.status}`);
        }
        const config = await response.json();
        return config;
    } catch (error) {
        console.error("Error fetching Firebase config:", error);
        return null;
    }
}

// Function to dynamically load script
function loadScript(src, callback) {
    const script = document.createElement('script');
    script.src = src;
    script.async = true;
    script.defer = true;
    script.onload = callback;
    script.onerror = () => {
        console.error(`Failed to load script: ${src}`);
    };
    document.head.appendChild(script);
}

// Initialize Firebase with retry mechanism
async function initializeFirebase(retryCount = 0) {
    // Fetch config if not already fetched
    if (!firebaseConfig) {
        firebaseConfig = await fetchFirebaseConfig();
        if (!firebaseConfig) {
            console.error("Failed to get Firebase configuration from server");
            return;
        }
    }

    if (typeof firebase !== 'undefined') {
        try {
            console.log("Firebase SDK found, initializing...");
            if (!firebase.apps || !firebase.apps.length) {
                firebase.initializeApp(firebaseConfig);
                console.log("Firebase initialized successfully");
            } else {
                console.log("Firebase already initialized");
            }
        } catch (error) {
            console.error("Firebase initialization error:", error);
        }
    } else {
        if (retryCount < 3) {
            console.log(`Firebase SDK not found, loading dynamically (attempt ${retryCount + 1})...`);
            
            // Load the Firebase scripts
            loadScript("https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js", () => {
                loadScript("https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js", () => {
                    // Try to initialize again after scripts are loaded
                    setTimeout(() => {
                        initializeFirebase(retryCount + 1);
                    }, 500);
                });
            });
        } else {
            console.error("Firebase SDK could not be loaded after multiple attempts");
        }
    }
}

// Call initialization on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM loaded, checking for Firebase...");
    initializeFirebase();
});

// Google Sign In Handler with better error handling
function setupGoogleSignIn(buttonId, authEndpoint) {
    const googleBtn = document.getElementById(buttonId);
    if (!googleBtn) {
        console.error(`Google sign in button with ID '${buttonId}' not found`);
        return;
    }
    
    googleBtn.addEventListener('click', function(e) {
        console.log("Google sign in button clicked");
        e.preventDefault();
        
        // Try to initialize Firebase again just in case
        initializeFirebase();
        
        // Check if Firebase is available after a small delay
        setTimeout(() => {
            if (typeof firebase === 'undefined' || !firebase.auth) {
                console.error("Firebase or Firebase Auth not available");
                alert("Authentication service not available. Please try again later.");
                return;
            }
            
            const provider = new firebase.auth.GoogleAuthProvider();
            provider.addScope('profile');
            provider.addScope('email');
            
            firebase.auth().signInWithPopup(provider)
                .then((result) => {
                    console.log("Google sign in successful");
                    return result.user.getIdToken();
                })
                .then((idToken) => {
                    console.log("ID token obtained, sending to backend");
                    return fetch(authEndpoint, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ idToken: idToken })
                    });
                })
                .then(response => {
                    console.log("Backend response received");
                    return response.json();
                })
                .then(data => {
                    console.log("Data from backend:", data);
                    if (data.success) {
                        window.location.href = data.redirect;
                    } else {
                        alert(data.error || 'Authentication failed');
                    }
                })
                .catch((error) => {
                    console.error('Error during Google sign in:', error);
                    alert('Google authentication failed: ' + error.message);
                });
        }, 500);
    });
} 