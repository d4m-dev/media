// Supabase Integration for Music Pro Application
class MusicProSupabase {
    constructor(appInstance) {
        this.app = appInstance;
        this.supabaseService = new SupabaseService();
        this.userId = null;
        this.init();
    }

    async init() {
        // Wait for Supabase service to initialize
        setTimeout(async () => {
            await this.initializeUser();
            await this.syncUserData();
        }, 1000); // Give some time for everything to load
    }

    async initializeUser() {
        try {
            // Try to get current user
            const user = await this.supabaseService.getCurrentUser();
            
            if (user) {
                this.userId = user.id;
                console.log('User authenticated:', user.id);
            } else {
                // Sign in anonymously if no user is logged in
                const anonResult = await this.supabaseService.signInAnonymously();
                this.userId = anonResult.user.id;
                console.log('Anonymous user created:', this.userId);
            }
        } catch (error) {
            console.error('Error initializing user:', error);
            // Fallback to anonymous user
            const anonResult = await this.supabaseService.signInAnonymously();
            this.userId = anonResult.user.id;
        }
    }

    async syncUserData() {
        if (!this.userId) {
            console.error('No user ID available for sync');
            return;
        }

        try {
            // Sync favorites
            const supabaseFavorites = await this.supabaseService.getFavorites(this.userId);
            if (supabaseFavorites && supabaseFavorites.length > 0) {
                // Merge with local favorites
                const localFavorites = this.app.state.favorites;
                const mergedFavorites = [...new Set([...localFavorites, ...supabaseFavorites])];
                this.app.state.favorites = mergedFavorites;
                localStorage.setItem('favorites', JSON.stringify(mergedFavorites));
            } else {
                // Save local favorites to Supabase
                const localFavorites = JSON.parse(localStorage.getItem('favorites') || '[]');
                if (localFavorites.length > 0) {
                    await this.supabaseService.saveFavorites(this.userId, localFavorites);
                }
            }

            // Sync user playlists
            const supabasePlaylists = await this.supabaseService.getUserPlaylists(this.userId);
            if (supabasePlaylists && supabasePlaylists.length > 0) {
                // Merge with local playlists
                const localPlaylists = this.app.state.userPlaylists;
                const mergedPlaylists = [...localPlaylists, ...supabasePlaylists.filter(
                    newPlaylist => !localPlaylists.some(existing => existing.id === newPlaylist.id)
                )];
                this.app.state.userPlaylists = mergedPlaylists;
                localStorage.setItem('userPlaylists', JSON.stringify(mergedPlaylists));
            } else {
                // Save local playlists to Supabase
                const localPlaylists = JSON.parse(localStorage.getItem('userPlaylists') || '[]');
                if (localPlaylists.length > 0) {
                    await this.supabaseService.saveUserPlaylists(this.userId, localPlaylists);
                }
            }

            // Sync user profile data
            const supabaseUserData = await this.supabaseService.getUserData(this.userId);
            if (supabaseUserData) {
                // Update app state with synced data
                if (supabaseUserData.customPrimaryColor) {
                    this.app.state.customPrimaryColor = supabaseUserData.customPrimaryColor;
                    localStorage.setItem('customPrimaryColor', supabaseUserData.customPrimaryColor);
                }
                if (supabaseUserData.fontFamily) {
                    this.app.state.fontFamily = supabaseUserData.fontFamily;
                    localStorage.setItem('fontFamily', supabaseUserData.fontFamily);
                }
                if (supabaseUserData.fontWeight) {
                    this.app.state.fontWeight = supabaseUserData.fontWeight;
                    localStorage.setItem('fontWeight', supabaseUserData.fontWeight);
                }
                if (supabaseUserData.layoutMode) {
                    this.app.state.layoutMode = supabaseUserData.layoutMode;
                    localStorage.setItem('layoutMode', supabaseUserData.layoutMode);
                }
                
                // Apply the synced settings
                this.app.applyColorToUIElements(supabaseUserData.customPrimaryColor);
                this.app.setFontFamily(supabaseUserData.fontFamily, supabaseUserData.fontWeight);
                this.app.setLayoutMode(supabaseUserData.layoutMode);
            } else {
                // Save current local settings to Supabase
                const userDataToSave = {
                    customPrimaryColor: this.app.state.customPrimaryColor,
                    fontFamily: this.app.state.fontFamily,
                    fontWeight: this.app.state.fontWeight,
                    layoutMode: this.app.state.layoutMode
                };
                
                if (userDataToSave.customPrimaryColor || userDataToSave.fontFamily || 
                    userDataToSave.fontWeight || userDataToSave.layoutMode) {
                    await this.supabaseService.saveUserData(this.userId, userDataToSave);
                }
            }

            console.log('User data synchronized successfully');
        } catch (error) {
            console.error('Error syncing user data:', error);
        }
    }

