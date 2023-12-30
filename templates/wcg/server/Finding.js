console.log("服务器启动中...");
const ws = require('ws').Server;
const WebSocket = require('ws');
const PORT = 3888;
const wss = new ws({port: PORT});
console.log("服务器启动成功!");

var players = [];
var playersws = [];
var rooms = [];
var playersIndex = -1;
var roomsIndex = -1;
var nowwaitingpid = 'null';

function wsSend(pid, content) {
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

wss.on('connection', function (ws) {

    ws.on("message", function (message) {
        var msg = JSON.parse(message);
        var type = msg.type;
        var pid = msg.pid;
        switch (type) {
            case 'connection':
                for (var i = 0; i <= playersIndex; i++) {
                    if (players[i].pid == pid) {
                        if (players[i].status == 'playing') {
                            playersws[i].ws = ws;
                            wsSend(pid, players[i]);
                            return;
                        }
                        players[i].pid = pid;
                        players[i].epid = 'null';
                        players[i].status = 'waiting';
                        playersws[i].ws = ws;
                        console.log("客户端 [%s] 重新连接！", pid);
                        wsSend(pid, players[i]);
                        return;
                    }
                }
                players.push({
                    'pid': 'null',
                    'epid': 'null',
                    'status': 'waiting'
                });
                playersws.push({
                    "ws": ws
                });
                playersIndex += 1;
                players[playersIndex].pid = pid;
                console.log("客户端 [%s] 新连接！", pid);
                wsSend(pid, players[playersIndex]);
                break;
            case 'find':
                if (nowwaitingpid != 'null') {
                    for (var i = 0; i <= playersIndex; i++) {
                        if (players[i].pid == nowwaitingpid) {
                            for (var j = 0; j <= playersIndex; j++) {
                                if (players[j].pid == pid) {
                                    players[i].status = 'playing';
                                    players[j].status = 'playing';
                                    players[i].epid = players[j].pid;
                                    players[j].epid = players[i].pid;
                                    wsSend(pid, players[j]);
                                    wsSend(nowwaitingpid, players[i]);
                                    nowwaitingpid = 'null';
                                    playersws[j].ws.close();
                                    playersws[i].ws.close();
                                    return;
                                }
                            }
                        }
                    }
                }
                for (var i = 0; i <= playersIndex; i++) {
                    if (players[i].pid == pid) {
                        players[i].status = 'finding';
                        nowwaitingpid = pid;
                        return;
                    }
                }
                break;
            case 'room':
                if (msg.msgtype == 'create') {
                    rooms.push({
                        'type': 'room',
                        'id': Math.floor(Math.random() * 100000),
                        'pid': pid,
                        'epid': 'null'
                    });
                    roomsIndex++;
                    loop1: while (1) {
                        for (var i = 0; i < roomsIndex; i++) {
                            if (rooms[i].id == rooms[roomsIndex].id) {
                                rooms[roomsIndex].id = Math.floor(Math.random() * 100000);
                                continue loop1;
                            }
                        }
                        break;
                    }
                    for (var i = 0; i <= playersIndex; i++) {
                        if (players[i].pid == pid) {
                            players[i].status = 'room';
                        }
                    }
                    wsSend(pid, rooms[roomsIndex]);
                } else if (msg.msgtype == 'join') {
                    var id = msg.roomid;
                    for (var i = 0; i <= roomsIndex; i++) {
                        if (rooms[i].id == id) {
                            rooms[i].epid = pid;
                            for (var j = 0; j <= playersIndex; j++) {
                                if (players[j].pid == rooms[i].pid) {
                                    if (players[j].status != 'room') {
                                        wsSend(pid, {
                                            'type': 'warning',
                                            'text': "房主已解散房间。"
                                        });
                                        rooms[i].pid = 'null';
                                        rooms[i].epid = 'null';
                                        playersws[j].ws.close();
                                        return;
                                    }
                                    for (var k = 0; k <= playersIndex; k++) {
                                        if (players[k].pid == pid) {
                                            players[j].status = 'playing';
                                            players[k].status = 'playing';
                                            players[j].epid = pid;
                                            players[k].epid = rooms[i].pid;
                                            wsSend(pid, players[k]);
                                            wsSend(rooms[i].pid, players[j]);
                                            playersws[j].ws.close();
                                            playersws[k].ws.close();
                                            rooms[i].pid = 'null';
                                            rooms[i].epid = 'null';
                                            return;
                                        }
                                    }
                                }
                            }
                        }
                    }
                    wsSend(pid, {
                        'type': 'warning',
                        'text': "房间未找到。"
                    });
                }
                break;
            case 'exit':
                for (var i = 0; i <= playersIndex; i++) {
                    if (players[i].pid == pid) {
                        players[i].status = 'waiting';
                        if (nowwaitingpid == players[i].pid) nowwaitingpid = 'null';
                        return;
                    }
                }
                break;
        }
    });
});