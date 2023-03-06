document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65432;
var server_addr = "127.0.0.1";   // the IP address of your Raspberry PI

function read_from_server() {
    console.log("reading from server");
    const net = require('net');
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        console.log('connected to server!');
    });

    client.on('data', (data) => {
        console.log(data.toString());
        obj = JSON.parse(data.toString());
        document.getElementById("speed").innerText = obj.curr_speed;
        document.getElementById("distance").innerText = obj.distance_traveled;
        document.getElementById("battery").innerText = obj.battery_percentage;
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}

function send_to_server(s) {
    const net = require('net');
    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        console.log('connected to server!');
        client.write(`${s}`);
    });

    client.on('data', (data) => {
        console.log(data.toString());
        obj = JSON.parse(data.toString());
        document.getElementById("speed").innerText = obj.curr_speed;
        document.getElementById("distance").innerText = obj.distance_traveled;
        document.getElementById("battery").innerText = obj.battery_percentage;
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {
    console.log("update key")
    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        send_to_server("87");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        send_to_server("83");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        send_to_server("65");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        send_to_server("68");
    }
}

// reset the key to the start state 
function resetKey(e) {
    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";

    send_to_server("0");
}