    // Override the toggleFavorite method to sync with Supabase
    async toggleFavorite(idx) {
        // Call the original method
        this.app.toggleFavorite(idx);
        
        // Sync to Supabase
        if (this.userId) {
            try {
                await this.supabaseService.saveFavorites(this.userId, this.app.state.favorites);
            } catch (error) {
                console.error('Error saving favorites to Supabase:', error);
            }
        }
    }

    // Override the createPlaylist method to sync with Supabase
    async createPlaylist(name, description = '', trackIndexToAdd = null) {
        // Call the original method
        this.app.createPlaylist(name, description, trackIndexToAdd);
        
        // Sync to Supabase
        if (this.userId) {
            try {
                await this.supabaseService.saveUserPlaylists(this.userId, this.app.state.userPlaylists);
            } catch (error) {
                console.error('Error saving playlists to Supabase:', error);
            }
        }
    }

    // Override the deletePlaylist method to sync with Supabase
    async deletePlaylist(index) {
        // Call the original method
        this.app.deletePlaylist(index);
        
        // Sync to Supabase
        if (this.userId) {
            try {
                await this.supabaseService.saveUserPlaylists(this.userId, this.app.state.userPlaylists);
            } catch (error) {
                console.error('Error saving playlists to Supabase:', error);
            }
        }
    }

    // Override the updatePlaylist method to sync with Supabase
    async updatePlaylist(index, name, description) {
        // Call the original method
        this.app.updatePlaylist(index, name, description);
        
        // Sync to Supabase
        if (this.userId) {
            try {
                await this.supabaseService.saveUserPlaylists(this.userId, this.app.state.userPlaylists);
            } catch (error) {
                console.error('Error saving playlists to Supabase:', error);
            }
        }
    }

    // Override the setCustomPrimaryColor method to sync with Supabase
    async setCustomPrimaryColor(color) {
        // Call the original method
        this.app.setCustomPrimaryColor(color);
        
        // Sync to Supabase
        if (this.userId) {
            try {
                const userData = await this.supabaseService.getUserData(this.userId) || {};
                userData.customPrimaryColor = color;
                await this.supabaseService.saveUserData(this.userId, userData);
            } catch (error) {
                console.error('Error saving user data to Supabase:', error);
            }
        }
    }

    // Override the setFontFamily method to sync with Supabase
    async setFontFamily(fontFamily, fontWeight = '400') {
        // Call the original method
        this.app.setFontFamily(fontFamily, fontWeight);
        
        // Sync to Supabase
        if (this.userId) {
            try {
                const userData = await this.supabaseService.getUserData(this.userId) || {};
                userData.fontFamily = fontFamily;
                userData.fontWeight = fontWeight;
                await this.supabaseService.saveUserData(this.userId, userData);
            } catch (error) {
                console.error('Error saving user data to Supabase:', error);
            }
        }
    }

