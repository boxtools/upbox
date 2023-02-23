const readline = require('readline');
readline.emitKeypressEvents(process.stdin);
process.stdin.on('keypress', (ch, key) => {
    console.log(key.name);
    process.exit()
});
process.stdin.setRawMode(true);