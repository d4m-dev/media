// Supabase Configuration
// Replace these values with your actual Supabase project credentials
const SUPABASE_URL = 'https://tpgttyigrqjjrhqybeue.supabase.co';
const SUPABASE_PUBLIC_KEY = 'sb_publishable_05SQwoDeNHDBpjDTnoC-6A_XFuTr5jv';

// Initialize Supabase client
let supabase = null;

// Function to initialize Supabase client
function initializeSupabase() {
    // Check if the configuration values are still placeholders
    if (SUPABASE_URL.includes('YOUR_PROJECT_ID') || SUPABASE_PUBLIC_KEY.includes('YOUR_SUPABASE_PUBLIC_KEY')) {
        console.warn('Supabase configuration not found. Please update SUPABASE_URL and SUPABASE_PUBLIC_KEY with your actual project credentials.');
        return null;
    }

    // Dynamically load Supabase client if not already loaded
    if (typeof window !== 'undefined' && window.supabase) {
        // If Supabase is already loaded via CDN
        supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_PUBLIC_KEY);
    } else {
        console.warn('Supabase client not loaded. Please include the Supabase CDN script.');
    }

    return supabase;
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        SUPABASE_URL,
        SUPABASE_PUBLIC_KEY,
        initializeSupabase
    };
}