const http = require('node:http');
const url = require("url");
const StringDecoder = require("string_decoder").StringDecoder; 
const messages = require('./messages.json');
const r = messages.noob;
const wysd = messages.wysd;
const path = require('path');
const express = require('express');
const app = express();
const fs = require('fs');
const https = require('https');
const certfile = fs.readFileSync(path.join(__dirname, "../documenten", "ve-server.pem"));
const keyfile = fs.readFileSync(path.join(__dirname, "../documenten", "country_key.pem"));
const Banken_Venezuela = {
	"EBDV": {"PORT": '', "IP" :"145.24.222.58"}, 
	"DOLA": {"PORT":"8443", "IP": "145.24.222.63"}, 
	"ELBA": {"PORT":"Niet doorgegeven", "IP": "Niet doorgegeven"}
}; 


//HTTPS options
//Note that rejectUnauth is false in order to politely respond to invalid certs
const opts = {
    key: keyfile ,/*fs.readFileSync(filepaths.t1ServerKey)*/
    cert: certfile , /*fs.readFileSync(filepaths.t1ServerChain)*/
    requestCert: false,
    rejectUnauthorized: false,
    //ca: [fs.readFileSync(filepaths.noobRoot),
    //     fs.readFileSync(filepaths.noobCA)]
}

async function HTTP_request_naar_bank(dstIP, port, sentObj, apiMethod, callback){
	const apiMethodStr = '/'.concat(apiMethod);
	const options = {
	  hostname: dstIP,
	  port: port,
	  path: apiMethodStr,
	  method: 'POST',
	  headers: {
	    'Content-Type': 'application/json'
	  },
	  timeout:3000
	};
	const req = await http.request(options, (res) => {
	  let data = '';
	  res.setEncoding('utf8');
	  res.on('data', (chunk) => {
		data += chunk;
	  });
	  res.on('end', () => {
	  	try{
				if(typeof(data) == 'string'){
					callback(data, res.statusCode, false);
				}
				else{
					callback(data, 400 , true);
				}
			}
			catch(err){
				console.error(err);
				callback(err.code,408, true);
			}
		});
	});

	req.on('error', (e) => {
	  	console.error(e);
                callback(e.code ,408,true );
	});

	req.write(sentObj);
	req.end();
	}


async function HTTPS_request_naar_NOOB(body_doorsturen, apiMethod, callback) {
	const apiMethodStr = '/'.concat(apiMethod);
       const options = {
       host: '145.24.222.82',
       port : 8443,
       path: '/api'+apiMethodStr,
       method: 'POST',
       headers: {
        'Content-Type': 'application/json',
        },
	cert: certfile,
	key: keyfile,
	rejectUnauthorized: false,
        timeout: 3000
    };
	const req = await https.request(options, (res) => {

		let data = '';

    		console.log('Status Code:', res.statusCode);

    		res.on('data', (chunk) => {
        		data += chunk;
    		});

    		res.on('end', () => {
			try{
				callback(data, res.statusCode, false);
			}
			catch(err){
				console.error(err);
				callback(err.code,408, true);
			}
    		});

		}).on("error", (err) => {
    			console.log("Error: ", err.message);
			callback(err.code,408, true);
		});

	req.write(body_doorsturen);
	req.end();

}


/*async function sendRequest(dstIP, sendObj, apiMethod, httpMethod, _callback) {
    const apiMethodStr = '/'.concat(apiMethod);
    const https_options = {
	host:	 	dstIP,
	port: 		8443,
	path: 		apiMethodStr,
	method:		httpMethod,
        headers:        { 'Content-Type': 'application/json' },
        cert: 		certfile,
	key:            keyfile,
        rejectUnauthorized: false,
	timeout: 	3000
    };

    try {
        const req = await https.request(https_options, (res) => {
	    res.setEncoding('utf8');
	    res.on('data', (obj) => {
		try {
		    const responseObj = JSON.parse(obj);
		    const resFromBank = JSON.parse(responseObj).head.fromBank;
		    const resToBank = sendObj.head.fromBank;
		    console.log("Data van"+  responseObj);
		    _callback(true, res.statusCode, responseObj);
		}
		catch(e) {
                    _callback(false, r.jsonParseError.code, r.jsonParseError.message + wysd.seeLogs);
		}
	    });
	});
	req.on('socket', function (socket) {
    	    socket.setTimeout(https_options.timeout);
    	    socket.on('timeout', function() {
       		req.destroy();
		_callback(false, r.timeoutError.code, r.timeoutError.message);
    	    });
	});
	req.on('error', (e) => {
		req.destroy();
		console.log(e);
	    _callback(false, r.requestCompileError.code, r.requestCompileError.message + wysd.seeLogs);
	});
	req.write(JSON.stringify(sendObj));
	req.end();
    } catch(e) {
	_callback(false, r.sendRequestTLDR.code, r.sendRequestTLDR.message + wysd.blame);
    }
}*/


app.use(express.json())

app.get('/test', (req, res) => {
    console.log("GET");
    //res.status(r.noobTest.code).send(r.noobTest.message);
    res.write("Op deze URL is niks te vinden");
    res.end();
});

