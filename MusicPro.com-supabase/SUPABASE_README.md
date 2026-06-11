# Supabase Integration for Music Pro

This document explains how Supabase has been integrated into the Music Pro application.

## Overview

The Supabase integration provides:
- User authentication (email/password and anonymous)
- Cloud synchronization of user data (favorites, playlists, settings)
- Real-time database capabilities
- Secure data storage with Row Level Security (RLS)

## Files Added

### Client-side Files
- `src/supabase-config.js` - Configuration for Supabase connection
- `src/supabase-service.js` - Service layer for Supabase operations
- `src/supabase-integration.js` - Integration layer between Music Pro and Supabase
- `src/auth-ui.js` - Authentication UI components

### Server-side Files
- `supabase-schema.sql` - Database schema for Supabase

## How to Configure

1. Create a Supabase project at [supabase.io](https://supabase.io)
2. Get your Project URL and Anonymous Key from the dashboard
3. Update the configuration in `src/supabase-config.js`:

```javascript
const SUPABASE_URL = 'https://your-project-id.supabase.co';
const SUPABASE_ANON_KEY = 'your-anon-key';
```

4. Run the SQL schema in your Supabase SQL editor to create the required tables

## Features Implemented

### Authentication
- Email/password sign up and sign in
- Anonymous user accounts (for users who don't want to create an account)
- Automatic session management

### Data Synchronization
- Favorites: Sync favorite songs across devices
- Playlists: Sync custom playlists across devices  
- User settings: Sync customizations like theme, font, layout preferences
- Tracks: Load music tracks directly from Supabase database

### Offline Support
- Data is stored locally when offline
- Automatically syncs when connection is restored

## Database Schema

The integration uses three main tables:

1. `user_profiles` - Stores user preferences and settings
2. `user_playlists` - Stores user-created playlists
3. `user_favorites` - Stores user's favorite tracks

All tables have Row Level Security (RLS) enabled to ensure users can only access their own data.

## API Methods

The Supabase service provides the following methods:

### Authentication
- `signUp(email, password)` - Create a new account
- `signIn(email, password)` - Log into an existing account
- `signOut()` - Log out
- `getCurrentUser()` - Get the current user's information

### Data Operations
- `saveUserData(userId, data)` - Save user preferences
- `getUserData(userId)` - Retrieve user preferences
- `saveUserPlaylists(userId, playlists)` - Save user playlists
- `getUserPlaylists(userId)` - Retrieve user playlists
- `saveFavorites(userId, favorites)` - Save favorite tracks
- `getFavorites(userId)` - Retrieve favorite tracks
- `syncLocalDataToUser(userId)` - Sync local data to user account
- `loadTracks()` - Load music tracks from the database

## Security

- All database operations use Row Level Security
- Users can only access their own data
- Anonymous users have temporary IDs stored locally
- Data is encrypted in transit

## Error Handling

The integration includes comprehensive error handling:
- Network errors are caught and handled gracefully
- Offline mode preserves user data locally
- Sync conflicts are resolved automatically
- User-friendly error messages are displayed

## Future Enhancements

- Real-time updates when data changes on other devices
- Social features to share playlists
- Advanced analytics and recommendations
- File storage for custom avatars and music uploads