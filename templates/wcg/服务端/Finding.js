console.log("服务器启动中...");
const ws = require('ws').Server;
const WebSocket = require('ws');

var players = [];
var playersws = [];
var playersIndex = -1;

