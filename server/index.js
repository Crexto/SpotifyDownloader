const clientId = process.env['clientid']
const clientSecret = process.env['clientsec']
const axios = require('axios')
const express = require('express')
const Scraper = require('@yimura/scraper').default;
const youtube = new Scraper();
const SpotifyWebApi = require('spotify-web-api-node');
const fs = require('fs')
const fsex = require('fs-extra')
const ytdl = require('ytdl-core');

const editJsonFile = require("edit-json-file");
var qs = require('querystring');

fsex.emptyDirSync('./data');

const bodyParser = require("body-parser");
const router = express.Router();
const app = express();

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

function makeid(length) {
    var result = '';
    var characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for (var i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() *
            charactersLength));
    }
    return result;
}

app.use("/", router);

app.get('/', function (req, res) {
    res.sendStatus(200)
})

var spotifyApi = new SpotifyWebApi({
    clientId: clientId,
    clientSecret: clientSecret,
});

router.post("/getyt", async (req, res) => {

    try {

        const response = await axios.post('https://accounts.spotify.com/api/token', qs.stringify({ 'grant_type': 'client_credentials' }), {
            headers: {
                'Authorization': `Basic ${new Buffer.from(clientId + ':' + clientSecret).toString('base64')}`,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        if (response.status === 200) {
            spotifyApi.setAccessToken(response.data.access_token);

            spotifyApi.getPlaylist(req.body.id)
                .then(async function (data) {
                    songs = data.body.tracks.items;

                    const token = makeid(5)
                    const result = await youtube.search(songs[0].track.name)
                    var stream = ytdl(result.videos[0].id, { filter: 'audioonly' }).pipe(fs.createWriteStream('./data/'+token+'.mp3'));

                    const map = await Promise.all(songs.slice(1,songs.length).map(async (song, index) => {
                        try {
                            const results = await youtube.search(song.track.name)

                            return { name: song.track.name, id: results.videos[0].id, index: index };
                        }
                        catch (err) {
                            throw (err)
                        }

                    }));

                    stream.on('finish', function () {
                        res.send({
                            status: true,
                            link: "https://spotify.zodiacthedev.repl.co/download/"+token+'.mp3',
                            token: token,
                            name: songs[0].track.name,
                            playlist:{
                                name:data.body.name,
                                owner:data.body.owner.display_name,
                                desc:data.body.description,
                                image:data.body.images[0].url,
                                tracks:map,
                            
                            }
                        })
                    });  

                    const results = {
                        "tracks": map,
                        "time": Date.now(),
                        "downloaded": 1
                    }

                    fs.writeFile(`data/${token}.json`, JSON.stringify(results), function (err, result) {
                        if (err) console.log('error', err);
                    });


                }, function (err) {
                    console.log('Something went wrong!', err);
                    res.send({
                        status: false
                    })
                });
        }
    } catch (error) {
        console.log(error);
    }

});

router.post("/gettracks", async (request, response) => {
    if (fs.existsSync("./data/" + request.body.token + ".mp3")) {
        fs.unlinkSync("./data/" + request.body.token + ".mp3")
    }

    if (!fs.existsSync("./data/" + request.body.token + ".json")) {
        console.log("invalid")
        response.send("invalid")

    } else {

        fs.readFile("./data/" + request.body.token + ".json", 'utf8', async (err, jsonString) => {
            if (err) {
                console.log("Error reading file from disk:", err)
                return
            }
            try {
                console.log(request.body)
                const data = JSON.parse(jsonString)

                if (data.tracks.length === 0) {
                    fs.unlinkSync("./data/" + request.body.token + ".json")
                    return response.send("finished")

                } else {

                    var stream = ytdl(data.tracks[0].id, { filter: 'audioonly' }).pipe(fs.createWriteStream('./data/'+request.body.token+'.mp3'));

                    stream.on('finish', function () {
                        response.send({
                            link: "https://spotify.zodiacthedev.repl.co/download/"+request.body.token+'.mp3',
                            name: data.tracks[0].name,
                            i: data.downloaded + 1
                        })
                    });

                    const fe = editJsonFile("./data/" + request.body.token + ".json")

                    fe.set("downloaded", data.downloaded + 1)
                    fe.pop("tracks")
                    fe.save()
                }

            } catch (err) {
                console.log('Error parsing JSON string:', err)
            }
        })
    }
});

router.get('/download/:file(*)', (req, res) => {
    var file = req.params.file;
    var fileLocation = "./data/" + file;
    console.log(fileLocation);
    res.download(fileLocation, file);
});

const port = 3000

app.listen(port, () => {
    console.log(`Crex server is listening on port ${port}`)
})