const express = require('express');
const fs = require('fs');
const { exec, spawn, fork, execFile } = require('promisify-child-process');

const scripts = __dirname + '/scripts';

const app = express();

let port = 2005;

app.get('/', function (req, res) {
    res.send('RSS dumb server');
});

function get_feed_list() {
    let feeds = [];
    let feedFolder = __dirname + '/feeds';
    let folders = fs.readdirSync(feedFolder);

    for (let i = 0; i < folders.length; i++) {
        let folder = folders[i];
        if (fs.lstatSync(feedFolder + '/' + folder).isDirectory()) {
            feeds.push(folder);
        }
    }

    return feeds;
}

// Analyze the feeds folder and create a page for each feed
app.get('/feeds', function (req, res) {
    // List the subfolders in the feeds folder
    let feeds = get_feed_list();

    // Create the page
    let html = '<html><head><title>RSS feeds</title></head><body>';
    for (let i = 0; i < feeds.length; i++) {
        let feed = feeds[i];
        html += '<a href="/feeds/' + feed + '">' + feed + '</a><br>';
    }
    html += '</body></html>';
    res.send(html);
});


app.get('/feeds/:feed', async (req, res) => {
    let feed = req.params.feed;

    // Check if the request wants to refresh the feed

    console.log(req.query);
    let refresh = req.query.refresh;
    if (refresh) {
        console.log('Refreshing feed of ' + feed);
        // Run python script to refresh the feed
        let scriptname = scripts + "/" + feed + ".py";
        let { stdout, stderr, code } = await spawn(
            'conda',
            ["run", "-n", "rssfeed", scriptname],
            { encoding: 'utf8' });
        if (stderr) {
            console.log(scriptname + " raised errors during execution.")
            console.log(stderr);
        }
        if (stdout) {
            console.log(stdout);
        }
    }

    // Read the feed
    let feedFolder = __dirname + '/feeds/' + feed;

    if (!fs.existsSync(feedFolder)) {
        res.status(404).send('Feed not found');
        return;
    }

    let feedFile = feedFolder + '/feed.xml';

    if (!fs.existsSync(feedFile)) {
        res.status(404).send('Feed found, but without a feed.xml file. Please fix.');
        return;
    }

    let feedData = fs.readFileSync(feedFile, 'utf8');

    // Create the page
    res.set('Content-Type', 'text/xml');
    res.send(feedData);
});

app.listen(port, function () {
    console.log('RSS server listening on port ' + port);
    console.log('List of currently offered feeds:');
    let feeds = get_feed_list();
    for (let i = 0; i < feeds.length; i++) {
        console.log('- ' + feeds[i]);
    }
});