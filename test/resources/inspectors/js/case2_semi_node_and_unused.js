var qqq = 10;

var readline = require('readline')
var rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.on('line', (line) => {
    let arr = [];
    if (line.trim() !== '') {
        arr = line.split(' ').map((n) => parseInt(n, 10));
    }

    console.log(sum(arr[0], arr[1]));
});

function sum(a, b) {
    return a + b;
}
