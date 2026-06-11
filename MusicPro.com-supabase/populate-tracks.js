/**
 * Script to populate the Supabase tracks table with data from the existing tracks.js file
 * This script should be run once to migrate the existing track data to Supabase
 */

async function populateTracksTable() {
    // First, we need to get the track data from the existing file
    try {
        // Fetch the tracks.js file content
        const response = await fetch('../load-track/tracks.js');
        const jsContent = await response.text();
        
        // Create a temporary script to execute the JS and get the window.TRACKS data
        const script = document.createElement('script');
        script.textContent = jsContent.replace('window.TRACKS', 'var tempTracks');
        
        document.head.appendChild(script);
        
        // Access the tracks data
        const tracks = window.tempTracks || tempTracks;
        
        // Remove the temporary script
        document.head.removeChild(script);
        
        if (!tracks || !Array.isArray(tracks)) {
            console.error('Could not load tracks data from tracks.js');
            return;
        }
        
        console.log(`Loaded ${tracks.length} tracks from tracks.js`);
        
        // Now upload to Supabase
        if (!window.app || !window.app.supabaseIntegration || !window.app.supabaseIntegration.supabaseService) {
            console.error('Supabase service not initialized');
            return;
        }
        
        const supabaseService = window.app.supabaseIntegration.supabaseService;
        
        // Note: Actually inserting tracks into the Supabase table would require service role permissions
        // which typically isn't available from the client side for security reasons.
        // This would normally be done from a server-side script or Supabase Edge Function.
        
        console.log('Tracks data structure:');
        console.log(JSON.stringify(tracks[0], null, 2));
        
        console.log('To populate the tracks table in Supabase:');
        console.log('1. Go to your Supabase dashboard');
        console.log('2. Navigate to the SQL Editor');
        console.log('3. Run the following INSERT statements:');
        
        // Generate sample INSERT statements for the first few tracks
        const sampleTracks = tracks.slice(0, 3);
        sampleTracks.forEach(track => {
            const insertStatement = `
INSERT INTO tracks (title, artist, cover, audio_src, instrumental_src, video_src, lyric_src) VALUES (
  '${track.title.replace(/'/g, "''")}',
  '${track.artist.replace(/'/g, "''")}',
  '${track.cover ? track.cover.replace(/'/g, "''") : ''}',
  '${track.audioSrc ? track.audioSrc.replace(/'/g, "''") : ''}',
  '${track.instrumentalSrc ? track.instrumentalSrc.replace(/'/g, "''") : ''}',
  '${track.videoSrc ? track.videoSrc.replace(/'/g, "''") : ''}',
  '${track.lyricSrc ? track.lyricSrc.replace(/'/g, "''") : ''}'
);`;
            console.log(insertStatement);
        });
        
        console.log(`... and so on for all ${tracks.length} tracks.`);
        
    } catch (error) {
        console.error('Error populating tracks table:', error);
    }
}

// Function to test the new track loading from Supabase
async function testTrackLoading() {
    try {
        if (!window.app || !window.app.supabaseIntegration || !window.app.supabaseIntegration.supabaseService) {
            console.error('Supabase service not initialized');
            return;
        }
        
        console.log('Testing track loading from Supabase...');
        const tracks = await window.app.supabaseIntegration.supabaseService.loadTracks();
        console.log(`Loaded ${tracks.length} tracks from Supabase`);
        if (tracks.length > 0) {
            console.log('Sample track:', tracks[0]);
        }
        
        return tracks;
    } catch (error) {
        console.error('Error loading tracks from Supabase:', error);
        return [];
    }
}

// Expose functions globally for manual testing
window.populateTracksTable = populateTracksTable;
window.testTrackLoading = testTrackLoading;

console.log('Supabase tracks utility functions loaded. Use populateTracksTable() to see INSERT statements, or testTrackLoading() to test loading from Supabase.');