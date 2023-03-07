const express = require('express');
const router = express.Router();
const config = require('./nhlConfig');

let harness = null;

// set the appropriate data harness - MYSQL or FAKE
if (config.data.type === "FIREBASE") {
    console.log("** Using FIREBASE Data Harness **");
    harness = require('./data/harness-firebase');
} else {
    console.log("!!! Harness type is NOT defined", config.data.type);
}

// Load data harness (whatever needs to happen here)
harness.load();

router.get('/', (req, res) => {
    res.send(`Communications Dashboard REST API ${config.apiVersion}`);
});

// TEAMS ------------------------------------->

/**
 * Returns teams by year
*/

router.get('/sessions/:year', (req, res) => {
    const seasonYear = req.params.year;
    
    console.log("** Get teams by year", seasonYear);

    harness.getTeamsByYear(seasonYear, (response, error) => {
        if (!error) {
            res.status(200).json(response);
        } else {
            console.log("! ERROR retrieving session", error);
        }
     });
});


// PLAYERS ------------------------------------->
router.get('/entities', (req, res) => {
    console.log("** Get all entities...");

    harness.getEntities((response, error) => {
        if (!error) {
            res.status(200).json(response);
        } else {
            console.log("! ERROR retrieving all entities", error);
        }
     });
});

/**
 * Returns entity by:
 *  sessionId
 */
router.get('/entities/session/:id', (req, res) => {
    const sessionId = req.params.id;

    console.log("** Get entity by session id [sessionId]", sessionId);
    
    harness.getEntitiesBySession(sessionId, (response, error) => {
        if (!error) {
            res.status(200).json(response);
        } else {
            console.log("! ERROR retrieving entities", error);
        }
     });
});

/**
 * Returns entity by:
 *  disid
 */
router.get('/entities/disid/:id', (req, res) => {
    const disId = req.params.id;

    console.log("** Get entity by DIS id [disId]", disId);
    
    harness.getEntitiesByDISId(disId, (response, error) => {
        if (!error) {
            res.status(200).json(response);
        } else {
            console.log("! ERROR retrieving entities", error);
        }
     });
});

/**
 * Returns entity by:
 *   id, sessionId, force, callsign, kind, domain, country, min_x, max_x, min_y, max_y
 */
router.get('/entity', (req, res) => {
    const entityId = req.query["id"] || null;
    const sessionId = req.query["sessionid"] || null;
    const force = req.query["force"] || null;
    const callsign = req.query["callsign"] || null;
    const kind = req.query["kind"] || null;
    const domain = req.query["domain"] || null;
    const country = req.query["country"] || null;
    const min_x = req.query["min_x"] || null;
    const max_x = req.query["max_x"] || null;
    const min_y = req.query["min_y"] || null;
    const max_y = req.query["max_y"] || null;
     
    console.log("** Get entity meta by info [entityId, sessionId, force, callsign, kind, domain, country, min_x, max_x, min_y, max_y]", entityId, sessionId, force, callsign, kind, domain, country, min_x, max_x, min_y, max_y);
    
    harness.getEntityByParameters( entityId, sessionId, force, callsign, kind, domain, country, min_x, max_x, min_y, max_y, (response, error) => {
        if (!error) {
            res.status(200).json(response);
        } else {
            console.log("! ERROR retrieving entities", error);
        }
     });
});


// Events ------------------------------------->
/**
 * Returns events by:
 *  sessionId
 */
router.get('/events/session/:id', (req, res) => {
    const sessionId = req.params.id;

    console.log("** Get event by session id [sessionId]", sessionId);
    
    harness.getEventsBySession(sessionId, (response, error) => {
        if (!error) {
            res.status(200).json(response);
        } else {
            console.log("! ERROR retrieving events", error);
        }
     });
});

// Radios ------------------------------------->
/**
 * Returns radios by:
 *  sessionId
 */
router.get('/radios/session/:id', (req, res) => {
    const sessionId = req.params.id;

    console.log("** Get radios by session id [sessionId]", sessionId);
    
    harness.getRadiosBySession(sessionId, (response, error) => {
        if (!error) {
            res.status(200).json(response);
        } else {
            console.log("! ERROR retrieving radios", error);
        }
     });
});

/**
 * Returns radios by:
 *  id, entity id
 */