app.post('/balance', async (req, res) => {
    	function einde_request(body,status_code, error){
		if(error == true){
			res.writeHead(status_code);
                	res.end(body);
                	console.log("Error: "+body);
			console.log("Status code: "+status_code);
		}
		else{
			res.writeHead(status_code);
			res.end(body);
		}
	}
        res.setHeader('Content-type', 'application/json');//Onze respone zal een JSON object zijn
        res.setHeader('Access-Control-Allow-Origin', "*");//Van elke browser/domain kan een request sturen
    	const methodCalled = "balance";
	var fromCtry_req;
	var fromBank_req;
	var toBank_req;
	var toCtry_req;
	var body_is_correct = true;
	try{
	    	fromCtry_req = req.body.head.fromCtry
	    	fromBank_req = req.body.head.fromBank;
	    	toBank_req = req.body.head.toBank;
	    	toCtry_req = req.body.head.toCtry;
	}
	catch(err){
		body_is_correct = false;
		console.error(err);
		}
	if(body_is_correct && !(fromCtry_req == undefined) && !(fromBank_req == undefined) && !(toBank_req == undefined) && !(toCtry_req == undefined) ){
   	const retObj = JSON.stringify({
            'head': {
                'fromCtry': fromCtry_req,
                'fromBank': fromBank_req,
                'toCtry': toCtry_req,
                'toBank': toBank_req
            },
            'body': req.body.body
   	 });
	console.log('Incoming balance request');
	var toBank = req.body.head.toBank;
        var Land_in_venezuela = false;
            for(let i = 0; i<3 ; i++){
                if(toBank in Banken_Venezuela){
                    Land_in_venezuela = true;
                    break;
                }
            }
	    var dstIP;
	    var PORT;
	    try{
		dstIP =Banken_Venezuela[""+toBank].IP;
		PORT = Banken_Venezuela[""+toBank].PORT;
		console.log("dstIP = "+ dstIP);
		}
	    catch(e){
		dstIP = undefined;
		PORT = undefined;
		}
            if(dstIP == undefined ){
			try {
				console.log("HTTPS request naar NOOB server");
				HTTPS_request_naar_NOOB(retObj, methodCalled, einde_request);
	              } catch(e) {
				console.error(e);
				res.writeHead(400);
				res.end("Error met het opstellen van het request");
	    		}
            }
            else if(dstIP == "Niet doorgegeven"){
			res.writeHead(500);
			res.end("Bank "+toBank+" is niet geregristreerd bij de landserver");

		}
	   else{
		try {
				 console.log("HTTP request naar bank "+ toBank);
				 HTTP_request_naar_bank(dstIP, PORT, retObj ,  methodCalled, einde_request );
	              } catch(e) {
				console.error(e);
				res.writeHead(400);
				res.end("Error met het opstellen van het request");
	    		}
		}
	}
	else{
		res.writeHead(400);
		res.end("Foute body");
		console.log("Foute body. Foutcode 400");
	}

});

app.post('/withdraw', (req, res) => {
	function einde_request(body,status_code, error){
		if(error == true){
			res.writeHead(status_code);
                	res.end(body);
                	console.log("Error: "+body);
			console.log("Status code: "+status_code);
		}
		else{
			res.writeHead(status_code);
			res.end(body);
		}
	}
        res.setHeader('Content-type', 'application/json');//Onze respone zal een JSON object zijn
        res.setHeader('Access-Control-Allow-Origin', "*");//Van elke browser/domain kan een request sturen
    	const methodCalled = "withdraw";
	var fromCtry_req;
	var fromBank_req;
	var toBank_req;
	var toCtry_req;
	var body_is_correct = true;
	try{
	    	fromCtry_req = req.body.head.fromCtry
	    	fromBank_req = req.body.head.fromBank;
	    	toBank_req = req.body.head.toBank;
	    	toCtry_req = req.body.head.toCtry;
	}
	catch(err){
		body_is_correct = false;
		console.error(err);
		}
	if(body_is_correct && !(fromCtry_req == undefined) && !(fromBank_req == undefined) && !(toBank_req == undefined) && !(toCtry_req == undefined) ){
   	const retObj = JSON.stringify({
            'head': {
                'fromCtry': fromCtry_req,
                'fromBank': fromBank_req,
                'toCtry': toCtry_req,
                'toBank': toBank_req
            },
            'body': req.body.body
   	 });
	console.log('Incoming withdraw request');
	var toBank = req.body.head.toBank;
        var Land_in_venezuela = false;
            for(let i = 0; i<3 ; i++){
                if(toBank in Banken_Venezuela){
                    Land_in_venezuela = true;
                    break;
                }
            }
	    var dstIP;
	    var PORT;
	    try{
		dstIP =Banken_Venezuela[""+toBank].IP;
		PORT = Banken_Venezuela[""+toBank].PORT;
		console.log("dstIP = "+ dstIP);
		}
	    catch(e){
		dstIP = undefined;
		PORT = undefined;
		}
            if(dstIP == undefined ){
			try {
				console.log("HTTPS request naar NOOB");
				HTTPS_request_naar_NOOB(retObj, methodCalled, einde_request);
	              } catch(e) {
				console.error(e);
				res.writeHead(400);
				res.end("Error met het opstellen van het request");
	    		}
            }
            else if(dstIP == "Niet doorgegeven"){
			res.writeHead(500);
			res.end("Bank "+toBank+" is niet geregristreerd bij de landserver");

		}
	   else{
		try {
				console.log("HTTP request naar bank "+ toBank);
				HTTP_request_naar_bank(dstIP ,PORT, retObj,methodCalled, einde_request );
	              } catch(e) {
				console.error(e);
				res.writeHead(400);
				res.end("Error met het opstellen van het request");
	    		}
		}
	}
	else{
		res.writeHead(400);
		res.end("Foute body");
		console.log("Foute body. Foutcode 400");
	}
});



const portnumber = 8443;
https.createServer(opts, app).listen(portnumber, function(){
  console.log('Listening on port ' + portnumber);
  
});
