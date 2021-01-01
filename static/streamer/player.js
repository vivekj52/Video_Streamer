function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

let ul = document.createElement('ul');

let videos = httpGet('videos');
videos = JSON.parse(videos);
console.log(videos);

document.getElementById('myItemList').appendChild(ul);

videos.forEach(function (video) {
    let li = document.createElement('li');
    li.onclick = function () {
        let title = li.innerText;

        for (let i = 0; i < videos.length; i++) {
            if (videos[i].pk == title) {
                let path = videos[i].fields.file;
                let description = videos[i].fields.description;
                let author = videos[i].fields.author;
                let upload_time = videos[i].fields.time;

                let player = document.getElementById('player');
                let title_p = document.getElementById('title');
                let description_p = document.getElementById('description');
                let author_p = document.getElementById('author');
                let time_p = document.getElementById('time');

                player.src = "video?path=" + path;
                title_p.innerText = title;
                description_p.innerText = description;
                author_p.innerText = author;
                time_p.innerText = upload_time;
                break;
            }
        }

    };
    ul.appendChild(li);

    li.innerHTML += video.pk;
});