function count_zoom_open(subject, zoom_num){
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === xhr.DONE) {
            if (xhr.status === 200 || xhr.status === 201) {
                console.log(xhr.responseText);
            } else {
                console.error(xhr.responseText);
            }
        }
    };
    xhr.open('GET', 'http://oneclickclass.kr/' + school +'/open_zoom_count/' +grade_class +'/'+subject+'/'+zoom_num.split('=')[3]);
    xhr.send();
}