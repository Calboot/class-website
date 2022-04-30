console.log("服务器启动中...");
const ws = require('ws').Server;
const WebSocket = require('ws');
const PORT = 3999;
const wss = new ws({ port: PORT });
const cards = 28;
const cardcost = [0,1,1,2,8,4,6,3,5,2,3,2,1,4,2,2,7,4,4,3,5,2,4,3,1,2,1,4,3];//卡牌消费
const pa = [0,1,1,4,8,3,4,3,1,2,5,3,1,1,4,1,12,3,1,2,3,3,3,1,1,2,1,2,3]; //卡牌提供的a
const pb = [0,1,1,1,0,2,2,1,4,1,2,2,1,1,4,1,21,2,2,2,3,2,3,5,2,2,1,2,3]; 
const mnum = 8;
const snum = 4;//卡牌提供的b
const monkeys = [7,9,13,20,21,22,23,24],spiders = [1,25,26,27];
console.log("服务器启动成功！");

var players = [];
var playersws = [];
var playersIndex = -1;

function wsSend(pid, content) {
    // console.log('playersws');
    // console.log(playersws);
    for (var i = 0; i <= playersIndex; i++) {
        if (players[i].pid == pid) {
            var clientSocket = playersws[i].ws;
            if (clientSocket.readyState == WebSocket.OPEN) {
                console.log(content);
                clientSocket.send(JSON.stringify(content));
            }
        }
    }
}

function find(pid){
    for (var i = 0; i <= playersIndex; i++){
        if (players[i].pid == pid) return i;
    }
}

function pop(pos, pid) { //将第pos张卡牌从玩家手中移除
    for (var i = 0; i <= playersIndex; i++) {
        if (players[i].pid == pid) {
            if (players[i].pcard == 0 || pos > players[i].pcard) return;
            for (var j = pos; j < players[i].pcard; j++) {
                players[i].pcd[j] = players[i].pcd[j + 1];
            }
            players[i].pcard -= 1;
            players[i].pcd[players[i].pcard + 1] = 0;
            return;
        }
    }
}

function inc(num, pid) {
    for (var i = 0; i <= playersIndex; i++) {
        if (players[i].pid == pid) {
            if (players[i].pcard >= 6) return;
            players[i].pcard += 1;
            players[i].pcd[players[i].pcard] = num;
            return;
        }
    }
}

function ismonk(num, pid) {
    for (var i = 0; i <= playersIndex; i++) {
        if (players[i].pid == pid) {
            for (var j = 0; j < mnum; j++) if (monkeys[j] == num) return true;
            return false;
        }

    }
}

function issipder(num, pid) {
    for (var i = 0; i <= playersIndex; i++) {
        if (players[i].pid == pid) {
            for (var j = 0; j < snum; j++) if (spiders[j] == num) return true;
            return false;
        }
    }
}

function empty(pid) { //判断牌库是否空了
    for (var i = 0; i <= playersIndex; i++) {
        if (players[i].pid == pid) {
            for (var j = 1; j <= cards; j++) if (players[i].had[j] < 2) return false;
            return true;
        }
    }
}

function getcard(pid) { //摸一张牌
    for (var i = 0; i <= playersIndex; i++) {
        if (players[i].pid == pid) {
            if (players[i].pcard == 6) {
                return;
            }
            if (empty(pid)) {
                return;
            }
            players[i].pcard += 1;
            while (players[i].had[players[i].pcd[players[i].pcard]] == 2) {
                players[i].pcd[players[i].pcard] = Math.floor(Math.random() * cards) + 1;
            }
            players[i].had[players[i].pcd[players[i].pcard]] += 1;//记录
        }
    }
}

