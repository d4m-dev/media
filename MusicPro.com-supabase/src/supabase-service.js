// Supabase Service for Music Pro Application
class SupabaseService {
    constructor() {
        this.supabase = null;
        this.initialized = false;
        this.init();
    }

    async init() {
        // Wait for the DOM to be ready and Supabase script to be loaded
        if (typeof window !== 'undefined' && window.supabase) {
            const config = await this.loadConfig();
            this.supabase = window.supabase.createClient(config.SUPABASE_URL, config.SUPABASE_ANON_KEY);
            this.initialized = true;
            console.log('Dịch vụ Supabase đã được khởi tạo thành công');
        } else {
            console.error('Client Supabase không khả dụng. Vui lòng đảm bảo script CDN Supabase đã được tải.');
        }
    }

    async loadConfig() {
        // In a real implementation, this would come from environment variables or a config file
        // For now, we'll return the values from the config file
        return {
            SUPABASE_URL: 'https://tpgttyigrqjjrhqybeue.supabase.co',
            SUPABASE_ANON_KEY: 'sb_publishable_05SQwoDeNHDBpjDTnoC-6A_XFuTr5jv'
        };
    }

    // Authentication methods
    async signUp(email, password) {
        if (!this.initialized) {
            await this.init();
        }
        
        try {
            const { data, error } = await this.supabase.auth.signUp({
                email,
                password,
            });
            
            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Lỗi đăng ký:', error.message);
            throw error;
        }
    }

    async signIn(email, password) {
        if (!this.initialized) {
            await this.init();
        }
        
        try {
            const { data, error } = await this.supabase.auth.signInWithPassword({
                email,
                password,
            });
            
            if (error) throw error;
            return data;
        } catch (error) {
            console.error('Lỗi đăng nhập:', error.message);
            throw error;
        }
    }

    async signInAnonymously() {
        if (!this.initialized) {
            await this.init();
        }
        
        try {
            // Generate a random identifier for anonymous users
            const randomId = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
            
            // Store the anonymous ID in localStorage
            localStorage.setItem('anonymous_user_id', randomId);
            
            return { user: { id: randomId, email: null, isAnonymous: true } };
        } catch (error) {
            console.error('Lỗi đăng nhập ẩn danh:', error.message);
            throw error;
        }
    }

    async signOut() {
        if (!this.initialized) {
            await this.init();
        }
        
        try {
            const { error } = await this.supabase.auth.signOut();
            if (error) throw error;
            
            // Clear anonymous user ID if exists
            localStorage.removeItem('anonymous_user_id');
            
            return true;
        } catch (error) {
            console.error('Lỗi đăng xuất:', error.message);
            throw error;
        }
    }

    async getCurrentUser() {
        if (!this.initialized) {
            await this.init();
        }
        
        try {
            const { data: { user }, error } = await this.supabase.auth.getUser();
            
            if (error) {
                // Check if there's an anonymous user
                const anonymousId = localStorage.getItem('anonymous_user_id');
                if (anonymousId) {
                    return { id: anonymousId, email: null, isAnonymous: true };
                }
                throw error;
            }
            
            return user;
        } catch (error) {
            console.error('Lỗi lấy thông tin người dùng:', error.message);
            // Return anonymous user if available
            const anonymousId = localStorage.getItem('anonymous_user_id');
            if (anonymousId) {
                return { id: anonymousId, email: null, isAnonymous: true };
            }
            return null;
        }
    }

    // Database methods for user data
    async saveUserData(userId, data) {
        if (!this.initialized) {
            await this.init();
        }
        
        try {
            // Check if user is anonymous
            const isAnonymous = localStorage.getItem('anonymous_user_id') === userId;
            
            if (isAnonymous) {
                // For anonymous users, store in localStorage
                localStorage.setItem('user_data', JSON.stringify(data));
                return { success: true, data: { id: userId } };
            }
            
            // For authenticated users, store in Supabase
            const { data: result, error } = await this.supabase
                .from('user_profiles')
                .upsert({ user_id: userId, ...data }, { onConflict: 'user_id' });
                
            if (error) throw error;
            return { success: true, data: result };
        } catch (error) {
            console.error('Lỗi lưu dữ liệu người dùng:', error.message);
            throw error;
        }
    }

    async getUserData(userId) {
        if (!this.initialized) {
            await this.init();
        }
        
        try {
            // Check if user is anonymous
            const isAnonymous = localStorage.getItem('anonymous_user_id') === userId;
            
            if (isAnonymous) {
                // For anonymous users, retrieve from localStorage
                const userData = localStorage.getItem('user_data');
                return userData ? JSON.parse(userData) : null;
            }
            
            // For authenticated users, retrieve from Supabase
            const { data, error } = await this.supabase
                .from('user_profiles')
                .select('*')
                .eq('user_id', userId)
                .single();
                
            if (error) {
                if (error.code === 'PGRST116') {
                    // Record not found, return null
                    return null;
                }
                throw error;
            }
            
            return data;
        } catch (error) {
            console.error('Lỗi lấy dữ liệu người dùng:', error.message);
            return null;
        }
    }

