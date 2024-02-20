const fetch = require('node-fetch');
const { JSDOM, ResourceLoader } = require('jsdom');

const { window } = new JSDOM('', {
    url: 'https://discord.com',
    referrer: 'https://discord.com',
    contentType: 'text/html',
    includeNodeLocations: false,
    runScripts: 'outside-only',
    pretendToBeVisual: true,
    resources: new ResourceLoader({ agent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36' }),
});

fetch('https://newassets.hcaptcha.com/c/0fb9fb5/hsw.js')
    .then(response => response.text())
    .then(data => {
        global.window = window;
        window.eval(data);
        window.run = function(token) {
            return window.hsw(token);
        }
        window.run(process.argv[2]).then(console.log);
    })