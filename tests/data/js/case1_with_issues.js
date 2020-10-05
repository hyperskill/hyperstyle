function a(x) {
    var b = 10;
    if (true) {
        return x;
    } else if (false) {
        return x+1;
    } else {
        return 4;
    }
}

function sayHello(name){
    alert("Hello " + name);
}

name = "Douglas Crockford";
sayHello(name)
