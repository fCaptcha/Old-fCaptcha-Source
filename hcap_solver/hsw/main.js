const { readFile } = require('fs').promises;
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

readFile(`${__dirname}/hsw.js`, 'utf-8').then(hsw => {
    global.window = window;
    window.eval(hsw);
    window.test(process.argv[2]).then(console.log);
});