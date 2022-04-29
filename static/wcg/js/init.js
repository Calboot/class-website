var playerID = document.getElementById('getusername').innerHTML;
var ws = new WebSocket("ws://localhost:3999/");
var wsf = new WebSocket("ws://localhost:3888/");
var enemyID;

function wsSend(content) {
    if (ws.readyState === WebSocket.OPEN) {
        ws.send(content);
        console.log("已发送");
    }
}

function wsfSend(content) {
    if (wsf.readyState === WebSocket.OPEN) {
        wsf.send(content);
        console.log("已发送");
    }
}

wsf.onopen = function () {
    var message = JSON.stringify({
        'type': 'connection',
        'pid': playerID
    });
    wsfSend(message);
}

ws.onmessage = function (evt) {
    var tmp = JSON.parse(evt.data);
    a = tmp.a;
    b = tmp.b;
    d = tmp.d;
    blood = tmp.blood;
    pcd = tmp.pcd;
    pcard = tmp.pcard;
    skip = tmp.skip;
    if (tmp.lose) {
        alert("You Lose!");
        window.location.href = "index.html";
    }
    else if (tmp.win) {
        alert("You Win!");
        window.location.href = "index.html";
    }
    update();
    console.log(JSON.parse(evt.data));
}

wsf.onmessage = function (evt) {
    var tmp = JSON.parse(evt.data);
    switch (tmp.type) {
        case 'room':
            room(tmp.id);
            break;
        case 'warning':
            alert(tmp.text);
            break;
        default:
            switch (tmp.status) {
                case 'waiting':
                    waiting();
                    break;
                case 'finding':
                    finding();
                    break;
                case 'playing':
                    playing(tmp.pid, tmp.epid);
                    break;
            }
            break;
    }
}

ws.onerror = function () {
    alert("无法连接至游戏服务器");
}

ws.onclose = function () {
    alert("服务器维护中/游戏结束");
}

wsf.onerror = function () {
    alert("无法连接至匹配服务器");
}

function joinroom() {
    var rmid = document.getElementById('jroomid').value;
    var message = JSON.stringify({
        'type': 'room',
        'msgtype': 'join',
        'roomid': rmid,
        'pid': playerID
    });
    wsfSend(message);
}

function messageExit() {
    var message_exit = JSON.stringify({
        "type": "message",
        "pid": playerID,
        "epid": enemyID,
        "msgtype": "exit",
    });
    wsSend(message_exit);
    window.location.href = "index.html";
}

function messageHand(updateType, handNo) {
    var message_hand = JSON.stringify({
        "type": "message",
        "pid": playerID,
        "epid": enemyID,
        "msgtype": "updateHand",
        "updateType": updateType,
        "handNo": handNo
    });
    wsSend(message_hand);
}

function messageSkip() {
    var message_skip = JSON.stringify({
        "type": "message",
        "pid": playerID,
        "epid": enemyID,
        "msgtype": "skip"
    });
    wsSend(message_skip);
}

function usecard(num) {
    messageHand("useCard", num);
}

function playing(a, b) {
    enemyID = b;
    document.getElementById('select mode').style.display='none';
    document.getElementById('select room').style.display='none';
    wsf.close();
    var message = JSON.stringify({
        "type": "connection",
        "pid": a,
        "epid": b
    });
    wsSend(message);
    document.getElementById('playing').style.display='block';
    document.getElementById('starting').style.display='none';
}

function Joinroom(){
    document.getElementById('select room').style.display='none';
    document.getElementById('join room').style.display='block';
}

function Createroom(){
    document.getElementById('select room').style.display='none';
    document.getElementById('create room').style.display='block';
    document.getElementById('croomid').innerHTML='加载中...';
    var message = JSON.stringify({
        'type': 'room',
        'pid': playerID,
        'msgtype': 'create'
    });
    wsfSend(message);
}

function Finding(){
    document.getElementById('select mode').style.display='none';
}

function Mode(){
    document.getElementById('select room').style.display='none';
    document.getElementById('select mode').style.display='block';
}

function Room(){
    document.getElementById('select mode').style.display='none';
    document.getElementById('select room').style.display='block';
    document.getElementById('join room').style.display='none';
    document.getElementById('create room').style.display='none';
}

function room(id){
    document.getElementById('croomid').innerHTML=id;
}

function index(){
    window.location.href = "index.html";
}