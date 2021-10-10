function set_button(){
    var button_list = document.querySelectorAll("button")
    for(var index = 0; index<Object.keys(button_list).length; index++){
        button_list[index].onclick = function(){
            var url = url_data[this.id];
            count_zoom_open(this.id,url)
            if(hyperlink === false)
            {
                var url  = "https://zoom.us/j/" +  url.split("no=")[1];
            }
            window.open(url, target = "_parent");
        } 
        }
}