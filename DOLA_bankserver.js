// DOLA server

const bank = "DOLA";
const ctry = "VE";

const express = require('express');
// const http = require('http');
const https = require('https');
const mysql = require('mysql2');
const messages = require('./messages.json');

const r = messages.DOLA;
const wysd = messages.wysd;

const app = express();
app.use(express.json());

const landserver = "145.24.222.239";

var con = mysql.createConnection({
    host: "localhost",
    user: "thijs",
    password: "Some_NewWachtwo0rd",
    database: "DollasBank",
    port: 8000
});

async function sendRequest(sendBody, apiMethod, callback) {
    // functie aangeroepen wanneer DOLA server gegevens van buiten moet ophalen
    const apiMethodStr = '/'.concat(apiMethod);
    const options = {
        host: landserver,
        port : 8443,
        path: apiMethodStr,
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        rejectUnauthorized: false,
        timeout: 3000
    };

    try {
        const req = await https.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => {
                data += chunk;
            });
            res.on('end', () => {
                callback(true, res.statusCode, data);
            });

            req.on('socket', function (socket) {
                socket.setTimeout(https_options.timeout);
                socket.on('timeout', function() {
                    console.log(r.timeoutError.message);
                    req.destroy();
                    callback(true, res.statusCode, data);
                });
            });
        }).on("error", (err) => {
            console.log(err.message);
            try {
                callback(false, res.statusCode, data);
                res.write(502);
            } catch (e) {
                console.log("ERROR! Landserver staat niet aan!");
                
            }
            
        });
        req.write(JSON.stringify(sendBody));
        // console.log(sendBody);
        req.end();
    } catch (e) {
        console.log(e);
        callback(false, res.statusCode, data);
    }
}

app.post('/balance', async (req, res) => {
    const fromBank = req.body.head.fromBank;
    const fromCtry = req.body.head.fromCtry;
    const toBank = req.body.head.toBank;
    const toCtry = req.body.head.toCtry;

    const IBAN = req.body.body.acctNo;
    const rekeningNummer = IBAN.substring(10, 14);
    const pincode = req.body.body.pin;

    console.log("Request: balance (" + JSON.stringify(req.body) + ")");

    let saldo;

    if (IBAN.substring(0,6) == "VEDOLA") {
        // gegevens moeten uit database komen
        
        con.connect(function (err) {
            if (err) throw err;
            con.query("SELECT * FROM DollasBank.Pinpassen WHERE IBAN='"+IBAN+"';", function (err, result, fields) {
                if (err) throw err;
                try {
                    // probeer te checken of pincode klopt
                    // Geeft error wanneer record niet voorkomt in database
                    
                    if (result[0].aantalKeerIncorrectePincode > 3) {
                        //console.log(result[0].aantalKeerIncorrectePincode);
                        // pas is geblokeerd!
                        res.status(403).send("[DOLA]: Pas geblokeerd!");
                        console.log("Reponse: 403");
                    }
                    else if (result[0].pincode == pincode) {
                        // pincode klopt
                        con.query("UPDATE DollasBank.Pinpassen SET aantalKeerIncorrectePincode = "+ 0 +" WHERE IBAN='"+IBAN+"';", function (err, result, fields) {
                            if (err) throw err;
                        // pincode klopt
                         });

                        con.connect(function (err) {
                           if (err) throw err;
                           con.query("SELECT saldo FROM DollasBank.Rekeningen WHERE rekeningNummer='"+rekeningNummer+"';", function (err, result, fields) {
                               if (err) throw err;
                               saldo = result[0].saldo;
                               // stuur bericht met saldo terug
                                const body = ({
                                    "head": {
                                        "fromCtry" : toCtry,
                                        "fromBank" : toBank,
                                        "toCtry" :   fromCtry,
                                        "toBank" :   fromBank
                                    },
                                    "body": {
                                        "acctNo" : IBAN,
                                        "balance" : saldo
                                    }
                                });
                                console.log("Response: 200 (" + JSON.stringify(body) + ")");
                                res.json(body);
                            });
                        });
                    }
                    else {
                        // pincode klopt niet!
                        res.status(403).send("[DOLA]: Incorrect Pincode!");
                        console.log("Reponse: 403");
                        foutPlusEen(IBAN);
                    }
                } catch (e) {
                    // IBAN komt niet voor in database
                    res.status(404).send("[DOLA]: pas niet gevonden!");
                    console.log("Reponse: 404");
                }
            });
        });
        
    }
    else if (toBank == "DOLA" && toCtry == "VE") {
        res.status(500).send("[DOLA]: incorrrecte body!");
    }
    else {
        // gegevens moeten van buiten worden opgehaald
        try {
            console.log("Send a request: (" + JSON.stringify(req.body) + ")");
	        const obj = await sendRequest(req.body, "balance", function(success, code, result) {
                // console.log((req.body));
                try {
                    const response = success ? JSON.parse(result) : result;
                    res.status(code).send(response);
                } catch (e) {
                    console.log("error 2");
                }
                console.log("Respons: " + code);
            });
    	} catch(e) {
            console.log(r.awaitError.message + e.message);
            res.status(r.somethingHappened.code).send(r.somethingHappened.message + wysd.seeLogs);
	    }
    }
});