router.get('/radio', (req, res) => {
    const radioId = (req.query["id"]) || null;
    const sessionId = (req.query["sessionid"]) || null;
    const entityId = (req.query["entityId"]) || null;
   
    console.log("** Get radio by info [radioId, sessionId, entityId]", radioId, sessionId, entityId);
    
    harness.getRadiosByParameters(radioId, sessionId, entityId, (response, error) => {
        if (!error) {
            res.status(200).json(response);
        } else {
            console.log("! ERROR retrieving radios", error);
        }
     });
});

// Frequencies ------------------------------------->
/**
 * Returns frequencies by:
 *  sessionId
 */
router.get('/frequencies/session/:id', (req, res) => {
    const sessionId = req.params.id;

    console.log("** Get frequencies by session id [sessionId]", sessionId);
    
    harness.getFrequenciesBySession(sessionId, (response, error) => {
        if (!error) {
            res.status(200).json(response);
        } else {
            console.log("! ERROR retrieving frequencies", error);
        }
     });
});

/**
 * Returns frequency by:
 *  id, mhz
 */
router.get('/frequency', (req, res) => {
    console.log(req.query)
    const frequencyId = (req.query["id"]) || null;
    const sessionId =  (req.query["sessionid"]) || null;
    const min_mhz = (req.query["min_mhz"]) || null;
    const max_mhz = (req.query["max_mhz"]) || null;
   
    console.log("** Get frequency by info [frequencyId, sessionId, min_mhz, max_mhz]", frequencyId, sessionId, min_mhz, max_mhz);
    
    harness.getFrequenciesByParameters(frequencyId, sessionId, min_mhz, max_mhz, (response, error) => {
        if (!error) {
            res.status(200).json(response);
        } else {
            console.log("! ERROR retrieving frequencies", error);
        }
     });
});

// Audios ------------------------------------->
/**
 * Returns audios by:
 *  sessionId
 */
router.get('/audios/session/:id', (req, res) => {
    const sessionId = req.params.id;

    console.log("** Get audios by session id [sessionId]", sessionId);
    
    harness.getAudiosBySession(sessionId, (response, error) => {
        if (!error) {
            res.status(200).json(response);
        } else {
            console.log("! ERROR retrieving audios", error);
        }
     });
});

/**
 * Returns audio by:
 *  id, mhz
 */
router.get('/audio', (req, res) => {
    const audioId = (req.query["id"]) || null;
    const sessionId =  (req.query["sessionid"]) || null;
    const radioId = (req.query["radioid"]) || null;
    const starttime = (req.query["starttime"]) || null;
    const endtime = (req.query["endtime"]) || null;
    const transcript = (req.query["transcript"]) || null;
   
    console.log("** Get frequency by info [audioId, sessionId, radioId, starttime, endtime, transcript]", audioId, sessionId, radioId, starttime, endtime, transcript);
    
    harness.getAudiosByParameterscd(audioId, sessionId, radioId, starttime, endtime, transcript, (response, error) => {
        if (!error) {
            res.status(200).json(response);
        } else {
            console.log("! ERROR retrieving audios", error);
        }
     });
});

/**
 * Returns audio waveform by:
 *  id
 */
router.get('/audio/img/:id', (req, res) => {
    const audioId = req.params.id;
    
    //console.log("** Get audio waveform by id", audioId);

    harness.getAudioWaveformById(audioId, (response, contentType, error) => {
        if (!error) {
            res.writeHead(200, {
                "Content-Type": contentType });
                res.end(response);
        } else {
            console.log("! ERROR retrieving waveform", error);
        }
     });
});

/**
 * Returns audio wav file by:
 *  id
 */
router.get('/audio/wav/:id', (req, res) => {
    const audioId = req.params.id.replace('.wav', '');
    
    //console.log("** Get audio wav file by id", audioId);

    harness.getAudioFileById(audioId, (response, contentType, error) => {
        if (!error) {
            res.writeHead(200, {
                "Content-Type": contentType });
                res.end(response);
        } else {
            console.log("! ERROR retrieving audio file", error);
        }
     });
});

router.route('/startIngest/:construct').get((req, res, next) => {
    const construct = req.params.construct;
  
    codaIngester.startIngest(construct, (response, err) => {
      if (!err) {
        res.status(200).json(response);
      } else {
        res.status(400).json( {
          err: err
        })
      }
    })
  })

module.exports = router;