    // Methods for managing user playlists
    async saveUserPlaylists(userId, playlists) {
        if (!this.initialized) {
            await this.init();
        }
        
        try {
            // Check if user is anonymous
            const isAnonymous = localStorage.getItem('anonymous_user_id') === userId;
            
            if (isAnonymous) {
                // For anonymous users, store in localStorage
                localStorage.setItem('user_playlists', JSON.stringify(playlists));
                return { success: true };
            }
            
            // For authenticated users, store in Supabase
            const { data: result, error } = await this.supabase
                .from('user_playlists')
                .upsert({ user_id: userId, playlists }, { onConflict: 'user_id' });
                
            if (error) throw error;
            return { success: true, data: result };
        } catch (error) {
            console.error('Lỗi lưu danh sách phát:', error.message);
            throw error;
        }
    }

    async getUserPlaylists(userId) {
        if (!this.initialized) {
            await this.init();
        }
        
        try {
            // Check if user is anonymous
            const isAnonymous = localStorage.getItem('anonymous_user_id') === userId;
            
            if (isAnonymous) {
                // For anonymous users, retrieve from localStorage
                const playlists = localStorage.getItem('user_playlists');
                return playlists ? JSON.parse(playlists) : [];
            }
            
            // For authenticated users, retrieve from Supabase
            const { data, error } = await this.supabase
                .from('user_playlists')
                .select('playlists')
                .eq('user_id', userId)
                .single();
                
            if (error) {
                if (error.code === 'PGRST116') {
                    // Record not found, return empty array
                    return [];
                }
                throw error;
            }
            
            return data.playlists || [];
        } catch (error) {
            console.error('Lỗi lấy danh sách phát:', error.message);
            return [];
        }
    }

    // Methods for managing favorites
    async saveFavorites(userId, favorites) {
        if (!this.initialized) {
            await this.init();
        }
        
        try {
            // Check if user is anonymous
            const isAnonymous = localStorage.getItem('anonymous_user_id') === userId;
            
            if (isAnonymous) {
                // For anonymous users, store in localStorage
                localStorage.setItem('favorites', JSON.stringify(favorites));
                return { success: true };
            }
            
            // For authenticated users, store in Supabase
            const { data: result, error } = await this.supabase
                .from('user_favorites')
                .upsert({ user_id: userId, favorites }, { onConflict: 'user_id' });
                
            if (error) throw error;
            return { success: true, data: result };
        } catch (error) {
            console.error('Lỗi lưu yêu thích:', error.message);
            throw error;
        }
    }

    async getFavorites(userId) {
        if (!this.initialized) {
            await this.init();
        }
        
        try {
            // Check if user is anonymous
            const isAnonymous = localStorage.getItem('anonymous_user_id') === userId;
            
            if (isAnonymous) {
                // For anonymous users, retrieve from localStorage
                const favorites = localStorage.getItem('favorites');
                return favorites ? JSON.parse(favorites) : [];
            }
            
            // For authenticated users, retrieve from Supabase
            const { data, error } = await this.supabase
                .from('user_favorites')
                .select('favorites')
                .eq('user_id', userId)
                .single();
                
            if (error) {
                if (error.code === 'PGRST116') {
                    // Record not found, return empty array
                    return [];
                }
                throw error;
            }
            
            return data.favorites || [];
        } catch (error) {
            console.error('Lỗi lấy yêu thích:', error.message);
            return [];
        }
    }

    // Method to load tracks from Supabase
    async loadTracks() {
        if (!this.initialized) {
            await this.init();
        }
        
        try {
            // Query all tracks from the database
            const { data, error } = await this.supabase
                .from('tracks')
                .select('*')
                .order('id', { ascending: true });
                
            if (error) throw error;
            
            // Transform the data to match the expected format
            const normalizedTracks = data.map(track => ({
                id: track.id,
                title: track.title,
                artist: track.artist,
                cover: track.cover,
                audioSrc: track.audio_src,
                instrumental: track.instrumental_src,
                vid: track.video_src,
                lyric: track.lyric_src
            }));
            
            return normalizedTracks;
        } catch (error) {
            console.error('Lỗi tải bài hát:', error.message);
            return [];
        }
    }

    // Method to sync local data with Supabase when user logs in
    async syncLocalDataToUser(userId) {
        if (!this.initialized) {
            await this.init();
        }
        
        try {
            // Retrieve local data
            const localPlaylists = JSON.parse(localStorage.getItem('user_playlists') || '[]');
            const localFavorites = JSON.parse(localStorage.getItem('favorites') || '[]');
            const localUserData = JSON.parse(localStorage.getItem('user_data') || '{}');
            
            // Save to Supabase
            await this.saveUserPlaylists(userId, localPlaylists);
            await this.saveFavorites(userId, localFavorites);
            await this.saveUserData(userId, localUserData);
            
            // Clear local storage after sync
            localStorage.removeItem('user_playlists');
            localStorage.removeItem('favorites');
            localStorage.removeItem('user_data');
            
            return { success: true };
        } catch (error) {
            console.error('Lỗi đồng bộ dữ liệu:', error.message);
            throw error;
        }
    }
}

// Export the service
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SupabaseService;
} else if (typeof window !== 'undefined') {
    window.SupabaseService = SupabaseService;
}