function acticard(num, pid) {
    for (var i = 0; i <= playersIndex; i++) {
        if (pid == players[i].pid) {
            players[i].a += pa[players[i].pcd[num]];
            players[i].b += pb[players[i].pcd[num]];
            if (ismonk(players[i].pcd[num])) players[i].monk++;
            if (issipder(players[i].pcd[num])) players[i].spid++;
            if (players[i].pcd[num] == 1) {
                pop(num, pid);
                if (Math.ceil(Math.random() * 10) == 2) {
                    players[i].pcard += 1;
                    players[i].pcd[players[i].pcard] = 1;
                }
                return;
            }
            if (players[i].pcd[num] == 2) {
                pop(num, pid);
                players[i].had[2]--;
                return;
            }
            if (players[i].pcd[num] == 5) { //如果是仓王，则交换a，b
                pop(num, pid);
                var tmp = players[i].a;
                players[i].a = players[i].b;
                players[i].b = tmp;
                return;
            }
            if (players[i].pcd[num] == 6) {
                pop(num, pid);
                for (var j = 0; j <= playersIndex; j++) {
                    if (players[j].pid == players[i].epid) {
                        var ca = players[j].card;
                        for (var i = 1; i <= players[j].card; i += 1) {
                            if (players[j].pcd[i] == 3) {
                                pop(i, players[i].epid);
                                break;
                            }
                        }
                        if (players[j].card == ca) {
                            pop(Math.floor(Math.random() * players[j].pcard) + 1, players[j].pid);
                        }
                        return;
                    }
                }
            }
            if (players[i].pcd[num] == 4) { //GDY有BUG
                pop(num, pid);
                if (players[i].b < players[i].a) {
                    players[i].a -= 5;
                    
                }
                players[i].gdy = 1;
                return;
            }
            if (players[i].pcd[num] == 7) { //如果是平行线，那么都取大者
                var x = Math.max(players[i].a, players[i].b);
                players[i].a = x;
                players[i].b = x;
                
                
            }
            if (players[i].pcd[num] == 8) {
                for(var j=0;j<=playersIndex;j++){
                    if(players[j].pid==players[i].epid){
                        var a,b;
                        if(players[j].pcard==0){
                            break;
                        }
                        if(players[j].pcard==1){
                            a=players[j].pcd[players[j].pcard];
                            players[j].pcd[players[j].pcard]=0;
                            players[j].pcard--;
                            b=0;
                        }
                        else {
                            a=players[j].pcd[players[j].pcard];
                            players[j].pcd[players[j].pcard]=0;
                            players[j].pcard--;
                            b=players[j].pcd[players[j].pcard];
                            players[j].pcd[players[j].pcard]=0;
                            players[j].pcard--;
                        }
                        if(players[i].pcard==6){
                            break;
                        }
                        if(players[i].pcard==5){
                            players[i].pcd[players[i].pcard+1]=a;
                            players[i].pcard+=1;
                            wsSend(players[j].pid,players[j]);
                            wsSend(players[i].pid,players[i]);
                            break;
                        }
                        players[i].pcd[players[i].pcard+1]=a;
                        players[i].pcd[players[i].pcard+2]=b;
                        players[i].pcard+=2;
                        wsSend(players[j].pid,players[j]);
                        wsSend(players[i].pid,players[i]);
                    }
                }
            }
            if (players[i].pcd[num] == 9) {
                for(var j=0;j<=playersIndex;j++){
                    if(players[j].pid==players[i].epid){
                        players[j].d--;
                        wsSend(players[j].pid,players[j]);
                    }
                }
            }
            if (players[i].pcd[num] == 11) { //如果是博学者，那么将没有吃饱的刘仓置入手牌
                pop(num, pid);
                players[i].pcard += 1;
                players[i].pcd[players[i].pcard] = 2;
                wsSend(players[i].pid,players[i]);
                return;
            }
            if (players[i].pcd[num] == 12) {
                pop(num, pid);
                getcard(players[i].pid);
                return;
            }
            if (players[i].pcd[num] == 13 && players[i].pcard > 3) {
                pop(num, pid);
                acticard(Math.floor(Math.random() * players[i].pcard) + 1);
                return;
            }
            if (players[i].pcd[num] == 14) {
                pop(num, pid);
                pop(Math.floor(Math.random() * players[i].pcard) + 1, pid);
                return;
            }
            if (players[i].pcd[num] == 15) {
                pop(num, pid);
                players[i].had[16]--;
                getcard(players[i].pid);
                pop(Math.floor(Math.random() * players[i].pcard) + 1, pid);
                return;
            }
            if (players[i].pcd[num] == 16) {
                pop(num,pid);
                var x = Math.min(players[i].a, players[i].b);
                players[i].a = x;
                players[i].b = x;
                return;
            }
            if (players[i].pcd[num] == 17) {
                pop(num, pid);
                pop(Math.floor(Math.random() * players[i].pcard) + 1, pid);
                var maxn = -1, maxi;
                for (var j = 1; j <= cards; j += 1) {
                    if (players[i].had[j] != 2 && maxn < cardcost[j]) {
                        maxn = cardcost[j];
                        maxi = j;
                    }
                }
                players[i].had[maxi] += 1;
                players[i].pcard += 1;
                players[i].pcd[players[i].pcard] = maxi;
                return;
            }
            if (players[i].pcd[num] == 18) {
                pop(num, pid);
                while (players[i].pcard < 5 && !empty(pid)) getcard();
                return;
            }
            if (players[i].pcd[num] == 20) {
                for (var i = 1; i < players[i].monk; i++) {
                    players[i].a += 3;
                    players[i].b += 3;
                }
            }
            if (players[i].pcd[num] == 21) {
                if (players[i].monk > 1) inc(21, pid);
            }
            if (players[i].pcd[num] == 22) {
                players[i].had[24] -= 2 * players[i].monk + 2;
            }
            if (players[i].pcd[num] == 23) {
                pop(num, pid);
                while (players[i].pcard < 6 && !empty(pid)) {
                    players[i].pcard += 1;
                    while (players[i].had[players[i].pcd[players[i].pcard]] == 2 || !ismonk(players[i].pcd[players[i].pcard], pid)) {
                        players[i].pcd[players[i].pcard] = Math.floor(Math.random() * cards) + 1;
                    }
                    players[i].had[players[i].pcd[players[i].pcard]] += 1;//记录
                }
                return;
            }
            if (players[i].pcd[num] == 25) {
                players[i].pcard += 1;
                while (players[i].had[players[i].pcd[players[i].pcard]] == 2 || !issipder(players[i].pcd[players[i].pcard], pid)) {
                    players[i].pcd[players[i].pcard] = Math.floor(Math.random() * cards) + 1;
                }
                players[i].had[players[i].pcd[players[i].pcard]] += 1;//记录
            }
            if (players[i].pcd[num] == 26) {
                for(var j=0;j<=playersIndex;j++){
                    if(players[j].pid==players[i].epid){
                        if(players[j].pcard==0){
                            break;
                        }
                        if(players[j].pcard==1){
                            players[j].pcd[players[j].pcard]=0;
                            players[j].pcard--;
                        }
                        else {
                            players[j].pcd[players[j].pcard]=0;
                            players[j].pcard--;
                            players[j].pcd[players[j].pcard]=0;
                            players[j].pcard--;
                        }
                        wsSend(players[j].pid,players[j]);
                    }
                }
            }
            if (players[i].pcd[num] == 27) {
                pop(num,pid);
                var TMP1 = players[i].pcard,TMP2;
                for (var j = 0; j <= playersIndex; j++) {
                    if (players[j] == players[i].epid) {
                        TMP2=players[j].pcard;
                        while (players[j].pcard > 0) pop(players[j].pcard, players[j].pid);
                    }
                }
                while (players[i].pcard > 0) pop(players[i].pcard, pid);
                while (TMP1 > 0) {
                    TMP1--;
                    getcard(pid);
                }
                while (TMP2 > 0) {
                    TMP2--;
                    getcard(players[i].epid);
                }
                return;
            }
            pop(num, pid);
            return;
        }
    }
}

