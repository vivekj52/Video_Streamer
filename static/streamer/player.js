function httpGet(theUrl)
    {
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
        xmlHttp.send( null );
        return xmlHttp.responseText;
    }

    let movies = httpGet('movies');
    movies = JSON.parse(movies);
    console.log(movies);
    let ul = document.createElement('ul');

    document.getElementById('myItemList').appendChild(ul);

    movies.forEach(function (movie) {
        let li = document.createElement('li');
        li.onclick = function(){
            let name = li.innerText;
            let path = "";
            for (let i = 0; i < movies.length; i++){
                if (movies[i].name == name)
                    path = movies[i].path;
            }
            let vid = document.getElementsByTagName('iframe')[0];
            console.log(path);
            vid.src = "video?path="+path;
        };
        ul.appendChild(li);

    li.innerHTML += movie.name;
    });