    // Override the setLayoutMode method to sync with Supabase
    async setLayoutMode(layoutMode) {
        // Call the original method
        this.app.setLayoutMode(layoutMode);
        
        // Sync to Supabase
        if (this.userId) {
            try {
                const userData = await this.supabaseService.getUserData(this.userId) || {};
                userData.layoutMode = layoutMode;
                await this.supabaseService.saveUserData(this.userId, userData);
            } catch (error) {
                console.error('Error saving user data to Supabase:', error);
            }
        }
    }

    // Helper to translate Supabase errors to Vietnamese
    translateError(message) {
        const errors = {
            'Invalid login credentials': 'Thông tin đăng nhập không chính xác',
            'User already registered': 'Email đã được đăng ký',
            'Password should be at least 6 characters': 'Mật khẩu phải có ít nhất 6 ký tự',
            'Email not confirmed': 'Email chưa được xác nhận',
            'User not found': 'Không tìm thấy người dùng'
        };
        for (const [key, value] of Object.entries(errors)) {
            if (message.includes(key)) return value;
        }
        return message;
    }

    // Method to handle user login
    async handleLogin(email, password) {
        try {
            const result = await this.supabaseService.signIn(email, password);
            
            if (result && result.user) {
                this.userId = result.user.id;
                
                // Sync local data to the authenticated account
                await this.supabaseService.syncLocalDataToUser(this.userId);
                
                // Reload user data from Supabase
                await this.syncUserData();
                
                this.app.showToast('Đăng nhập thành công!');
                return true;
            }
        } catch (error) {
            console.error('Login error:', error);
            this.app.showToast('Đăng nhập thất bại: ' + this.translateError(error.message));
            return false;
        }
    }

    // Method to handle user signup
    async handleSignup(email, password) {
        try {
            const result = await this.supabaseService.signUp(email, password);
            
            if (result && result.user) {
                this.userId = result.user.id;
                
                // Sync local data to the new account
                await this.supabaseService.syncLocalDataToUser(this.userId);
                
                this.app.showToast('Đăng ký thành công!');
                return true;
            }
        } catch (error) {
            console.error('Signup error:', error);
            this.app.showToast('Đăng ký thất bại: ' + this.translateError(error.message));
            return false;
        }
    }

    // Method to handle logout
    async handleLogout() {
        try {
            await this.supabaseService.signOut();
            this.userId = null;
            
            // Create new anonymous user
            const anonResult = await this.supabaseService.signInAnonymously();
            this.userId = anonResult.user.id;
            
            this.app.showToast('Đã đăng xuất!');
        } catch (error) {
            console.error('Logout error:', error);
            this.app.showToast('Đăng xuất thất bại: ' + this.translateError(error.message));
        }
    }
}

// Extend the original MusicPro class to include Supabase functionality
class ExtendedMusicPro extends MusicPro {
    constructor() {
        super();
        this.supabaseIntegration = new MusicProSupabase(this);
    }

    // Override methods to include Supabase sync
    toggleFavorite(idx) {
        this.supabaseIntegration.toggleFavorite(idx);
    }

    createPlaylist(name, description = '', trackIndexToAdd = null) {
        this.supabaseIntegration.createPlaylist(name, description, trackIndexToAdd);
    }

    deletePlaylist(index) {
        this.supabaseIntegration.deletePlaylist(index);
    }

    updatePlaylist(index, name, description) {
        this.supabaseIntegration.updatePlaylist(index, name, description);
    }

    setCustomPrimaryColor(color) {
        this.supabaseIntegration.setCustomPrimaryColor(color);
    }

    setFontFamily(fontFamily, fontWeight = '400') {
        this.supabaseIntegration.setFontFamily(fontFamily, fontWeight);
    }

    setLayoutMode(layoutMode) {
        this.supabaseIntegration.setLayoutMode(layoutMode);
    }
    
    // Add login/signup/logout methods to the main app
    async login(email, password) {
        return await this.supabaseIntegration.handleLogin(email, password);
    }
    
    async signup(email, password) {
        return await this.supabaseIntegration.handleSignup(email, password);
    }
    
    async logout() {
        return await this.supabaseIntegration.handleLogout();
    }
}