function usecard(num, pid) { //使用第num张手牌
    for (var i = 0; i <= playersIndex; i++) {
        if (players[i].pid == pid) {
            if (num > players[i].pcard || players[i].d < cardcost[players[i].pcd[num]]) return; //如果该位置无牌直接跳出
            players[i].d -= cardcost[players[i].pcd[num]]; //减去钻石
            acticard(num, pid);
            wsSend(pid,players[i]);
            for(var j = 0; j <= playersIndex; j++) {
                if(players[j].pid==players[i].epid)wsSend(players[i].epid,players[j]);
            }
        }
    }
}

wss.on('connection', function (ws) {
    

    ws.on("message", function (message) {
        var msg = JSON.parse(message);
        var type = msg.type;
        var pid = msg.pid;
        var epid = msg.epid;
        switch (type) {
            case "connection":
                for(var i=0;i<=playersIndex;i++){
                    if(players[i].pid==pid){
                        if(players[i].playing==true){
                            playersws[i].ws=ws;
                            console.log(ws.ping());
                            var p = players[i];
                            p.epid = epid;
                            wsSend(pid,p);
                            if (typeof players[find(epid)] != 'undefined'){
                                var ep = players[find(epid)];
                                ep.epid = pid;
                                wsSend(epid,ep);
                            }
                            return;
                        }
                        players[i].epid = epid;
                        players[i].pcd=[0,0,0,0,0,0,0,0];
                        players[i].pcard=0;
                        playersws[i].ws=ws;
                        players[i].had=[2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
                        players[i].a=0;
                        players[i].b=0;
                        players[i].d=1;
                        players[i].amt=1;
                        players[i].monk=0;
                        players[i].spid=0;
                        players[i].skip=false;
                        players[i].gdy=false;
                        players[i].blood=100;
                        players[i].playing=true;
                        players[i].win=false;
                        players[i].lose=false;
                        console.log("客户端 [%s] 重新连接！", pid);
                        getcard(pid);
                        getcard(pid);
                        getcard(pid);
                        getcard(pid);
                        wsSend(pid,players[i]);
                        return;
                    }
                }
                players.push({
                    "pid": "null",
                    "pcd": [0,0,0,0,0,0,0,0],
                    "pcard": 0,
                    "had": [2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    "epid": "null",
                    "a": 0,
                    "b": 0,
                    "d": 1,
                    "monk": 0,
                    "spid": 0,
                    "skip": false,
                    "gdy": false,
                    "blood": 100,
                    "amt": 1,
                    "win": false,
                    "lose": false,
                    "playing": false
                });
                playersws.push({
                    "ws": ws
                });
                playersIndex += 1;
                players[playersIndex].pid = pid;
                players[playersIndex].epid = epid;
                console.log("客户端 [%s] 新连接！", pid);
                getcard(pid);
                getcard(pid);
                getcard(pid);
                getcard(pid);
                wsSend(pid,players[playersIndex]);
                break;
            case "message":
                if (msg.msgtype == "updateHand") {
                    switch (msg.updateType) {
                        case "useCard":
                            usecard(msg.handNo, pid);
                            break;
                    }
                }
                if (msg.msgtype == "skip") {
                    var index,indexe;
                    for(var i=0;i<=playersIndex;i++){
                        if(pid==players[i].pid){
                            index=i;
                        }
                        if(epid==players[i].pid){
                            indexe=i;
                        }
                    }
                    players[index].skip=true;
                    if(players[index].skip&&players[indexe].skip){
                        players[index].amt++;
                        players[index].d=players[index].amt;
                        players[index].skip=false;
                        players[indexe].amt++;
                        players[indexe].d=players[indexe].amt;
                        players[indexe].skip=false;
                        if(players[index].a>players[indexe].b&&players[indexe].gdy==0){
                            players[indexe].blood-=(players[index].a-players[indexe].b);
                        }
                        if(players[indexe].a>players[index].b&&players[index].gdy==0){
                            players[index].blood-=(players[indexe].a-players[index].b);
                        }
                        players[index].a=0;
                        players[indexe].a=0;
                        players[index].b=0;
                        players[indexe].b=0;
                        players[index].gdy=0;
                        players[indexe].gdy=0;
                        getcard(epid);
                        getcard(pid);
                        wsSend(epid,players[indexe]);
                    }
                    if(players[index].blood<=0){
                        players[index].lose=true;
                        players[indexe].win=true;
                        wsSend(epid,players[indexe]);
                        wsSend(pid,players[index]);
                        playersws[indexe].ws.close();
                        playersws[index].ws.close();
                        players[indexe].playing=false;
                        players[index].playing=false;
                        return;
                    }
                    if(players[indexe].blood<=0){
                        players[indexe].lose=true;
                        players[index].win=true;
                        wsSend(epid,players[indexe]);
                        wsSend(pid,players[index]);
                        playersws[indexe].ws.close();
                        playersws[index].ws.close();
                        players[indexe].playing=false;
                        players[index].playing=false;
                        return;
                    }
                    wsSend(pid,players[index]);
                }
                if(msg.msgtype == "exit"){
                    var index,indexe;
                    for(var i=0;i<=playersIndex;i++){
                        if(pid==players[i].pid){
                            index=i;
                        }
                        if(epid==players[i].pid){
                            indexe=i;
                        }
                    }
                    players[index].playing=false;
                    players[indexe].playing=false;
                    players[indexe].win=true;
                    wsSend(epid,players[indexe]);
                }
                console.log("客户端 [%s] 发送消息 [%s]", pid, msg.msgtype);
        }
    });
});
process.on('SIGINT', function () {
    console.log("服务器关闭中...");
    wss.close();
    process.exit();
});
// function create(IP){
//     var server = new WebSocket(IP);
//     server.onopen = function(evt) {
//         console.log("连接成功！");
//     };
//     server.onmessage = function(evt) {
//         console.log("收到消息："+evt.data);
//         server.close();
//     };
//     server.onclose = function(evt) {
//         console.log("连接终止");
//     }
//     server.onerror = function(){
//         console.log("出现未知错误，连接终止。请检查互联网连接");
//     }
// }