app.post('/withdraw', async (req, res) => {
    const fromBank = req.body.head.fromBank;
    const fromCtry = req.body.head.fromCtry;
    const toBank = req.body.head.toBank;
    const toCtry = req.body.head.toCtry;

    const IBAN = req.body.body.acctNo;
    const rekeningNummer = IBAN.substring(10, 14);
    const pincode = req.body.body.pin;

    const hoeveelheid = req.body.body.amount;

    console.log("Request: withdraw (" + JSON.stringify(req.body) + ")");

    let saldo;

    if (IBAN.substring(0,6) == "VEDOLA") {
        // gegevens moeten uit database komen
        
        con.connect(function (err) {
            if (err) throw err;
            con.query("SELECT * FROM DollasBank.Pinpassen WHERE IBAN='"+IBAN+"';", function (err, result, fields) {
                if (err) throw err;
                try {
                    
                    if (result[0].aantalKeerIncorrectePincode > 3) {
                        //console.log(result[0].aantalKeerIncorrectePincode);
                        // pas is geblokeerd!
                        res.status(403).send("[DOLA]: Pas geblokeerd!");
                        console.log("Reponse: 403");
                    }
                    // probeer te checken of pincode klopt
                    // Geeft error wanneer record niet voorkomt in database
                    else if (result[0].pincode == pincode) {
                        // pincode klopt
                        con.query("UPDATE DollasBank.Pinpassen SET aantalKeerIncorrectePincode = "+ 0 +" WHERE IBAN='"+IBAN+"';", function (err, result, fields) {
                            if (err) throw err;
                        // pincode klopt
                         });

                        con.connect(function (err) {
                           if (err) throw err;
                           con.query("SELECT saldo FROM DollasBank.Rekeningen WHERE rekeningNummer='"+rekeningNummer+"';", function (err, result, fields) {
                               if (err) throw err;
                               console.log(saldo);
                               saldo = result[0].saldo;
                               nieuwSaldo = saldo - hoeveelheid;
                               console.log(nieuwSaldo);
                               if(nieuwSaldo <= saldo && nieuwSaldo >= 0) {
                                // if(true) {
                                    // hoeveelheid is niet negatief en nieuw saldo is niet negatief, dus transactie mag uitgevoerd worden
                                    con.query("UPDATE DollasBank.Rekeningen SET saldo = "+ nieuwSaldo +" WHERE rekeningNummer='"+rekeningNummer+"';", function (err, result, fields) {
                                        if (err) {
                                            // stuur bericht met saldo terug
                                            const body = ({
                                                "head": {
                                                    "fromCtry" : toCtry,
                                                    "fromBank" : toBank,
                                                    "toCtry" :   fromCtry,
                                                    "toBank" :   fromBank
                                                },
                                                "body": {
                                                    "succes" : false,
                                                    "acctNo" : IBAN,
                                                    "balance" : saldo
                                                }
                                            });
                                            console.log("Response: 200 (" + JSON.stringify(body) + ")");
                                            res.json(body);
                                        }
                                        else {
                                            // transactie is geslaagd
                                            // stuur bericht met saldo terug
                                            const body = ({
                                                "head": {
                                                    "fromCtry" : toCtry,
                                                    "fromBank" : toBank,
                                                    "toCtry" :   fromCtry,
                                                    "toBank" :   fromBank
                                                },
                                                "body": {
                                                    "succes" : true,
                                                    "acctNo" : IBAN,
                                                    "balance" : nieuwSaldo
                                                }
                                            });
                                            console.log("Response: 200 (" + JSON.stringify(body) + ")");
                                            res.json(body);
                                        }
                                        
                                    });                                
                               }
                               else {
                                    // transactie mag niet uitgevoerd worden
                                    // stuur bericht met saldo terug
                                    const body = ({
                                        "head": {
                                            "fromCtry" : toCtry,
                                            "fromBank" : toBank,
                                            "toCtry" :   fromCtry,
                                            "toBank" :   fromBank
                                        },
                                        "body": {
                                            "succes" : false,
                                            "acctNo" : IBAN,
                                            "balance" : saldo
                                        }
                                    });
                                    console.log("Response: 200 (" + JSON.stringify(body) + ")");
                                    res.json(body);
                               }
                            });
                        });
                    }
                    else {
                        // pincode klopt niet!
                        res.status(403).send("[DOLA]: Incorrect Pincode!");
                        console.log("Reponse: 403");
                        foutPlusEen(IBAN);
                    }
                } catch (e) {
                    // IBAN komt niet voor in database
                    res.status(404).send("[DOLA]: pas niet gevonden!");
                    console.log("Reponse: 404");
                }
            });
        });
        
    }
    else if (toBank == "DOLA" && toCtry == "VE") {
        res.status(500).send("[DOLA]: incorrrecte body!");
    }
    else {
        // gegevens moeten van buiten worden opgehaald
        try {
            console.log("Send a request: (" + JSON.stringify(req.body) + ")");
	        const obj = await sendRequest(req.body, "withdraw", function(success, code, result) {
                // console.log((req.body));
                try {
                    const response = success ? JSON.parse(result) : result;
                } catch (e) {
                    console.log("error");
                }
                res.status(code).send(response);
                console.log("Respons: " + code);
            });
    	} catch(e) {
            console.log(r.awaitError.message + e.message);
            res.status(r.somethingHappened.code).send(r.somethingHappened.message + wysd.seeLogs);
	    }
    }
});

function foutPlusEen(IBAN) {
    try {
        con.query("SELECT * FROM DollasBank.Pinpassen WHERE IBAN='"+IBAN+"';", function (err, result, fields) {
            if (err) throw err;
            // aantalKeerIncorrectePincode + 1
            const nieuwAantalKeerIncorrectePincode = result[0].aantalKeerIncorrectePincode + 1
            console.log(nieuwAantalKeerIncorrectePincode);
            con.query("UPDATE DollasBank.Pinpassen SET aantalKeerIncorrectePincode = "+ nieuwAantalKeerIncorrectePincode +" WHERE IBAN='"+IBAN+"';", function (err, result, fields) {
                if (err) throw err;
            });
        })
    } catch (e) {
        console.log(e);
    }
    
} 


app.listen(8443, () => {
    console.log("server started");
});
