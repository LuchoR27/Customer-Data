document.addEventListener('DOMContentLoaded', () => {
    const saveData = (function () {
        const a = document.createElement("a");
        document.body.appendChild(a);
        a.style = "display: none";
        return function (data, fileName) {
            const blob = new Blob([data], {type: "octet/stream"}),
                url = window.URL.createObjectURL(blob);
            a.href = url;
            a.download = fileName;
            a.click();
            window.URL.revokeObjectURL(url);
        };
    }());
    $('.list-group-item').on('click', function() {
        let selected_province = $( this ).text();
        $.get(get_cities_url, { province: $( this ).text() } )
        .done(function( data ) {
            $("#cities-container").empty();
            let cities = JSON.parse("[" + data + "]")[0];
            for(let i = 0; i < cities.length; i++) {
                let city = document.createElement("li");
                city.className = 'list-group-item list-group-item-action city';
                city.innerHTML = cities[i];
                $("#cities-container").append(city);
            }
            $('.city').click(function() {
                console.log(selected_province);
                $.get(download_csv_url, {city: $( this ).text(), province: selected_province } )
                .done(function( data ) {
                    saveData(data, 'data.csv');
                });
            });
        });
    });
});