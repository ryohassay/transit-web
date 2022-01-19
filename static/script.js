// ============================== Top page ==============================
function showInputForm(){
    for(let i = 0; i < 5; i++){
        let required = ['required ', '', '', '', '']
        let input_form =
            '<p>' +
            '    <input type="text" name="ip[' + i + '][\'start\']" placeholder="出発地" ' + required[i] + ' autocomplete="on" list="stations" autofocus>' +
            '    &ensp;→&ensp;' +
            '    <input type="text" name="ip[' + i + '][\'dest\']" placeholder="到着地" ' + required[i] + ' autocomplete="on" list="stations">' +
            '    &emsp;' +
            '    <input type="date" name="ip[' + i + '][\'date\']">' +
            '    <input type="time" name="ip[' + i + '][\'time\']">' +
            '    &emsp;' +
            '    <input type="radio" name="ip[' + i + '][\'tm_type\']" value="non" checked> 指定なし' +
            '    <input type="radio" name="ip[' + i + '][\'tm_type\']" value="dep"> 出発' +
            '    <input type="radio" name="ip[' + i + '][\'tm_type\']" value="arr"> 到着' +
            '</p>'

        document.getElementById("input-form").insertAdjacentHTML('beforebegin', input_form);
    }
}


function convertCSVtoArray(str){
    let array = []
    let rows = str.split("\n");

    let size = rows.length;
    for(let i = 0; i < size - 1; i++){
        array[i] = rows[i + 1].split(',');  // Omits the first row
    }
    return array
}


function createOptionHTML(sta_info){
    let stations = sta_info.map(item => item[2]);

    var datalist = document.createElement('datalist');
    datalist.id = 'stations';

    stations.forEach(name => {
        var option = document.createElement('option');
        option.value = name;
        datalist.appendChild(option);
    });
    document.body.appendChild(datalist);
}


function getCSV(csv_file){
    fetch(csv_file, {
        method: 'GET'
    }).then(res => res.text())
    .then((res_text) => {
        let array = convertCSVtoArray(res_text)
        createOptionHTML(array)
    }).catch((err) => {
        console.error(err);
    });
}


function showCandidates(){
    // Downloaded from https://ekidata.jp/
    const file_name = "../static/stations.csv";  // Directory seen from `index.html`
    getCSV(file_name);
}


function showError(error){
    if(error != null){
        alert(error)
    }
}


// ============================== Result page ==============================
function showResults(routes){
    console.log(routes)

    let total_fare = 0;
    let html = "";
    size = routes.length
    for(let i = 0; i < size; i++){
        total_fare += routes[i].fare;

        let top_html =
            '<div class="subtitle">' +
                routes[i]["start"] + '&ensp;→&ensp;' + routes[i]["dest"] +
            '</div>' +
            '<div class="fare">' +
            '    運賃：'+ routes[i]["fare"] + '円' +
            '</div>' +
            '<div class="detail">' +
            '    <div class="result-box">' +
            '        <table class="route-tb">'

        html += top_html

        size_trpt = routes[i]["transports"].length
        for(let j = 0; j < size_trpt; j++){
            let dep_tm = routes[i]["stations"][j]["dep_tm"]
            if(dep_tm == null){
                dep_tm = ""
            }

            let arr_tm = routes[i]["stations"][j]["arr_tm"]
            if(arr_tm == null){
                arr_tm = ""
            }

            let sta_row =
                '<tr class="sta-row">' +
                '    <td class="time">' +
                '        <ul>' +
                '            <li>' +
                                arr_tm +
                '            </li>' +
                '            <li>' +
                                dep_tm +
                '            </li>' +
                '        </ul>' +
                '    </td>' +
                '    <td class="symbol"><span class="circle"></span></td>' +
                '    <td class="name">' + routes[i]["stations"][j]["name"] + '</td>' +
                '</tr>'

            let trpt_row =
                '<tr class="trpt-row">' +
                    '<td class="time">' + '</td>' +
                    '<td class="line"><span class="line-color" style="background-color: ' + routes[i]["transports"][j]["color"] + ';"></span></td>' +
                    '<td class="transport">' + routes[i]["transports"][j]["name"] + '</td>' +
                '</tr>'

            html += sta_row
            html += trpt_row
        }

        let arr_tm_last = routes[i]["stations"][size_trpt]["arr_tm"]
        if(arr_tm_last == null){
            arr_tm_last = ""
        }
        let sta_row_last =
            '<tr class="sta-row">' +
            '    <td class="time">' +
            '        <ul>' +
            '            <li>' +
                            arr_tm_last +
            '            </li>' +
            '        </ul>' +
            '    </td>' +
            '    <td class="symbol"><span class="circle"></span></td>' +
            '    <td class="name">' + routes[i]["stations"][size_trpt]["name"] + '</td>' +
            '</tr>'
        html += sta_row_last

        let bottom_html = '</table><div><a href="' + routes[i]["url"] + '">Yahoo!乗換案内リンク</a></div></div></div>'
        html += bottom_html
    }

    fare_html = '<div class="total-fare"> 合計運賃：' + total_fare + '円</div>'
    document.getElementById("results").insertAdjacentHTML('beforeend', html);
    document.getElementById("results").insertAdjacentHTML('beforeend', fare_html);
}
