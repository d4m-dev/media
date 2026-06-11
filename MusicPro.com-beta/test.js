const { JSDOM } = require('jsdom');
const dom = new JSDOM();
const video = dom.window.document.createElement('video');
try {
  video.currentTime = 10;
  console.log('Success');
} catch (e) {
  console.log('Error:', e.name, e.message);
}
