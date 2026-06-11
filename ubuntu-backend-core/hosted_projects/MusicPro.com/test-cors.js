const https = require('https');
https.get("https://github.com/d4m-dev/media/raw/main/music/cunhuvaymotvannam/cover.jpg", (res) => {
    console.log(res.headers['access-control-allow-origin']);
    console.log(res.headers.location);
});
